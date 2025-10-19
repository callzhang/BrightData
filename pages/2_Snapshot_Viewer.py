#!/usr/bin/env python3
"""
BrightData Snapshot Viewer - Simple Web UI
A Streamlit application for viewing and operating on locally stored snapshots.
"""

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os
from datetime import datetime
import time
import requests
import sys

# Add the util directory to the path
sys.path.append(str(Path(__file__).parent.parent / "util"))

try:
    from util import BrightDataFilter
    from util.config import get_brightdata_api_key
except ImportError:
    st.error("❌ Could not import BrightData utilities. Make sure you're running from the project root.")
    st.stop()

@st.dialog("⚠️ Download Confirmation")
def download_snapshot_dialog(snapshot_id, selected_record, download_format):
    """Download confirmation dialog using proper st.dialog decorator."""
    st.warning("**You are about to download snapshot data that will incur costs.**")
    
    # Get record count for cost calculation
    records_limit = selected_record.get('records_limit', 1000)
    estimated_cost = records_limit * 0.002
    
    # Display download details
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Snapshot ID**: `{snapshot_id}`")
        st.write(f"**Format**: {download_format.upper()}")
    with col2:
        st.write(f"**Estimated Records**: {records_limit:,}")
        st.write(f"**Estimated Cost**: ${estimated_cost:.4f}")
    
    st.write("**Price**: $0.002 per record")
    st.divider()
    
    # Confirmation buttons
    col_confirm, col_cancel = st.columns(2)
    
    with col_confirm:
        if st.button("✅ Confirm Download", type="primary", use_container_width=True):
            # Close dialog
            st.session_state[f'show_download_dialog_{snapshot_id}'] = False
            
            # Proceed with download
            download_snapshot_id = snapshot_id
            compress_data = False  # Default to no compression
            
            # Additional validation
            if not download_snapshot_id.startswith('snap_'):
                st.error("❌ Invalid snapshot ID format")
                st.info("💡 Snapshot ID should start with 'snap_'")
                return
            
            # Initialize BrightData filter
            dataset_id = selected_record.get('dataset_id')
            if not dataset_id:
                st.error("❌ No dataset ID found in record")
                return
            
            brightdata = BrightDataFilter(dataset_id)
            
            # Check snapshot status before attempting download
            try:
                metadata = brightdata.get_snapshot_metadata(snapshot_id)
                if metadata and metadata.get('status') not in ['completed', 'ready']:
                    st.warning(f"⚠️ Snapshot status: {metadata.get('status', 'unknown')}")
                    st.info("💡 The snapshot may not be ready for download yet. Please wait and try again later.")
                    return
            except Exception as e:
                st.warning(f"⚠️ Could not check snapshot status: {e}")
                st.info("💡 Proceeding with download attempt...")
            
            # Show download progress
            with st.spinner(f"Downloading {download_snapshot_id} in {download_format.upper()} format..."):
                # Download the snapshot content with retry logic for 202 responses
                max_retries = 2
                retry_delay = 5  # seconds
                
                for attempt in range(max_retries + 1):
                    response = brightdata.download_snapshot_content(
                        download_snapshot_id,
                        format=download_format,
                        compress=compress_data
                    )
                    
                    if response.status_code == 200:
                        # Check if the response contains actual data or a status message
                        content = response.text.strip()
                        
                        # Check for status messages
                        if content in ["Snapshot is building. Try again in a few minutes", 
                                      "Snapshot not ready", 
                                      "Snapshot is processing",
                                      "No data available"]:
                            st.warning(f"⚠️ {content}")
                            st.info("💡 The snapshot is still being processed. Please wait and try again later.")
                            return
                        
                        # Save the downloaded data
                        downloads_dir = Path("data/downloads")
                        downloads_dir.mkdir(exist_ok=True)
                        
                        file_extension = f".{download_format}"
                        if compress_data:
                            file_extension += ".gz"
                        
                        file_path = downloads_dir / f"{download_snapshot_id}{file_extension}"
                        
                        with open(file_path, 'wb') as f:
                            f.write(response.content)
                        
                        # Update the record to mark as downloaded
                        record_file = Path("data/snapshots") / f"{download_snapshot_id}.json"
                        if record_file.exists():
                            with open(record_file, 'r') as f:
                                record = json.load(f)
                            
                            record['downloaded'] = True
                            record['download_time'] = datetime.now().isoformat()
                            record['download_format'] = download_format
                            record['download_file'] = str(file_path)
                            
                            with open(record_file, 'w') as f:
                                json.dump(record, f, indent=2)
                        
                        st.success(f"✅ Successfully downloaded {download_snapshot_id}!")
                        st.info(f"📁 File saved to: `{file_path}`")
                        st.info(f"📊 Size: {len(response.content) / 1024 / 1024:.2f} MB")
                        st.rerun()
                        return
                    
                    elif response.status_code == 202:
                        if attempt < max_retries:
                            st.warning(f"⏳ Snapshot is building... Retrying in {retry_delay} seconds (attempt {attempt + 1}/{max_retries + 1})")
                            time.sleep(retry_delay)
                            continue
                        else:
                            st.error(f"❌ Download failed: HTTP 202 Error details: Snapshot is building. Try again in a few minutes")
                            st.info("💡 The snapshot is still being processed. Please wait and try again later.")
                            return
                    
                    else:
                        st.error(f"❌ Download failed: HTTP {response.status_code}")
                        st.error(f"Error details: {response.text}")
                        
                        # Provide specific guidance based on error code
                        if response.status_code == 400:
                            st.info("💡 HTTP 400 usually means the snapshot is not ready or the request format is invalid.")
                            st.info("💡 Try checking the snapshot status first, or wait a few minutes and try again.")
                        elif response.status_code == 404:
                            st.info("💡 HTTP 404 means the snapshot was not found. Check if the snapshot ID is correct.")
                        elif response.status_code == 403:
                            st.info("💡 HTTP 403 means access is forbidden. Check your API key and permissions.")
                        
                        return
    
    with col_cancel:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state[f'show_download_dialog_{snapshot_id}'] = False
            st.rerun()

