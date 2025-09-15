"""
Core data filtering functionality using BrightData API.

This module provides the base classes and functionality for filtering data
using the BrightData Marketplace Dataset API across multiple datasets.
"""

import json
import requests
import os
import time
from datetime import datetime
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass
from enum import Enum
from .dataset_registry import get_dataset_schema, validate_field_operator, get_dataset_id


class FilterOperator(Enum):
    """Supported filter operators for the Bright Data API"""
    EQUAL = "="
    NOT_EQUAL = "!="
    LESS_THAN = "<"
    LESS_THAN_EQUAL = "<="
    GREATER_THAN = ">"
    GREATER_THAN_EQUAL = ">="
    IN = "in"
    NOT_IN = "not_in"
    INCLUDES = "includes"
    NOT_INCLUDES = "not_includes"
    ARRAY_INCLUDES = "array_includes"
    NOT_ARRAY_INCLUDES = "not_array_includes"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"


class LogicalOperator(Enum):
    """Logical operators for combining filters"""
    AND = "and"
    OR = "or"


@dataclass
class FilterCondition:
    """Represents a single filter condition"""
    name: str
    operator: FilterOperator
    value: Any = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert filter condition to API format"""
        result = {
            "name": self.name,
            "operator": self.operator.value
        }
        if self.value is not None:
            result["value"] = self.value
        return result
    
    def __and__(self, other: Union['FilterCondition', 'FilterGroup']) -> 'FilterGroup':
        """Override & operator for AND operations - combines into single AND group"""
        if isinstance(other, (FilterCondition, FilterGroup)):
            # If other is already an AND group, add self to it
            if isinstance(other, FilterGroup) and other.operator == LogicalOperator.AND:
                return FilterGroup(LogicalOperator.AND, [self] + other.filters)
            # Otherwise create new AND group
            else:
                return FilterGroup(LogicalOperator.AND, [self, other])
        return NotImplemented
    
    def __or__(self, other: Union['FilterCondition', 'FilterGroup']) -> 'FilterGroup':
        """Override | operator for OR operations"""
        if isinstance(other, (FilterCondition, FilterGroup)):
            return FilterGroup(LogicalOperator.OR, [self, other])
        return NotImplemented
    
    def __add__(self, other: Union['FilterCondition', 'FilterGroup']) -> 'FilterGroup':
        """Override + operator for AND operations (alternative syntax)"""
        return self.__and__(other)
    
    def __str__(self) -> str:
        """Human-readable string representation"""
        if self.value is None:
            return f"{self.name} {self.operator.value}"
        return f"{self.name} {self.operator.value} {self.value}"
    
    def __repr__(self) -> str:
        """Developer representation"""
        return f"FilterCondition(name='{self.name}', operator={self.operator}, value={self.value})"


@dataclass
class FilterGroup:
    """Represents a group of filters with logical operator"""
    operator: LogicalOperator
    filters: List[Union['FilterGroup', FilterCondition]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert filter group to API format"""
        return {
            "operator": self.operator.value,
            "filters": [f.to_dict() for f in self.filters]
        }
    
    def __and__(self, other: Union['FilterCondition', 'FilterGroup']) -> 'FilterGroup':
        """Override & operator for AND operations - combines into single AND group"""
        if isinstance(other, (FilterCondition, FilterGroup)):
            # If both are AND groups, combine their filters
            if (isinstance(self, FilterGroup) and self.operator == LogicalOperator.AND and
                isinstance(other, FilterGroup) and other.operator == LogicalOperator.AND):
                return FilterGroup(LogicalOperator.AND, self.filters + other.filters)
            # If self is AND group, add other to it
            elif isinstance(self, FilterGroup) and self.operator == LogicalOperator.AND:
                return FilterGroup(LogicalOperator.AND, self.filters + [other])
            # If other is AND group, add self to it
            elif isinstance(other, FilterGroup) and other.operator == LogicalOperator.AND:
                return FilterGroup(LogicalOperator.AND, [self] + other.filters)
            # Otherwise create new AND group
            else:
                return FilterGroup(LogicalOperator.AND, [self, other])
        return NotImplemented
    
    def __or__(self, other: Union['FilterCondition', 'FilterGroup']) -> 'FilterGroup':
        """Override | operator for OR operations"""
        if isinstance(other, (FilterCondition, FilterGroup)):
            return FilterGroup(LogicalOperator.OR, [self, other])
        return NotImplemented
    
    def __add__(self, other: Union['FilterCondition', 'FilterGroup']) -> 'FilterGroup':
        """Override + operator for AND operations (alternative syntax)"""
        return self.__and__(other)
    
    def __str__(self) -> str:
        """Human-readable string representation - uses pretty print by default"""
        return self.pretty_print()
    
    def __repr__(self) -> str:
        """Developer representation"""
        return f"FilterGroup(operator={self.operator}, filters={len(self.filters)} items)"
    
    def pretty_print(self, indent: int = 0) -> str:
        """Pretty print with indentation for complex nested filters"""
        prefix = "  " * indent
        
        if len(self.filters) == 1:
            return f"{prefix}{self.filters[0]}"
        
        lines = [f"{prefix}("]
        for i, filter_item in enumerate(self.filters):
            if isinstance(filter_item, FilterGroup):
                lines.append(filter_item.pretty_print(indent + 1))
            else:
                lines.append(f"{prefix}  {filter_item}")
            
            if i < len(self.filters) - 1:
                lines.append(f"{prefix}  {self.operator.value.upper()}")
        
        lines.append(f"{prefix})")
        return "\n".join(lines)


