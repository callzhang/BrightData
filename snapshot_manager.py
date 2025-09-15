#!/usr/bin/env python3
"""
Snapshot Manager - Local BrightData Snapshot Management Utility

This script provides a comprehensive interface for managing local snapshot records:
- View all snapshot records and their status
- Check current status from BrightData API
- Initiate downloads for ready snapshots
- View downloaded data locally
- Monitor progress of processing snapshots

Usage:
    python snapshot_manager.py [options]
    
Options:
    --list, -l          List all snapshot records
    --status, -s        Check status of all snapshots
    --download, -d      Download ready snapshots
    --view, -v          View downloaded data
    --monitor, -m       Monitor processing snapshots
    --help, -h          Show this help message
"""

import os
import json
import sys
import argparse
import requests
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add util to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from util import BrightDataFilter, get_brightdata_api_key


class SnapshotManager:
    """Manages local snapshot records and BrightData API interactions"""
    
    def __init__(self, storage_dir: str = "snapshot_records"):
        """
        Initialize the snapshot manager
        
        Args:
            storage_dir: Directory containing snapshot records
        """
        self.storage_dir = Path(storage_dir)
        self.api_key = get_brightdata_api_key()
        
        if not self.storage_dir.exists():
            print(f"❌ Storage directory '{storage_dir}' not found")
            print("💡 Run some filters first to create snapshot records")
            sys.exit(1)
    
    def list_records(self) -> List[Dict[str, Any]]:
        """List all local snapshot records"""
        records = []
        
        for json_file in self.storage_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    record = json.load(f)
                
                metadata = record.get("metadata") or {}
                records.append({
                    "snapshot_id": record.get("snapshot_id"),
                    "submission_time": record.get("submission_time"),
                    "status": record.get("status"),
                    "dataset_id": record.get("dataset_id"),
                    "records_limit": record.get("records_limit"),
                    "completion_time": record.get("completion_time"),
                    "cost": metadata.get("cost", "N/A"),
                    "file_path": str(json_file)
                })
            except Exception as e:
                print(f"⚠️ Error reading {json_file}: {e}")
        
        # Sort by submission time (newest first)
        records.sort(key=lambda x: x.get("submission_time", ""), reverse=True)
        return records
    
    def print_records_table(self, records: List[Dict[str, Any]]):
        """Print records in a formatted table"""
        if not records:
            print("📭 No snapshot records found")
            return
        
        print(f"\n📊 Found {len(records)} snapshot records:")
        print("=" * 120)
        print(f"{'Snapshot ID':<20} {'Status':<12} {'Dataset':<20} {'Limit':<8} {'Cost':<8} {'Submitted':<20}")
        print("=" * 120)
        
        for record in records:
            snapshot_id = record["snapshot_id"][:18] + "..." if len(record["snapshot_id"]) > 18 else record["snapshot_id"]
            status = record["status"]
            dataset_id = record["dataset_id"][:18] + "..." if len(record["dataset_id"]) > 18 else record["dataset_id"]
            limit = str(record["records_limit"])
            cost = f"${record['cost']}" if record["cost"] != "N/A" else "N/A"
            submitted = record["submission_time"][:19] if record["submission_time"] else "N/A"
            
            # Color coding for status
            status_colors = {
                "ready": "✅",
                "failed": "❌", 
                "scheduled": "⏳",
                "building": "🔨",
                "submitted": "📤"
            }
            status_icon = status_colors.get(status, "❓")
            
            print(f"{snapshot_id:<20} {status_icon} {status:<10} {dataset_id:<20} {limit:<8} {cost:<8} {submitted:<20}")
        
        print("=" * 120)
    
    def check_status(self, snapshot_id: str) -> Dict[str, Any]:
        """Check current status of a snapshot from BrightData API"""
        try:
            # Get dataset ID from local record
            record_path = self.storage_dir / f"{snapshot_id}.json"
            if not record_path.exists():
                raise FileNotFoundError(f"No local record for {snapshot_id}")
            
            with open(record_path, 'r') as f:
                record = json.load(f)
            
            dataset_id = record["dataset_id"]
            
            # Initialize filter for API calls
            filter_obj = BrightDataFilter(dataset_id, str(self.storage_dir), self.api_key)
            
            # Get current metadata
            metadata = filter_obj.get_snapshot_metadata(snapshot_id)
            
            # Update local record
            filter_obj.update_snapshot_record(snapshot_id, metadata=metadata)
            
            return metadata
            
        except Exception as e:
            return {"error": str(e)}
    
    def check_all_status(self):
        """Check status of all snapshots"""
        records = self.list_records()
        
        print(f"\n🔍 Checking status of {len(records)} snapshots...")
        
        for i, record in enumerate(records, 1):
            snapshot_id = record["snapshot_id"]
            print(f"\n[{i}/{len(records)}] Checking {snapshot_id}...")
            
            metadata = self.check_status(snapshot_id)
            
            if "error" in metadata:
                print(f"❌ Error: {metadata['error']}")
            else:
                status = metadata.get("status", "unknown")
                cost = metadata.get("cost", "N/A")
                dataset_size = metadata.get("dataset_size", "N/A")
                file_size = metadata.get("file_size", "N/A")
                
                print(f"📊 Status: {status}")
                print(f"💰 Cost: ${cost}")
                print(f"📈 Records: {dataset_size}")
                print(f"💾 Size: {file_size} bytes")
                
                if status == "ready":
                    print("✅ Ready for download!")
                elif status == "failed":
                    print(f"❌ Failed: {metadata.get('error', 'Unknown error')}")
                elif status in ["scheduled", "building"]:
                    print("⏳ Still processing...")
    
    def download_snapshot(self, snapshot_id: str, output_dir: str = "downloads") -> bool:
        """
        Download a ready snapshot
        
        Args:
            snapshot_id: Snapshot ID to download
            output_dir: Directory to save downloaded files
            
        Returns:
            True if download successful, False otherwise
        """
        try:
            # Check if snapshot is ready
            metadata = self.check_status(snapshot_id)
            
            if "error" in metadata:
                print(f"❌ Error checking status: {metadata['error']}")
                return False
            
            if metadata.get("status") != "ready":
                print(f"❌ Snapshot not ready. Status: {metadata.get('status')}")
                return False
            
            # Get download URL from metadata
            download_url = metadata.get("download_url")
            if not download_url:
                print("📤 No download URL available, attempting to deliver snapshot...")
                
                # Get dataset_id from local record
                record_path = self.storage_dir / f"{snapshot_id}.json"
                if not record_path.exists():
                    print(f"❌ No local record found for {snapshot_id}")
                    return False
                
                with open(record_path, 'r') as f:
                    record = json.load(f)
                
                dataset_id = record["dataset_id"]
                
                # Try to deliver the snapshot with a webhook configuration
                # This will trigger the delivery process
                try:
                    delivery_config = {
                        "deliver": {
                            "type": "webhook",
                            "filename": {
                                "template": f"snapshot_{snapshot_id}",
                                "extension": "json"
                            },
                            "endpoint": "https://httpbin.org/post"  # Temporary endpoint for testing
                        },
                        "compress": False
                    }
                    
                    # Initialize filter for API calls
                    filter_obj = BrightDataFilter(dataset_id, str(self.storage_dir), self.api_key)
                    delivery_result = filter_obj.deliver_snapshot(snapshot_id, delivery_config)
                    
                    print(f"✅ Delivery initiated: {delivery_result}")
                    print("⏳ Please wait for delivery to complete, then try downloading again")
                    return False
                    
                except Exception as e:
                    print(f"❌ Failed to initiate delivery: {e}")
                    return False
            
            # Create output directory
            output_path = Path(output_dir)
            output_path.mkdir(exist_ok=True)
            
            # Download file
            print(f"📥 Downloading {snapshot_id}...")
            response = requests.get(download_url, stream=True)
            response.raise_for_status()
            
            # Determine file extension
            content_type = response.headers.get('content-type', '')
            if 'json' in content_type:
                ext = '.json'
            elif 'csv' in content_type:
                ext = '.csv'
            elif 'zip' in content_type:
                ext = '.zip'
            else:
                ext = '.dat'
            
            # Save file
            filename = f"{snapshot_id}{ext}"
            file_path = output_path / filename
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"✅ Downloaded to: {file_path}")
            
            # Update local record with download info
            record_path = self.storage_dir / f"{snapshot_id}.json"
            with open(record_path, 'r') as f:
                record = json.load(f)
            
            record["downloaded_file"] = str(file_path)
            record["download_time"] = datetime.now().isoformat()
            
            with open(record_path, 'w') as f:
                json.dump(record, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def download_ready_snapshots(self, output_dir: str = "downloads"):
        """Download all ready snapshots"""
        records = self.list_records()
        ready_snapshots = [r for r in records if r["status"] == "ready"]
        
        if not ready_snapshots:
            print("📭 No ready snapshots to download")
            return
        
        print(f"📥 Found {len(ready_snapshots)} ready snapshots")
        
        for record in ready_snapshots:
            snapshot_id = record["snapshot_id"]
            print(f"\n--- Downloading {snapshot_id} ---")
            self.download_snapshot(snapshot_id, output_dir)
    
    def view_downloaded_data(self, snapshot_id: str, max_lines: int = 20):
        """View downloaded data for a snapshot"""
        record_path = self.storage_dir / f"{snapshot_id}.json"
        
        if not record_path.exists():
            print(f"❌ No record found for {snapshot_id}")
            return
        
        with open(record_path, 'r') as f:
            record = json.load(f)
        
        downloaded_file = record.get("downloaded_file")
        if not downloaded_file:
            print(f"❌ No downloaded file for {snapshot_id}")
            return
        
        file_path = Path(downloaded_file)
        if not file_path.exists():
            print(f"❌ Downloaded file not found: {file_path}")
            return
        
        print(f"📄 Viewing {file_path} (first {max_lines} lines):")
        print("=" * 80)
        
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r') as f:
                    data = json.load(f)
                print(json.dumps(data, indent=2)[:2000] + "..." if len(str(data)) > 2000 else json.dumps(data, indent=2))
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f):
                        if i >= max_lines:
                            print("...")
                            break
                        print(line.rstrip())
        except Exception as e:
            print(f"❌ Error reading file: {e}")
    
    def monitor_processing(self, check_interval: int = 30):
        """Monitor all processing snapshots"""
        records = self.list_records()
        processing = [r for r in records if r["status"] in ["scheduled", "building", "submitted"]]
        
        if not processing:
            print("📭 No snapshots currently processing")
            return
        
        print(f"🔍 Monitoring {len(processing)} processing snapshots...")
        print("Press Ctrl+C to stop monitoring")
        
        try:
            while True:
                print(f"\n⏰ {datetime.now().strftime('%H:%M:%S')} - Checking status...")
                
                for record in processing:
                    snapshot_id = record["snapshot_id"]
                    metadata = self.check_status(snapshot_id)
                    
                    if "error" not in metadata:
                        status = metadata.get("status", "unknown")
                        print(f"  {snapshot_id}: {status}")
                        
                        if status == "ready":
                            print(f"    ✅ {snapshot_id} is ready for download!")
                        elif status == "failed":
                            print(f"    ❌ {snapshot_id} failed")
                
                print(f"⏳ Waiting {check_interval} seconds...")
                import time
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Monitoring stopped")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="BrightData Snapshot Manager")
    parser.add_argument("--list", "-l", action="store_true", help="List all snapshot records")
    parser.add_argument("--status", "-s", action="store_true", help="Check status of all snapshots")
    parser.add_argument("--download", "-d", action="store_true", help="Download ready snapshots")
    parser.add_argument("--view", "-v", type=str, help="View downloaded data for snapshot ID")
    parser.add_argument("--monitor", "-m", action="store_true", help="Monitor processing snapshots")
    parser.add_argument("--storage-dir", type=str, default="snapshot_records", help="Storage directory for records")
    parser.add_argument("--output-dir", type=str, default="downloads", help="Output directory for downloads")
    parser.add_argument("--lines", type=int, default=20, help="Number of lines to show when viewing data")
    
    args = parser.parse_args()
    
    # Initialize manager
    try:
        manager = SnapshotManager(args.storage_dir)
    except SystemExit:
        return
    
    # Execute requested actions
    if args.list:
        records = manager.list_records()
        manager.print_records_table(records)
    
    if args.status:
        manager.check_all_status()
    
    if args.download:
        manager.download_ready_snapshots(args.output_dir)
    
    if args.view:
        manager.view_downloaded_data(args.view, args.lines)
    
    if args.monitor:
        manager.monitor_processing()
    
    # If no arguments provided, show help
    if not any([args.list, args.status, args.download, args.view, args.monitor]):
        parser.print_help()
        print("\n💡 Quick start:")
        print("  python snapshot_manager.py --list    # List all snapshots")
        print("  python snapshot_manager.py --status  # Check all statuses")
        print("  python snapshot_manager.py --download # Download ready snapshots")


if __name__ == "__main__":
    main()