@st.dialog("⚠️ Delete Confirmation")
def delete_snapshot_dialog(snapshot_id, selected_record):
    """Delete confirmation dialog using proper st.dialog decorator."""
    st.error("**You are about to permanently delete this snapshot.**")
    
    # Display snapshot details
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Snapshot ID**: `{snapshot_id}`")
        st.write(f"**Title**: {selected_record.get('title', 'Untitled')}")
    with col2:
        st.write(f"**Status**: {selected_record.get('status', 'Unknown')}")
        st.write(f"**Records**: {selected_record.get('records_limit', 'Unknown')}")
    
    st.warning("**This will permanently remove:**")
    st.write("• Snapshot record and metadata")
    st.write("• Downloaded data files (if any)")
    st.write("• All associated files")
    
    st.divider()
    
    # Confirmation buttons
    col_confirm, col_cancel = st.columns(2)
    
    with col_confirm:
        if st.button("✅ Yes, Delete", type="primary", use_container_width=True):
            # Delete the snapshot
            try:
                # Delete the snapshot record file
                record_file = Path("data/snapshots") / f"{snapshot_id}.json"
                if record_file.exists():
                    record_file.unlink()
                
                # Delete downloaded data files (check all formats)
                downloads_dir = Path("data/downloads")
                for ext in ['.json', '.csv', '.json.gz', '.csv.gz']:
                    data_file = downloads_dir / f"{snapshot_id}{ext}"
                    if data_file.exists():
                        data_file.unlink()
                
                st.success(f"✅ Snapshot `{snapshot_id}` deleted successfully!")
                
                # Clear session state and refresh
                if 'selected_snapshot' in st.session_state:
                    del st.session_state['selected_snapshot']
                
                # Close dialog
                st.session_state[f'show_delete_dialog_{snapshot_id}'] = False
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Failed to delete snapshot: {e}")
    
    with col_cancel:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state[f'show_delete_dialog_{snapshot_id}'] = False
            st.rerun()

