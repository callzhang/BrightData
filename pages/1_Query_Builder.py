#!/usr/bin/env python3
"""
Query Builder Page - Create and submit data queries

This page allows users to select datasets, build complex filters,
and submit queries to the BrightData API.
"""

import streamlit as st
import json
import sys
from pathlib import Path
from datetime import datetime

# Add the util directory to the path
sys.path.append(str(Path(__file__).parent.parent / "util"))

try:
    from util import BrightDataFilter, FilterCondition, FilterGroup, FilterOperator, LogicalOperator
    from util.config import get_brightdata_api_key
    from util.dataset_registry import dataset_registry
except ImportError as e:
    st.error(f"❌ Could not import utilities: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Query Builder - BrightData Manager",
    page_icon="🔍",
    layout="wide"
)

def main():
    """Main query builder interface"""
    
    st.title("🔍 Query Builder")
    st.markdown("Build and submit data queries to BrightData datasets")
    
    # Initialize session state
    if 'filter_structure' not in st.session_state:
        st.session_state.filter_structure = {
            'type': 'group',
            'operator': 'AND',
            'filters': []
        }
    if 'selected_dataset' not in st.session_state:
        st.session_state.selected_dataset = None
    if 'query_result' not in st.session_state:
        st.session_state.query_result = None
    
    # Dataset selection
    st.header("📊 Dataset Selection")
    
    try:
        # Get available datasets from registry
        available_datasets = dataset_registry.list_datasets()
        if not available_datasets:
            st.error("❌ No datasets available. Please check your configuration.")
            return
        
        # Create display names for the selectbox
        dataset_choices = {schema.name: schema for schema in available_datasets}
        
        selected_dataset_display_name = st.selectbox(
            "Choose a dataset:",
            options=list(dataset_choices.keys()),
            index=0,
            help="Select the dataset you want to query"
        )
        
        # Get dataset configuration
        dataset_config = dataset_choices[selected_dataset_display_name]
        if not dataset_config:
            st.error(f"❌ Dataset configuration not found: {selected_dataset_display_name}")
            return
        
        st.session_state.selected_dataset = dataset_config
        
        # Display dataset info
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **Dataset ID:** `{dataset_config.dataset_id}`  
            **Description:** {dataset_config.description}  
            **Fields Available:** {len(dataset_config.fields)}
            """)
        
        with col2:
            st.success(f"""
            **Name:** {dataset_config.name}  
            **Total Fields:** {len(dataset_config.fields)}  
            **Status:** ✅ Ready for querying
            """)
        
    except Exception as e:
        st.error(f"❌ Error loading datasets: {e}")
        return
    
    st.divider()
    
    # Filter builder
    st.header("🔧 Advanced Filter Builder")
    st.markdown("Create nested filter groups with AND/OR logic")
    
    # Filter structure controls
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("➕ Add Condition", type="primary"):
            st.session_state.filter_structure['filters'].append({
                'type': 'condition',
                'field': '',
                'operator': '=',
                'value': ''
            })
            st.rerun()
    
    with col2:
        if st.button("📦 Add Group"):
            st.session_state.filter_structure['filters'].append({
                'type': 'group',
                'operator': 'AND',
                'filters': []
            })
            st.rerun()
    
    with col3:
        if st.session_state.filter_structure['filters']:
            st.info(f"📋 {len(st.session_state.filter_structure['filters'])} item(s) in root group")
        else:
            st.warning("⚠️ No filters added yet")
    
    # Display filter structure
    def render_filter_item(item, path="", level=0):
        """Recursively render filter items"""
        indent = "  " * level
        
        if item['type'] == 'condition':
            # Ultra-compact condition layout
            # Field and operator in one row with right-aligned X button
            col1, col2, col3, col4, col5 = st.columns([2, 1, 2, 1, 0.3])
            
            with col1:
                # Field selection with detailed descriptions
                field_choices = {}
                for field_name, field in dataset_config.fields.items():
                    # Create detailed field description
                    field_desc = f"{field_name} ({field.field_type.value})"
                    if field.description:
                        field_desc += f" - {field.description}"
                    field_choices[field_desc] = field_name
                
                field_options = list(field_choices.keys())
                
                # Find the current field index first
                current_field = item.get('field', '')
                try:
                    current_index = next(i for i, k in enumerate(field_options) if field_choices[k] == current_field)
                except StopIteration:
                    current_index = 0
                
                # Get field description for help text
                selected_field_name = field_choices.get(field_options[current_index] if current_index < len(field_options) else field_options[0], "")
                field_description = dataset_config.fields.get(selected_field_name, {}).description if selected_field_name else ""
                
                field_key = st.selectbox(
                    "Field:",
                    options=field_options,
                    index=current_index,
                    key=f"field_{path}",
                    help=f"Select the field to filter on{f': {field_description}' if field_description else ''}"
                )
                item['field'] = field_choices[field_key]
            
            with col2:
                # Operator selection with detailed help
                operators = ['=', '!=', '<', '<=', '>', '>=', 'includes', 'not_includes', 'in', 'not_in']
                current_operator = item.get('operator', '=')
                try:
                    operator_index = operators.index(current_operator)
                except ValueError:
                    operator_index = 0
                
                # Create detailed operator help text
                operator_help = """