class BrightDataFilter:
    """
    A comprehensive search filter function for data using the BrightData API.
    
    This class provides methods to build complex filters for data across multiple datasets,
    supporting all available operators and field types from the BrightData API.
    """
    
    def __init__(self, dataset: str = "amazon_products", storage_dir: str = "snapshot_records", api_key: str = None):
        """
        Initialize the BrightData database connection.
        
        Args:
            dataset: Dataset name (e.g., 'amazon_products', 'amazon', 'shopee') or dataset ID
            storage_dir: Directory to store snapshot records (default: "snapshot_records")
            api_key: BrightData API key (optional, will load from secrets if not provided)
        """
        # Load API key from secrets if not provided
        if api_key is None:
            from .config import get_brightdata_api_key
            self.api_key = get_brightdata_api_key()
        else:
            self.api_key = api_key
        
        # Convert dataset name to ID if needed
        try:
            self.dataset_id = get_dataset_id(dataset)
        except ValueError as e:
            raise ValueError(f"Invalid dataset: {e}")
        
        self.base_url = "https://api.brightdata.com/datasets"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Setup local storage directory
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        
        # Validate dataset exists
        self.schema = get_dataset_schema(self.dataset_id)
        if not self.schema:
            raise ValueError(f"Unknown dataset ID: {self.dataset_id}. Available datasets: {self._get_available_datasets()}")
        
        # Create filter fields for this dataset
        from .filter_criteria import DatasetFilterFields
        self.filter = DatasetFilterFields(self.dataset_id)
    
    def _get_available_datasets(self) -> List[str]:
        """Get list of available dataset IDs"""
        from .dataset_registry import list_available_datasets
        return [schema.dataset_id for schema in list_available_datasets()]
    
    @classmethod
    def amazon_products(cls, storage_dir: str = "snapshot_records", api_key: str = None):
        """Convenience method to create BrightData connection for Amazon Products dataset"""
        return cls("amazon_products", storage_dir, api_key)
    
    @classmethod
    def amazon_walmart(cls, storage_dir: str = "snapshot_records", api_key: str = None):
        """Convenience method to create BrightData connection for Amazon-Walmart dataset"""
        return cls("amazon_walmart", storage_dir, api_key)
    
    @classmethod
    def shopee(cls, storage_dir: str = "snapshot_records", api_key: str = None):
        """Convenience method to create BrightData connection for Shopee dataset"""
        return cls("shopee", storage_dir, api_key)
    
    def create_filter(self, 
                     name: str, 
                     operator: Union[FilterOperator, str], 
                     value: Any = None) -> FilterCondition:
        """
        Create a single filter condition.
        
        Args:
            name: Field name to filter on
            operator: Filter operator (FilterOperator enum or string)
            value: Filter value (not required for is_null/is_not_null)
            
        Returns:
            FilterCondition object
            
        Raises:
            ValueError: If field or operator is not valid for this dataset
        """
        # Convert string operator to FilterOperator enum if needed
        if isinstance(operator, str):
            try:
                operator = FilterOperator(operator)
            except ValueError:
                raise ValueError(f"Invalid operator '{operator}'. Valid operators: {[op.value for op in FilterOperator]}")
        
        # Validate field and operator combination
        if not validate_field_operator(self.dataset_id, name, operator.value):
            available_fields = self.schema.get_field_names()
            field_def = self.schema.get_field(name)
            if not field_def:
                raise ValueError(f"Field '{name}' not found in dataset '{self.dataset_id}'. Available fields: {available_fields}")
            else:
                raise ValueError(f"Operator '{operator.value}' not supported for field '{name}'. Supported operators: {field_def.operators}")
        
        return FilterCondition(name, operator, value)
    
    def filter(self, field: str, op: str, value: Any = None) -> FilterCondition:
        """
        Convenience method to create filters with string operators.
        
        Args:
            field: Field name to filter on
            op: Operator as string (e.g., ">=", "=", "in", "array_includes")
            value: Filter value
            
        Returns:
            FilterCondition object
        """
        # Map string operators to FilterOperator enum
        op_map = {
            "=": FilterOperator.EQUAL,
            "!=": FilterOperator.NOT_EQUAL,
            "<": FilterOperator.LESS_THAN,
            "<=": FilterOperator.LESS_THAN_EQUAL,
            ">": FilterOperator.GREATER_THAN,
            ">=": FilterOperator.GREATER_THAN_EQUAL,
            "in": FilterOperator.IN,
            "not_in": FilterOperator.NOT_IN,
            "includes": FilterOperator.INCLUDES,
            "not_includes": FilterOperator.NOT_INCLUDES,
            "array_includes": FilterOperator.ARRAY_INCLUDES,
            "not_array_includes": FilterOperator.NOT_ARRAY_INCLUDES,
            "is_null": FilterOperator.IS_NULL,
            "is_not_null": FilterOperator.IS_NOT_NULL
        }
        
        if op not in op_map:
            raise ValueError(f"Unknown operator: {op}. Available: {list(op_map.keys())}")
        
        return FilterCondition(field, op_map[op], value)
    
    def create_filter_group(self, 
                           operator: LogicalOperator, 
                           filters: List[Union[FilterGroup, FilterCondition]]) -> FilterGroup:
        """
        Create a filter group with logical operator.
        
        Args:
            operator: Logical operator (AND/OR)
            filters: List of filter conditions or groups
            
        Returns:
            FilterGroup object
        """
        return FilterGroup(operator, filters)
    
    def search_data(self, 
                    filter_obj: Union[FilterCondition, FilterGroup], 
                    records_limit: int = 1000) -> Dict[str, Any]:
        """
        Execute the search with the provided filter and save local record.
        
        Args:
            filter_obj: Filter condition or group
            records_limit: Maximum number of records to return
            
        Returns:
            API response with snapshot_id and local record path
        """
        payload = {
            "dataset_id": self.dataset_id,
            "records_limit": records_limit,
            "filter": filter_obj.to_dict()
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/filter",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            api_response = response.json()
            
            # Save local record
            snapshot_id = api_response.get("snapshot_id")
            if snapshot_id:
                submission_time = datetime.now().isoformat()
                record_path = self._save_snapshot_record(snapshot_id, filter_obj, records_limit, submission_time)
                
                # Add local record info to response
                api_response["local_record_path"] = record_path
                api_response["submission_time"] = submission_time
                
                print(f"📝 Local record saved: {record_path}")
                print(f"🆔 Snapshot ID: {snapshot_id}")
                print(f"⏰ Submitted at: {submission_time}")
            
            return api_response
            
        except requests.exceptions.HTTPError as e:
            # Get the actual error response from the API
            try:
                error_details = response.json()
                error_message = f"HTTP {response.status_code}: {error_details}"
            except:
                error_message = f"HTTP {response.status_code}: {response.text}"
            raise Exception(f"API request failed: {error_message}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def _save_snapshot_record(self, snapshot_id: str, filter_obj: Union[FilterCondition, FilterGroup], 
                             records_limit: int, submission_time: str) -> str:
        """
        Save a local record of the snapshot submission.
        
        Args:
            snapshot_id: The snapshot ID from the API response
            filter_obj: The filter that was submitted
            records_limit: The records limit that was requested
            submission_time: Timestamp when the filter was submitted
            
        Returns:
            Path to the saved record file
        """
        record = {
            "snapshot_id": snapshot_id,
            "submission_time": submission_time,
            "dataset_id": self.dataset_id,
            "records_limit": records_limit,
            "filter_criteria": filter_obj.to_dict(),
            "status": "submitted",
            "metadata": None,
            "completion_time": None,
            "error": None
        }
        
        file_path = os.path.join(self.storage_dir, f"{snapshot_id}.json")
        with open(file_path, 'w') as f:
            json.dump(record, f, indent=2)
        
        return file_path
    
    def get_snapshot_metadata(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Get metadata for a snapshot to check its status and details.
        
        Args:
            snapshot_id: The snapshot ID returned from search_data()
            
        Returns:
            Snapshot metadata including status, size, cost, etc.
        """
        try:
            response = requests.get(
                f"{self.base_url}/snapshots/{snapshot_id}",
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            # Get the actual error response from the API
            try:
                error_details = response.json()
                error_message = f"HTTP {response.status_code}: {error_details}"
            except:
                error_message = f"HTTP {response.status_code}: {response.text}"
            raise Exception(f"Failed to get snapshot metadata: {error_message}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get snapshot metadata: {str(e)}")
    
    def update_snapshot_record(self, snapshot_id: str, metadata: Dict[str, Any] = None, 
                              error: str = None) -> Dict[str, Any]:
        """
        Update the local snapshot record with metadata or error information.
        
        Args:
            snapshot_id: The snapshot ID to update
            metadata: Snapshot metadata from the API
            error: Error message if the snapshot failed
            
        Returns:
            Updated record data
        """
        file_path = os.path.join(self.storage_dir, f"{snapshot_id}.json")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No local record found for snapshot {snapshot_id}")
        
        with open(file_path, 'r') as f:
            record = json.load(f)
        
        # Update record with new information
        if metadata:
            record["metadata"] = metadata
            record["status"] = metadata.get("status", "unknown")
            if metadata.get("status") in ["ready", "failed"]:
                record["completion_time"] = datetime.now().isoformat()
        
        if error:
            record["error"] = error
            record["status"] = "error"
            record["completion_time"] = datetime.now().isoformat()
        
        # Save updated record
        with open(file_path, 'w') as f:
            json.dump(record, f, indent=2)
        
        return record
    
    def wait_for_snapshot_completion(self, snapshot_id: str, max_wait_time: int = 1800, 
                                   check_interval: int = 30) -> Dict[str, Any]:
        """
        Wait for a snapshot to complete processing and return the final metadata.
        Updates the local record with progress and final results.
        
        Args:
            snapshot_id: The snapshot ID to monitor
            max_wait_time: Maximum time to wait in seconds (default: 30 minutes)
            check_interval: Time between status checks in seconds (default: 30 seconds)
            
        Returns:
            Final snapshot metadata when ready or failed
        """
        start_time = time.time()
        
        print(f"🔍 Monitoring snapshot {snapshot_id}...")
        print(f"⏰ Max wait time: {max_wait_time//60} minutes, Check interval: {check_interval} seconds")
        
        while time.time() - start_time < max_wait_time:
            try:
                metadata = self.get_snapshot_metadata(snapshot_id)
                status = metadata.get('status', 'unknown')
                
                # Update local record with current status
                self.update_snapshot_record(snapshot_id, metadata=metadata)
                
                print(f"📊 Status: {status} (elapsed: {int((time.time() - start_time)//60)}m {int((time.time() - start_time)%60)}s)")
                
                if status == 'ready':
                    dataset_size = metadata.get('dataset_size', 'N/A')
                    file_size = metadata.get('file_size', 'N/A')
                    cost = metadata.get('cost', 'N/A')
                    print(f"✅ Snapshot ready! Records: {dataset_size}, Size: {file_size} bytes, Cost: ${cost}")
                    return metadata
                elif status == 'failed':
                    error_msg = metadata.get('error', 'Unknown error')
                    print(f"❌ Snapshot failed: {error_msg}")
                    return metadata
                elif status in ['scheduled', 'building']:
                    print(f"⏳ Processing... waiting {check_interval}s...")
                    time.sleep(check_interval)
                else:
                    print(f"⚠️ Unknown status: {status}")
                    time.sleep(check_interval)
                    
            except Exception as e:
                print(f"⚠️ Error checking status: {e}")
                time.sleep(check_interval)
        
        print(f"⏰ Timeout reached ({max_wait_time//60} minutes). Final status:")
        try:
            final_metadata = self.get_snapshot_metadata(snapshot_id)
            self.update_snapshot_record(snapshot_id, metadata=final_metadata)
            return final_metadata
        except Exception as e:
            self.update_snapshot_record(snapshot_id, error=str(e))
            raise e
    
    def get_snapshot_record(self, snapshot_id: str) -> Dict[str, Any]:
        """
        Get the local record for a snapshot.
        
        Args:
            snapshot_id: The snapshot ID to retrieve
            
        Returns:
            Local record data
        """
        file_path = os.path.join(self.storage_dir, f"{snapshot_id}.json")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"No local record found for snapshot {snapshot_id}")
        
        with open(file_path, 'r') as f:
            return json.load(f)
    
    def list_snapshot_records(self) -> List[Dict[str, Any]]:
        """
        List all local snapshot records.
        
        Returns:
            List of snapshot records with basic info
        """
        records = []
        
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                snapshot_id = filename[:-5]  # Remove .json extension
                try:
                    record = self.get_snapshot_record(snapshot_id)
                    records.append({
                        "snapshot_id": snapshot_id,
                        "submission_time": record.get("submission_time"),
                        "status": record.get("status"),
                        "dataset_id": record.get("dataset_id"),
                        "records_limit": record.get("records_limit"),
                        "completion_time": record.get("completion_time")
                    })
                except Exception as e:
                    print(f"⚠️ Error reading record {filename}: {e}")
        
        # Sort by submission time (newest first)
        records.sort(key=lambda x: x.get("submission_time", ""), reverse=True)
        return records
    
    def get_field_reference(self) -> Dict[str, str]:
        """Quick reference for available fields in this dataset"""
        return {
            field_name: field.description 
            for field_name, field in self.schema.fields.items()
        }
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Get information about the current dataset"""
        return {
            "dataset_id": self.schema.dataset_id,
            "name": self.schema.name,
            "description": self.schema.description,
            "field_count": len(self.schema.fields),
            "available_fields": self.schema.get_field_names()
        }
    
    @staticmethod
    def list_available_datasets(include_names: bool = False) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """
        List all available datasets with optional name mappings
        
        Args:
            include_names: If True, includes dataset name mappings and comprehensive info
            
        Returns:
            List of dataset info dicts, or comprehensive dict if include_names=True
        """
        from .dataset_registry import list_available_datasets
        
        if include_names:
            # Return comprehensive information
            comprehensive = list_available_datasets(include_names=True)
            
            # Add formatted dataset info
            formatted_datasets = []
            for schema in comprehensive["schemas"]:
                formatted_datasets.append({
                    "dataset_id": schema.dataset_id,
                    "name": schema.name,
                    "description": schema.description,
                    "field_count": len(schema.fields),
                    "available_aliases": [
                        name for name, dataset_id in comprehensive["names"].items() 
                        if dataset_id == schema.dataset_id
                    ]
                })
            
            return {
                "datasets": formatted_datasets,
                "names": comprehensive["names"],
                "summary": comprehensive["summary"]
            }
        else:
            # Return simple list
            datasets = list_available_datasets()
            return [
                {
                    "dataset_id": schema.dataset_id,
                    "name": schema.name,
                    "description": schema.description,
                    "field_count": len(schema.fields)
                }
                for schema in datasets
            ]


# Utility functions for filter management
def export_filter_to_json(filter_obj: Union[FilterCondition, FilterGroup], 
                         filename: str = "filter_config.json") -> None:
    """
    Export a filter configuration to JSON file.
    
    Args:
        filter_obj: Filter condition or group to export
        filename: Output filename
    """
    with open(filename, 'w') as f:
        json.dump(filter_obj.to_dict(), f, indent=2)
    print(f"Filter configuration exported to {filename}")


def load_filter_from_json(filename: str) -> Dict[str, Any]:
    """
    Load a filter configuration from JSON file.
    
    Args:
        filename: Input filename
        
    Returns:
        Filter configuration dictionary
    """
    with open(filename, 'r') as f:
        return json.load(f)


def analyze_filter_results(snapshot_id: str, api_key: str) -> Dict[str, Any]:
    """
    Analyze the results from a filter query.
    
    Args:
        snapshot_id: Snapshot ID from the filter API response
        api_key: Bright Data API key
        
    Returns:
        Analysis results
    """
    # This would typically involve downloading and analyzing the snapshot data
    # For now, return a placeholder structure
    return {
        "snapshot_id": snapshot_id,
        "analysis": "Results analysis would be implemented here",
        "recommendations": "Product recommendations based on analysis"
    }