# Page configuration
st.set_page_config(
    page_title="Snapshot Viewer - BrightData Manager",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .status-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.2rem 0;
        border: 1px solid rgba(0,0,0,0.1);
    }
    .status-completed { background-color: #d4edda; color: #155724; border-color: #c3e6cb; }
    .status-processing { background-color: #fff3cd; color: #856404; border-color: #ffeaa7; }
    .status-failed { background-color: #f8d7da; color: #721c24; border-color: #f5c6cb; }
    .status-submitted { background-color: #cce5ff; color: #004085; border-color: #b3d9ff; }
</style>
""", unsafe_allow_html=True)

def load_snapshot_records():
    """Load all snapshot records from the data/snapshots directory."""
    records_dir = Path("data/snapshots")
    if not records_dir.exists():
        return []
    
    records = []
    for file_path in records_dir.glob("*.json"):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                # Handle both list and dictionary formats
                if isinstance(data, list):
                    # If it's a list, create a summary record
                    record = {
                        'snapshot_id': file_path.stem,
                        'submission_time': '2025-01-01T00:00:00.000000',  # Default timestamp
                        'dataset_id': 'unknown',
                        'status': 'ready',
                        'records_count': len(data),
                        'file_type': 'data_list',
                        'file_path': str(file_path)
                    }
                elif isinstance(data, dict):
                    # If it's a dictionary, use it as is
                    record = data.copy()
                    record['file_path'] = str(file_path)
                else:
                    # Skip unknown formats
                    continue
                    
                records.append(record)
        except (json.JSONDecodeError, KeyError, TypeError):
            continue
    
    return sorted(records, key=lambda x: x.get('submission_time', ''), reverse=True)

def check_snapshot_status(snapshot_id, dataset_id):
    """Check the current status of a snapshot from the API."""
    brightdata = BrightDataFilter(dataset_id)
    metadata = brightdata.get_snapshot_metadata(snapshot_id)
    return metadata


def get_snapshot_status_badge(status):
    """Get a styled status badge with icon."""
    status_config = {
        'completed': {'class': 'status-completed', 'icon': '✅'},
        'ready': {'class': 'status-completed', 'icon': '✅'},
        'processing': {'class': 'status-processing', 'icon': '⏳'},
        'building': {'class': 'status-processing', 'icon': '🔨'},
        'submitted': {'class': 'status-submitted', 'icon': '📤'},
        'failed': {'class': 'status-failed', 'icon': '❌'}
    }
    
    config = status_config.get(status, {'class': 'status-submitted', 'icon': '📋'})
    return f'<span class="status-badge {config["class"]}">{config["icon"]} {status.upper()}</span>'

def get_time_ago(dt):
    """Get a human-readable time ago string."""
    now = datetime.now(dt.tzinfo) if dt.tzinfo else datetime.now()
    diff = now - dt
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    elif diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "just now"

def load_snapshot_data(snapshot_id):
    """Load the actual data for a snapshot (supports multiple formats)."""
    downloads_dir = Path("data/downloads")
    
    # Check for different file formats
    for ext in ['.json', '.csv', '.json.gz', '.csv.gz']:
        data_file = downloads_dir / f"{snapshot_id}{ext}"
        if data_file.exists():
            try:
                # Check if the file is empty first
                if data_file.stat().st_size == 0:
                    st.warning("⚠️ Downloaded file is empty")
                    return None
                
                # For compressed files, skip the content check and go directly to loading
                if ext.endswith('.gz'):
                    # Try to load the data based on format
                    if ext == '.json.gz':
                        return pd.read_json(data_file, compression='gzip')
                    elif ext == '.csv.gz':
                        return pd.read_csv(data_file, compression='gzip')
                else:
                    # For non-compressed files, check content first
                    with open(data_file, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                    
                    # Check if the content is a status message instead of data
                    if content in ["Snapshot is building. Try again in a few minutes", 
                                  "Snapshot not ready", 
                                  "Snapshot is processing",
                                  "No data available"]:
                        st.warning(f"⚠️ {content}")
                        return None
                    
                    # Check if the file is empty
                    if not content:
                        st.warning("⚠️ Downloaded file is empty")
                        return None
                    
                    # Try to load the data based on format
                    if ext == '.json':
                        return pd.read_json(data_file)
                    elif ext == '.csv':
                        return pd.read_csv(data_file)
                    
            except pd.errors.EmptyDataError:
                st.warning("⚠️ Downloaded file contains no data")
                return None
            except json.JSONDecodeError as e:
                st.error(f"❌ Invalid JSON format in {data_file}: {e}")
                st.info("💡 The snapshot might still be building. Try downloading again later.")
                return None
            except Exception as e:
                st.error(f"❌ Error loading data from {data_file}: {e}")
                return None
    
    return None

def delete_snapshot_record(snapshot_id):
    """Delete a snapshot record and its associated files."""
    try:
        # Delete the JSON record file
        record_file = Path("data/snapshots") / f"{snapshot_id}.json"
        if record_file.exists():
            record_file.unlink()
        
        # Delete the downloaded data file if it exists (check all formats)
        downloads_dir = Path("data/downloads")
        for ext in ['.json', '.csv', '.json.gz', '.csv.gz']:
            data_file = downloads_dir / f"{snapshot_id}{ext}"
            if data_file.exists():
                data_file.unlink()
        
        return True
    except Exception as e:
        st.error(f"Error deleting snapshot: {e}")
        return False

def update_manual_snapshot_status(snapshot_id):
    """Update the status of a manually added snapshot using the utility function."""
    try:
        # Get metadata using the utility function
        metadata = get_snapshot_metadata(snapshot_id)
        
        if metadata:
            # Update the record with new status and metadata
            record_file = Path("data/snapshots") / f"{snapshot_id}.json"
            if record_file.exists():
                with open(record_file, 'r') as f:
                    record = json.load(f)
                
                # Update status and metadata with all available information
                record['status'] = metadata.get('status', 'unknown')
                record['metadata'] = metadata
                
                # Update additional fields from metadata
                if 'dataset_id' in metadata:
                    record['dataset_id'] = metadata['dataset_id']
                if 'created' in metadata:
                    record['created_time'] = metadata['created']
                if 'dataset_size' in metadata:
                    record['dataset_size'] = metadata['dataset_size']
                if 'file_size' in metadata:
                    record['file_size'] = metadata['file_size']
                if 'cost' in metadata:
                    record['cost'] = metadata['cost']
                
                # Update filter criteria to show it's been updated
                if record.get('filter_criteria', {}).get('manual_entry'):
                    record['filter_criteria']['last_updated'] = datetime.now().isoformat()
                    record['filter_criteria']['status_checked'] = True
                
                # Save updated record
                with open(record_file, 'w') as f:
                    json.dump(record, f, indent=2)
                
                return True
        return False
    except Exception as e:
        st.error(f"Error updating snapshot status: {e}")
        return False

def get_snapshot_metadata(snapshot_id):
    """
    Get snapshot metadata from BrightData API.
    This is a utility function that doesn't require a dataset ID.
    """
    try:
        from util.config import get_brightdata_api_key
        api_key = get_brightdata_api_key()
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"https://api.brightdata.com/datasets/snapshots/{snapshot_id}",
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error retrieving snapshot metadata: {e}")
        return None

def get_snapshot_filter_details(snapshot_id):
    """
    Attempt to retrieve filter details from BrightData API.
    Note: This may not always work as the API doesn't always return original filter criteria.
    """
    try:
        metadata = get_snapshot_metadata(snapshot_id)
        if metadata:
            # Check if metadata contains filter information
            if 'filter' in metadata:
                return metadata['filter']
            elif 'query' in metadata:
                return metadata['query']
            else:
                return None
        return None
    except Exception as e:
        st.error(f"Error retrieving filter details: {e}")
        return None

def main():
    
    # Load snapshot records
    records = load_snapshot_records()
    
    if not records:
        st.warning("📁 No snapshot records found. Submit some filters first!")
        st.info("💡 Use the demo.ipynb notebook to submit filters and create snapshots.")
        return
    
    # Auto-refresh functionality removed as requested
    
    # Sidebar - Snapshot List
    st.sidebar.header("📊 All Snapshots")
    
    # Status summary in sidebar
    status_counts = {}
    
    for record in records:
        # Use "downloaded" status if downloaded, otherwise use original status
        if record.get('downloaded'):
            status = 'downloaded'
        else:
            status = record.get('status', 'submitted')  # Default to submitted instead of unknown
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Display status summary
    if status_counts:
        status_text = " | ".join([f"{status}: {count}" for status, count in status_counts.items()])
        st.sidebar.caption(f"Status: {status_text}")
    
    # Display all snapshots in sidebar
    for i, record in enumerate(records):
        status = record.get('status', 'submitted')  # Default to submitted instead of unknown
        date = record.get('submission_time', 'Unknown date')
        is_selected = st.session_state.get('selected_snapshot', {}).get('snapshot_id') == record['snapshot_id']
        
        if date != 'Unknown date':
            try:
                date_obj = datetime.fromisoformat(date.replace('Z', '+00:00'))
                date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                time_ago = get_time_ago(date_obj)
                date_str = f"{date_str} ({time_ago})"
            except:
                date_str = date
        else:
            date_str = 'Unknown'
        
        # Get filter count
        filter_criteria = record.get('filter_criteria', {})
        filter_count = 0
        if filter_criteria:
            if 'filters' in filter_criteria:
                filter_count = len(filter_criteria['filters'])
            else:
                filter_count = 1
        
        # Get records limit
        records_limit = record.get('records_limit', 'N/A')
        
        # Get title (use snapshot ID as fallback)
        title = record.get('title', f"Snapshot {record['snapshot_id'][:12]}...")
        
        # Create clickable card for each snapshot in sidebar
        card_style = ""
        if is_selected:
            card_style = "background-color: #e3f2fd; border-left: 3px solid #2196f3;"
        
        # Create a clickable container for each snapshot
        with st.sidebar.container():
            # Status badge with icon
            status_icons = {
                'completed': '✅',
                'ready': '✅', 
                'downloaded': '💾',
                'processing': '⏳',
                'building': '🔨',
                'submitted': '📤',
                'failed': '❌'
            }
            icon = status_icons.get(status, '📋')
            
            # Determine display status - show "downloaded" if downloaded, otherwise show original status
            display_status = "downloaded" if record.get('downloaded') else status
            display_icon = status_icons.get(display_status, '📋')
            
            # Create clickable area with title - make time more prominent
            button_text = f"{display_icon} {display_status.upper()}\n{title}\n[{records_limit} Records] {filter_count} filters\n🕒 {date_str}\nID: {record['snapshot_id']}"
            
            # Add highlighting for selected snapshot
            if is_selected:
                button_text = f"🎯 {button_text}"  # Add target icon for selected
                help_text = "Currently selected snapshot"
            else:
                help_text = "Click to select this snapshot"
            
            if st.sidebar.button(
                button_text,
                key=f"select_{i}",
                help=help_text,
                width='stretch'
            ):
                st.session_state['selected_snapshot'] = record
                # Check status when selecting a snapshot
                brightdata = BrightDataFilter('amazon_walmart')
                metadata = brightdata.get_snapshot_metadata(record['snapshot_id'])
                
                # Update the record with latest status
                if metadata:
                    record['status'] = metadata.get('status', record.get('status', 'submitted'))
                    record['dataset_size'] = metadata.get('dataset_size')
                    record['file_size'] = metadata.get('file_size')
                    record['cost'] = metadata.get('cost')
                    
                    # Save updated record
                    record_file = Path("data/snapshots") / f"{record['snapshot_id']}.json"
                    if record_file.exists():
                        with open(record_file, 'w') as f:
                            json.dump(record, f, indent=2)
                    
                    st.session_state['selected_snapshot'] = record
                
                st.rerun()
    
    # Main content area controls
    col1, col2 = st.columns([3, 1])
    
    with col1:
        
        # Display title and time as main title and subtitle
        if 'selected_snapshot' in st.session_state and st.session_state['selected_snapshot']:
            selected_snapshot = st.session_state['selected_snapshot']
            
            # Get title and dataset from the snapshot record
            title = selected_snapshot.get('title', 'Untitled Query')
            dataset_id = selected_snapshot.get('dataset_id', 'Unknown Dataset')
            
            # Get dataset name from registry
            try:
                from util.dataset_registry import dataset_registry
                dataset_config = dataset_registry.get_dataset(dataset_id)
                dataset_name = dataset_config.name if dataset_config else dataset_id
            except:
                dataset_name = dataset_id
            
            st.title(f"📊 {title} ({dataset_name})")
            
            # Get and format submission time as subtitle
            submission_time = selected_snapshot.get('submission_time', 'N/A')
            if submission_time != 'N/A':
                try:
                    dt = datetime.fromisoformat(submission_time.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                    time_ago = get_time_ago(dt)
                    st.subheader(f"🕒 Submitted: {formatted_time} ({time_ago})")
                except:
                    st.subheader(f"🕒 Submitted: {submission_time}")
            else:
                st.subheader("🕒 Submission time not available")
        
        # Show status check indicator
        if 'selected_snapshot' in st.session_state:
            selected_snapshot = st.session_state['selected_snapshot']
            if selected_snapshot:
                status = selected_snapshot.get('status', 'submitted')
                if status == 'ready':
                    st.success(f"✅ Status: {status.upper()} - Ready for download")
                elif status == 'downloaded':
                    st.info(f"💾 Status: {status.upper()} - Data available")
                elif status == 'submitted':
                    st.warning(f"📤 Status: {status.upper()} - Processing...")
                elif status == 'failed':
                    st.error(f"❌ Status: {status.upper()} - Failed")
                else:
                    st.info(f"📊 Status: {status.upper()}")
    
    # Main content area
    # Check if we have any records
    if not records:
        st.warning("⚠️ No snapshot records found in the data/snapshots directory.")
        st.info("💡 Make sure you have run some queries to generate snapshots.")
        return
    
    # Get selected record (from session state or first record)
    if 'selected_snapshot' in st.session_state and st.session_state['selected_snapshot'] is not None:
        selected_record = st.session_state['selected_snapshot']
        # Validate that the selected record still exists in our records
        if not any(r.get('snapshot_id') == selected_record.get('snapshot_id') for r in records):
            selected_record = records[0]
            st.session_state['selected_snapshot'] = selected_record
    else:
        selected_record = records[0]
        st.session_state['selected_snapshot'] = selected_record
    
    # Final safety check for selected_record
    if not selected_record or not isinstance(selected_record, dict):
        st.error("❌ Invalid snapshot record selected.")
        st.write(f"Debug: selected_record = {selected_record}")
        return
    
    snapshot_id = selected_record['snapshot_id']
    
    # Main content area
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Snapshots", len(records))
    
    with col2:
        completed_count = sum(1 for r in records if r.get('status', 'submitted') in ['completed', 'ready'])
        st.metric("✅ Completed", completed_count)
    
    with col3:
        processing_count = sum(1 for r in records if r.get('status', 'submitted') in ['submitted', 'processing', 'building'])
        st.metric("⏳ Processing", processing_count)
    
    with col4:
        failed_count = sum(1 for r in records if r.get('status', 'submitted') == 'failed')
        st.metric("❌ Failed", failed_count)
    
    st.divider()
    
    # Title and Description editing section
    
    # Selected Snapshot Details - Basic Information and Filter Criteria side by side
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Basic info
        st.subheader("📊 Basic Information")
        
        # Editable title and description with automatic saving
        current_title = selected_record.get('title', f"Snapshot {snapshot_id[:12]}...")
        current_description = selected_record.get('description', 'No description available')

        
        new_title = st.text_input(
            "📌 Title",
            value=current_title,
            help="Give your snapshot a descriptive title",
            key=f"title_{snapshot_id}"
        )
    
        new_description = st.text_area(
            "📄 Description",
            value=current_description,
            help="Describe what this snapshot contains or its purpose",
            key=f"description_{snapshot_id}"
        )

        # Auto-save when title or description changes
        if new_title != current_title or new_description != current_description:
            try:
                # Update the record
                selected_record['title'] = new_title
                selected_record['description'] = new_description
                selected_record['last_modified'] = datetime.now().isoformat()
                
                # Save back to file
                record_file = Path("data/snapshots") / f"{snapshot_id}.json"
                with open(record_file, 'w') as f:
                    json.dump(selected_record, f, indent=2)
                
                st.success("✅ Metadata updated automatically!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error saving metadata: {e}")
        
        
        # Basic metadata
        if not selected_record:
            st.error("❌ No snapshot record selected.")
            st.write(f"Debug: selected_record is None at metadata section")
            return
        
        # Final defensive check before accessing properties
        if not isinstance(selected_record, dict) or 'snapshot_id' not in selected_record:
            st.error("❌ Invalid snapshot record format.")
            return
            
        try:
            # Determine status - show "downloaded" if downloaded, otherwise show original status
            current_status = selected_record.get('status', 'submitted')
            if selected_record.get('downloaded'):
                display_status = "downloaded"
            else:
                display_status = current_status
            
            # Format submission time for better display
            submission_time = selected_record.get('submission_time', 'N/A')
            if submission_time != 'N/A':
                try:
                    # Parse and format the submission time
                    if 'T' in submission_time:
                        dt = datetime.fromisoformat(submission_time.replace('Z', '+00:00'))
                        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                        time_ago = get_time_ago(dt)
                        submission_time_display = f"{formatted_time} ({time_ago})"
                    else:
                        submission_time_display = submission_time
                except:
                    submission_time_display = submission_time
            else:
                submission_time_display = 'N/A'
            
            # Format completion time if available
            completion_time = selected_record.get('completion_time', 'N/A')
            if completion_time != 'N/A':
                try:
                    if 'T' in completion_time:
                        dt = datetime.fromisoformat(completion_time.replace('Z', '+00:00'))
                        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                        time_ago = get_time_ago(dt)
                        completion_time_display = f"{formatted_time} ({time_ago})"
                    else:
                        completion_time_display = completion_time
                except:
                    completion_time_display = completion_time
            else:
                completion_time_display = 'N/A'
            
            info_data = {
                "Snapshot ID": selected_record['snapshot_id'],
                "Dataset ID": selected_record.get('dataset_id', 'N/A'),
                "Records Limit": selected_record.get('records_limit', 'N/A'),
                "Status": display_status,
                "Cost": selected_record.get('metadata', {}).get('cost', 'N/A') if selected_record.get('metadata') else 'N/A'
            }
        except (AttributeError, TypeError, KeyError) as e:
            st.error(f"❌ Error accessing snapshot metadata: {e}")
            st.info("🔄 Please refresh the page or select a different snapshot.")
            return
        
        # Add last modified time if available
        last_modified = selected_record.get('last_modified')
        if last_modified:
            try:
                modified_time = datetime.fromisoformat(last_modified.replace('Z', '+00:00'))
                info_data["Last Modified"] = modified_time.strftime('%Y-%m-%d %H:%M:%S')
            except:
                info_data["Last Modified"] = last_modified
        
        for key, value in info_data.items():
            if key == "Status":
                st.markdown(f"**{key}:** {get_snapshot_status_badge(value)}", unsafe_allow_html=True)
            else:
                st.write(f"**{key}:** {value}")
        
        st.divider()
        
        # Prominent Time Information Section
        st.subheader("🕒 Timeline")
        
        # Add custom CSS for timeline styling
        st.markdown("""
        <style>
        .timeline-container {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
        }
        .timeline-item {
            background: rgba(255, 255, 255, 0.9);
            padding: 0.8rem;
            border-radius: 8px;
            margin: 0.5rem 0;
            border-left: 4px solid #667eea;
        }
        .timeline-time {
            font-size: 1.1em;
            font-weight: bold;
            color: #2c3e50;
        }
        .timeline-label {
            font-size: 0.9em;
            color: #7f8c8d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create columns for time information
        time_col1, time_col2 = st.columns(2)
        
        with time_col1:
            if submission_time_display != 'N/A':
                st.markdown(f"""
                <div class="timeline-item">
                    <div class="timeline-label">📤 Submission Time</div>
                    <div class="timeline-time">🕒 {submission_time_display}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Submission time not available")
        
        with time_col2:
            if completion_time_display != 'N/A':
                st.markdown(f"""
                <div class="timeline-item">
                    <div class="timeline-label">✅ Completion Time</div>
                    <div class="timeline-time">🕒 {completion_time_display}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("⏳ Not completed yet")
        
        # Calculate processing duration if both times are available
        if submission_time != 'N/A' and completion_time != 'N/A':
            try:
                sub_dt = datetime.fromisoformat(submission_time.replace('Z', '+00:00'))
                comp_dt = datetime.fromisoformat(completion_time.replace('Z', '+00:00'))
                duration = comp_dt - sub_dt
                
                if duration.days > 0:
                    duration_str = f"{duration.days} day{'s' if duration.days > 1 else ''}, {duration.seconds // 3600}h {(duration.seconds % 3600) // 60}m"
                elif duration.seconds > 3600:
                    hours = duration.seconds // 3600
                    minutes = (duration.seconds % 3600) // 60
                    duration_str = f"{hours}h {minutes}m"
                elif duration.seconds > 60:
                    minutes = duration.seconds // 60
                    duration_str = f"{minutes}m {duration.seconds % 60}s"
                else:
                    duration_str = f"{duration.seconds}s"
                
                st.markdown(f"""
                <div class="timeline-item">
                    <div class="timeline-label">⏱️ Processing Duration</div>
                    <div class="timeline-time">🕒 {duration_str}</div>
                </div>
                """, unsafe_allow_html=True)
            except:
                st.markdown("**⏱️ Processing Duration:** Unable to calculate")
        
        st.divider()
    
    with col2:
        # Query Information
        st.subheader("🔍 Query Information")
        
        # Display the filter criteria if available
        filter_criteria = selected_record.get('filter_criteria', {})
        if filter_criteria:
            st.write("**Filter Criteria:**")
            st.json(filter_criteria)
        else:
            st.info("No filter criteria available")
        
        # Display query parameters
        st.write("**Query Parameters:**")
        query_params = {
            "Dataset ID": selected_record.get('dataset_id', 'N/A'),
            "Records Limit": selected_record.get('records_limit', 'N/A'),
            "Filter Type": selected_record.get('filter_type', 'N/A'),
            "Created": selected_record.get('submission_time', 'N/A')
        }
        
        for key, value in query_params.items():
            st.write(f"**{key}:** {value}")
        
        st.divider()
        
    
    # Data Analysis (if data is available)
    if data_available:
        st.divider()
        st.header("📈 Data Analysis")
        
        # Load and display data
        df = load_snapshot_data(snapshot_id)
        if df is not None:
            # Basic info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Records", len(df))
            with col2:
                st.metric("📋 Columns", len(df.columns))
            with col3:
                st.metric("💾 Memory", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.1f} MB")
            
            # Data preview
            st.subheader("🔍 Data Preview")
            st.dataframe(df.head(10), width='stretch')
            
            # Column information
            st.subheader("📋 Column Information")
            st.dataframe(pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes,
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum(),
                'Null %': (df.isnull().sum() / len(df) * 100).round(2)
            }), width='stretch')
            
            # Statistical analysis
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                st.subheader("📊 Statistical Summary")
                st.dataframe(df[numeric_cols].describe(), width='stretch')
                
                # Simple visualizations
                if len(numeric_cols) > 0:
                    st.subheader("📈 Visualizations")
                    
                    # Select columns for visualization
                    selected_cols = st.multiselect(
                        "Select numeric columns to visualize:",
                        options=numeric_cols.tolist(),
                        default=numeric_cols.tolist()[:2] if len(numeric_cols) >= 2 else numeric_cols.tolist()
                    )
                    
                    if selected_cols:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            # Histogram
                            if len(selected_cols) >= 1:
                                fig_hist = px.histogram(df, x=selected_cols[0], title=f"Distribution of {selected_cols[0]}")
                                st.plotly_chart(fig_hist, use_container_width=True)
                        
                        with col2:
                            # Scatter plot
                            if len(selected_cols) >= 2:
                                fig_scatter = px.scatter(df, x=selected_cols[0], y=selected_cols[1], 
                                                       title=f"{selected_cols[0]} vs {selected_cols[1]}")
                                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Categorical analysis
            categorical_cols = df.select_dtypes(include=['object']).columns
            if len(categorical_cols) > 0:
                st.subheader("📋 Categorical Analysis")
                
                selected_cat_col = st.selectbox(
                    "Select categorical column:",
                    options=categorical_cols.tolist()
                )
                
                if selected_cat_col:
                    value_counts = df[selected_cat_col].value_counts().head(10)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write("**Top 10 Values:**")
                        st.dataframe(value_counts.to_frame('Count'), width='stretch')
                    
                    with col2:
                        fig_bar = px.bar(x=value_counts.index, y=value_counts.values,
                                       title=f"Top Values in {selected_cat_col}")
                        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Actions section at the bottom
    st.divider()
    st.subheader("🛠️ Actions")
    
    # Check if data is available (support multiple formats)
    downloads_dir = Path("data/downloads")
    data_file = None
    data_available = False
    
    # Check for different file formats
    for ext in ['.json', '.csv', '.json.gz', '.csv.gz']:
        potential_file = downloads_dir / f"{snapshot_id}{ext}"
        if potential_file.exists():
            data_file = potential_file
            data_available = True
            break
    
    if data_available:
        st.success("✅ Data available for analysis")
    else:
        st.warning("⚠️ Data not downloaded yet")
        
        # Download form with snapshot ID requirement
        # Download section with popup confirmation
        st.write("**📥 Download Snapshot Data**")
        
        # Get record count for cost calculation
        records_limit = selected_record.get('records_limit', 1000)
        estimated_cost = records_limit * 0.002
        
        col_download1, col_download2 = st.columns(2)
        
        with col_download1:
            if st.button("📥 Download Data", type="primary", help="Download snapshot data (incurs costs)"):
                st.session_state[f'show_download_dialog_{snapshot_id}'] = True
        
        with col_download2:
            # Download format selection
            download_format = st.selectbox(
                "Format",
                options=["json", "csv"],
                index=0,
                help="Choose the format for downloaded data",
                key=f"format_{snapshot_id}"
            )
        
        # Show cost information
        st.info(f"💰 **Estimated Cost**: ${estimated_cost:.4f} (${0.002:.3f} per record × {records_limit:,} records)")
        
        # Download confirmation dialog
        if st.session_state.get(f'show_download_dialog_{snapshot_id}', False):
            download_snapshot_dialog(snapshot_id, selected_record, download_format)
    
    # Delete button section
    st.divider()
    st.subheader("🗑️ Snapshot Management")
    
    col_delete1, col_delete2 = st.columns([1, 1])
    
    with col_delete1:
        if st.button("🗑️ Delete Snapshot", type="secondary", help="Permanently delete this snapshot"):
            st.session_state[f'show_delete_dialog_{snapshot_id}'] = True
    
    with col_delete2:
        st.info("⚠️ This action cannot be undone")
    
    # Delete confirmation dialog
    if st.session_state.get(f'show_delete_dialog_{snapshot_id}', False):
        delete_snapshot_dialog(snapshot_id, selected_record)
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
        <p>📊 BrightData Snapshot Viewer | Built with Streamlit</p>
        <p>💡 Use the snapshot manager for advanced operations</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