**Comparison Operators:**

**Equality:**
• `=` - Exact match (e.g., name = "John")
• `!=` - Not equal (e.g., status != "inactive")

**Numeric/Date Comparisons:**
• `<` - Less than (e.g., age < 25, date < "2023-01-01")
• `<=` - Less than or equal (e.g., price <= 100)
• `>` - Greater than (e.g., rating > 4.0)
• `>=` - Greater than or equal (e.g., score >= 80)

**Text/Array Operations:**
• `includes` - Contains text (e.g., description includes "software")
• `not_includes` - Does not contain (e.g., title not_includes "test")
• `in` - Value in list (e.g., category in ["tech", "business"])
• `not_in` - Value not in list (e.g., status not_in ["closed", "cancelled"])

**Examples:**
• For text: `name = "John"` or `title includes "manager"`
• For numbers: `age > 25` or `price <= 100`
• For categories: `status in ["active", "pending"]`
                """
                
                operator = st.selectbox(
                    "Op:",
                    options=operators,
                    index=operator_index,
                    key=f"operator_{path}",
                    help=operator_help
                )
                item['operator'] = operator
            
            with col3:
                # Value input with field-specific help
                selected_field_name = field_choices.get(field_options[current_index] if current_index < len(field_options) else field_options[0], "")
                field_config = dataset_config.fields.get(selected_field_name)
                
                # Create field-specific help text
                if field_config:
                    field_type = field_config.field_type.value
                    if field_type == 'string':
                        value_help = f"""
**Text Value Examples:**
• Exact match: `"John Smith"`
• Partial match: `"software"` (use includes operator)
• Multiple values: `["tech", "business"]` (use in operator)
• Case-sensitive matching
                        """
                    elif field_type == 'numeric':
                        value_help = f"""
**Numeric Value Examples:**
• Single value: `25`, `100.50`
• Comparisons: `> 50`, `<= 1000`
• Ranges: Use multiple conditions
• No quotes needed for numbers
                        """
                    elif field_type == 'boolean':
                        value_help = f"""
**Boolean Value Examples:**
• `true` or `false`
• `1` or `0`
• `yes` or `no`
• Case-insensitive
                        """
                    else:
                        value_help = f"""
**Value Examples for {field_type}:**
• Enter the exact value to match
• Use quotes for text: `"value"`
• No quotes for numbers: `123`
• For lists: `["item1", "item2"]`
                        """
                else:
                    value_help = "Enter the value to compare against"
                
                value = st.text_input(
                    "Value:",
                    value=item.get('value', ''),
                    key=f"value_{path}",
                    help=value_help
                )
                item['value'] = value
            
            with col4:
                # Empty space for alignment
                st.write("")
            
            with col5:
                # Right-aligned X button
                st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
                if st.button("❌", key=f"remove_{path}", help="Remove this condition"):
                    # Find and remove from parent
                    parent = st.session_state.filter_structure
                    for i, filter_item in enumerate(parent['filters']):
                        if filter_item == item:
                            parent['filters'].pop(i)
                            break
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
            
            # No separator needed - conditions flow naturally
        
        elif item['type'] == 'group':
            with st.expander(f"{indent}📦 Group ({item['operator']})", expanded=True):
                # Group controls in a more compact layout
                col1, _, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1, 0.5])
                
                with col1:
                    current_operator = item.get('operator', 'AND')
                    operator_index = 0 if current_operator == 'AND' else 1
                    
                    operator = st.selectbox(
                        "Logic:",
                        options=['AND', 'OR'],
                        index=operator_index,
                        key=f"group_operator_{path}",
                        label_visibility="collapsed",
                        help="How ALL items in this group are combined"
                    )
                    item['operator'] = operator
                
                with col2:
                    if st.button("➕ Condition", key=f"add_condition_{path}", help="Add a condition to this group"):
                        item['filters'].append({
                            'type': 'condition',
                            'field': '',
                            'operator': '=',
                            'value': ''
                        })
                        st.rerun()
                
                with col3:
                    if st.button("📦 Subgroup", key=f"add_subgroup_{path}", help="Add a subgroup to this group"):
                        item['filters'].append({
                            'type': 'group',
                            'operator': 'AND',
                            'filters': []
                        })
                        st.rerun()
                
                with col4:
                    # Empty space for alignment
                    st.write("")
                
                with col5:
                    # Right-aligned X button (only for non-root groups)
                    if path != "":  # Don't show delete for root group
                        if st.button("❌", key=f"remove_group_{path}", help="Remove this group"):
                            # Find and remove from parent
                            parent = st.session_state.filter_structure
                            for i, filter_item in enumerate(parent['filters']):
                                if filter_item == item:
                                    parent['filters'].pop(i)
                                    break
                            st.rerun()
                
                # Show group logic explanation
                # st.caption(f"💡 All items in this group will be combined with {item['operator']}")
                
                # Render nested items
                if item['filters']:
                    for i, nested_item in enumerate(item['filters']):
                        render_filter_item(nested_item, f"{path}_{i}", level + 1)
                else:
                    st.info("ℹ️ Add conditions or subgroups to this group")
    
    # Render the filter structure
    if st.session_state.filter_structure['filters']:
        st.subheader("🏗️ Filter Structure")
        for i, item in enumerate(st.session_state.filter_structure['filters']):
            render_filter_item(item, str(i))
    else:
        st.info("ℹ️ Add conditions or groups to build your filter")
    
    st.divider()
    
    # Query preview and submission
    st.header("📋 Query Preview")
    
    def build_filter_from_structure(structure):
        """Recursively build filter objects from the nested structure"""
        if structure['type'] == 'condition':
            if not structure.get('field') or not structure.get('value'):
                return None
            
            field_name = structure['field']
            operator = structure['operator']
            value = structure['value']
            
            # Convert value based on field type
            field_config = dataset_config.fields.get(field_name)
            if field_config and field_config.field_type.value == 'numeric':
                try:
                    value = float(value)
                except ValueError:
                    st.warning(f"⚠️ Invalid numeric value for {field_name}: {value}")
                    return None
            elif field_config and field_config.field_type.value == 'boolean':
                value = value.lower() in ['true', '1', 'yes', 'on']
            
            # Create condition based on operator
            if operator == '=':
                return FilterCondition(field_name, FilterOperator.EQUAL, value)
            elif operator == '!=':
                return FilterCondition(field_name, FilterOperator.NOT_EQUAL, value)
            elif operator == '<':
                return FilterCondition(field_name, FilterOperator.LESS_THAN, value)
            elif operator == '<=':
                return FilterCondition(field_name, FilterOperator.LESS_THAN_EQUAL, value)
            elif operator == '>':
                return FilterCondition(field_name, FilterOperator.GREATER_THAN, value)
            elif operator == '>=':
                return FilterCondition(field_name, FilterOperator.GREATER_THAN_EQUAL, value)
            elif operator == 'includes':
                return FilterCondition(field_name, FilterOperator.INCLUDES, value)
            elif operator == 'not_includes':
                return FilterCondition(field_name, FilterOperator.NOT_INCLUDES, value)
            elif operator == 'in':
                values = [v.strip() for v in value.split(',')]
                return FilterCondition(field_name, FilterOperator.IN, values)
            elif operator == 'not_in':
                values = [v.strip() for v in value.split(',')]
                return FilterCondition(field_name, FilterOperator.NOT_IN, values)
            else:
                st.warning(f"⚠️ Unsupported operator: {operator}")
                return None
        
        elif structure['type'] == 'group':
            # Build filters for this group
            group_filters = []
            for item in structure['filters']:
                built_filter = build_filter_from_structure(item)
                if built_filter:
                    group_filters.append(built_filter)
            
            if not group_filters:
                return None
            elif len(group_filters) == 1:
                return group_filters[0]
            else:
                # Create group with the specified logical operator
                logical_op = LogicalOperator.AND if structure['operator'] == 'AND' else LogicalOperator.OR
                return FilterGroup(logical_op, group_filters)
        
        return None
    
    if st.session_state.filter_structure['filters']:
        # Build filter object from nested structure
        try:
            filter_obj = build_filter_from_structure(st.session_state.filter_structure)
            
            if filter_obj:
                # Display query preview
                st.subheader("🔍 Query Preview")
                st.json({
                    "dataset": dataset_config.name,
                    "dataset_id": dataset_config.dataset_id,
                    "filter_structure": str(filter_obj),
                    "filter_type": type(filter_obj).__name__
                })
                
                # Title and description inputs
                st.subheader("📝 Query Details")
                query_title = st.text_input(
                    "Query Title *",
                    placeholder="Enter a descriptive title for your query...",
                    help="This title will help you identify the query in the Snapshot Viewer",
                    key="query_title"
                )
                
                if not query_title.strip():
                    st.warning("⚠️ Please enter a title for your query")
                    st.stop()
                
                # Description input (optional)
                query_description = st.text_area(
                    "Query Description",
                    placeholder="Describe what this query is looking for, its purpose, or any notes...",
                    help="Optional description to help you remember what this query does",
                    key="query_description"
                )
                
                # Records limit input
                col_limit1, col_limit2 = st.columns([1, 1])
                
                with col_limit1:
                    records_limit = st.number_input(
                        "Records Limit",
                        min_value=1,
                        max_value=10000,
                        value=1000,
                        step=100,
                        help="Maximum number of records to retrieve (1-10,000)",
                        key="records_limit"
                    )
                
                with col_limit2:
                    # Show estimated cost
                    estimated_cost = records_limit * 0.002
                    st.metric(
                        "Estimated Cost",
                        f"${estimated_cost:.4f}",
                        help=f"${0.002:.3f} per record × {records_limit:,} records"
                    )
                
                # Submit button
                col1, col2, col3 = st.columns([1, 2, 1])
                with col2:
                    if st.button("🚀 Submit Query", type="primary", use_container_width=True):
                        with st.spinner("Submitting query to BrightData API..."):
                            try:
                                # Initialize BrightData filter with correct storage directory
                                brightdata = BrightDataFilter(dataset_config.dataset_id, storage_dir="data/snapshots")
                                
                                # Submit query
                                snapshot_id = brightdata.search_data(
                                    filter_obj=filter_obj,
                                    records_limit=records_limit,
                                    description=query_description.strip() if query_description.strip() else f"Nested query with {st.session_state.filter_structure['operator']} logic",
                                    title=query_title.strip()
                                )
                                
                                st.session_state.query_result = {
                                    'snapshot_id': snapshot_id,
                                    'dataset': dataset_config.name,
                                    'filter_type': 'nested',
                                    'timestamp': datetime.now().isoformat()
                                }
                                
                                st.success(f"✅ Query submitted successfully!")
                                st.info(f"📊 Snapshot ID: `{snapshot_id}`")
                                st.info(f"📝 Title: {query_title.strip()}")
                                if query_description.strip():
                                    st.info(f"📄 Description: {query_description.strip()}")
                                st.info(f"📈 Records Limit: {records_limit:,}")
                                st.info(f"💰 Estimated Cost: ${estimated_cost:.4f}")
                                st.info("💡 Go to Snapshot Viewer to monitor progress and download results")
                                
                            except Exception as e:
                                st.error(f"❌ Query submission failed: {e}")
                                st.error("💡 Check your API key in Settings and try again")
            else:
                st.warning("⚠️ No valid filters configured. Please add at least one filter with a field and value.")
        
        except Exception as e:
            st.error(f"❌ Error building query: {e}")
    
    else:
        st.info("ℹ️ Add filters above to build your query")
    
    # Show recent results
    if st.session_state.query_result:
        st.divider()
        st.header("📊 Recent Query Results")
        
        result = st.session_state.query_result
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Safely handle snapshot_id (could be string or other type)
            snapshot_id = str(result.get('snapshot_id', 'Unknown'))
            display_id = snapshot_id[:20] + "..." if len(snapshot_id) > 20 else snapshot_id
            st.metric("Snapshot ID", display_id)
        
        with col2:
            st.metric("Dataset", result.get('dataset', 'Unknown'))
        
        with col3:
            st.metric("Filters", result.get('filters_count', result.get('filter_type', 'Unknown')))
        
        st.info(f"⏰ Submitted at: {result.get('timestamp', 'Unknown time')}")
        
        if st.button("🔄 Submit Another Query"):
            st.session_state.query_result = None
            st.rerun()

if __name__ == "__main__":
    main()
