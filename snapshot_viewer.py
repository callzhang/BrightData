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
sys.path.append(str(Path(__file__).parent / "util"))

try:
    from util import BrightDataFilter
    from util.config import get_brightdata_api_key
except ImportError:
    st.error("❌ Could not import BrightData utilities. Make sure you're running from the project root.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="BrightData Snapshot Viewer",
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
    """Load all snapshot records from the snapshot_records directory."""
    records_dir = Path("snapshot_records")
    if not records_dir.exists():
        return []
    
    records = []
    for file_path in records_dir.glob("*.json"):
        try:
            with open(file_path, 'r') as f:
                record = json.load(f)
                record['file_path'] = str(file_path)
                records.append(record)
        except (json.JSONDecodeError, KeyError):
            continue
    
    return sorted(records, key=lambda x: x.get('submission_time', ''), reverse=True)

def check_snapshot_status(snapshot_id, dataset_id):
    """Check the current status of a snapshot from the API."""
    try:
        brightdata = BrightDataFilter(dataset_id)
        metadata = brightdata.get_snapshot_metadata(snapshot_id)
        return metadata
    except Exception as e:
        print(f"Error checking status for {snapshot_id}: {e}")
        return None

def update_snapshot_status(record):
    """Update the status of a snapshot record if it's not completed."""
    current_status = record.get('status', 'unknown')
    
    # Only check status for non-completed snapshots
    if current_status in ['submitted', 'processing', 'scheduled']:
        try:
            metadata = get_snapshot_metadata(record['snapshot_id'])
            if metadata:
                new_status = metadata.get('status', current_status)
                
                # Only update if status actually changed
                if new_status != current_status:
                    # Update the record with new status and all metadata
                    record['status'] = new_status
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
                    if metadata.get('completion_time'):
                        record['completion_time'] = metadata['completion_time']
                    
                    # Save updated record back to file
                    with open(record['file_path'], 'w') as f:
                        json.dump(record, f, indent=2)
                    
                    return True
        except Exception as e:
            # Don't print errors to avoid cluttering the UI
            pass
    
    return False

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

def load_snapshot_data(snapshot_id):
    """Load the actual data for a snapshot."""
    data_file = Path("downloads") / f"{snapshot_id}.json"
    if data_file.exists():
        try:
            return pd.read_json(data_file)
        except Exception as e:
            st.error(f"Error loading data: {e}")
            return None
    return None

def delete_snapshot_record(snapshot_id):
    """Delete a snapshot record and its associated files."""
    try:
        # Delete the JSON record file
        record_file = Path("snapshot_records") / f"{snapshot_id}.json"
        if record_file.exists():
            record_file.unlink()
        
        # Delete the downloaded data file if it exists
        data_file = Path("downloads") / f"{snapshot_id}.json"
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
            record_file = Path("snapshot_records") / f"{snapshot_id}.json"
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
        from .config import get_brightdata_api_key
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
    # Header
    st.markdown('<h1 class="main-header">📊 BrightData Snapshot Viewer</h1>', unsafe_allow_html=True)
    
    # Load snapshot records
    records = load_snapshot_records()
    
    if not records:
        st.warning("📁 No snapshot records found. Submit some filters first!")
        st.info("💡 Use the demo.ipynb notebook to submit filters and create snapshots.")
        return
    
    # Auto-check status for non-completed snapshots (only on first load)
    if 'status_checked' not in st.session_state:
        with st.spinner("🔄 Checking snapshot statuses..."):
            updated_count = 0
            for record in records:
                if update_snapshot_status(record):
                    updated_count += 1
            
            if updated_count > 0:
                st.success(f"✅ Auto-updated {updated_count} snapshot statuses")
                st.rerun()
        
        st.session_state['status_checked'] = True
    
    # Auto-refresh mechanism
    if 'last_refresh' not in st.session_state:
        st.session_state['last_refresh'] = time.time()
    
    # Check if 30 seconds have passed since last refresh
    current_time = time.time()
    time_since_refresh = current_time - st.session_state['last_refresh']
    
    if time_since_refresh >= 30:
        # Auto-refresh statuses
        updated_count = 0
        for record in records:
            if update_snapshot_status(record):
                updated_count += 1
        
        if updated_count > 0:
            st.success(f"🔄 Auto-refresh: Updated {updated_count} snapshot statuses")
        
        st.session_state['last_refresh'] = current_time
        st.rerun()
    
    # Store countdown info for display
    st.session_state['countdown_seconds'] = max(0, 30 - int(time_since_refresh))
    
    # Sidebar - Snapshot List
    st.sidebar.header("📊 All Snapshots")
    
    # Status summary in sidebar
    status_counts = {}
    for record in records:
        status = record.get('status', 'unknown')
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Display status summary
    if status_counts:
        status_text = " | ".join([f"{status}: {count}" for status, count in status_counts.items()])
        st.sidebar.caption(f"Status: {status_text}")
    
    # Manual snapshot ID input
    st.sidebar.divider()
    st.sidebar.subheader("➕ Add Snapshot Manually")
    
    with st.sidebar.form("add_snapshot_form"):
        manual_snapshot_id = st.text_input(
            "Snapshot ID", 
            placeholder="e.g., snap_abc123...",
            help="Enter a snapshot ID to add manually"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("➕ Add Snapshot"):
                if manual_snapshot_id:
                    # Try to get metadata from API first
                    with st.spinner("Retrieving snapshot details..."):
                        metadata = get_snapshot_metadata(manual_snapshot_id)
                        
                        if metadata:
                            # Create record with API metadata
                            manual_record = {
                                'snapshot_id': manual_snapshot_id,
                                'dataset_id': metadata.get('dataset_id', 'unknown'),
                                'records_limit': metadata.get('dataset_size', 1000),
                                'submission_time': datetime.now().isoformat(),
                                'created_time': metadata.get('created'),
                                'status': metadata.get('status', 'unknown'),
                                'dataset_size': metadata.get('dataset_size'),
                                'file_size': metadata.get('file_size'),
                                'cost': metadata.get('cost'),
                                'filter_criteria': {
                                    'manual_entry': True,
                                    'description': 'Manually added snapshot',
                                    'filters': [],
                                    'original_criteria': None,
                                    'api_retrieved': True
                                },
                                'metadata': metadata
                            }
                            st.sidebar.success("✅ Retrieved details from API!")
                        else:
                            # Create basic record if API fails
                            manual_record = {
                                'snapshot_id': manual_snapshot_id,
                                'dataset_id': 'unknown',
                                'records_limit': 1000,
                                'submission_time': datetime.now().isoformat(),
                                'status': 'unknown',
                                'filter_criteria': {
                                    'manual_entry': True,
                                    'description': 'Manually added snapshot',
                                    'filters': [],
                                    'original_criteria': None,
                                    'api_retrieved': False
                                },
                                'metadata': {
                                    'cost': None,
                                    'delivery_url': None,
                                    'download_url': None,
                                    'status': 'unknown'
                                }
                            }
                            st.sidebar.warning("⚠️ Could not retrieve from API, created basic record")
                        
                        # Save the manual record
                        record_file = Path("snapshot_records") / f"{manual_snapshot_id}.json"
                        try:
                            with open(record_file, 'w') as f:
                                json.dump(manual_record, f, indent=2)
                            st.sidebar.success(f"✅ Added snapshot: {manual_snapshot_id[:12]}...")
                            st.rerun()
                        except Exception as e:
                            st.sidebar.error(f"❌ Error adding snapshot: {e}")
                else:
                    st.sidebar.error("❌ Please enter a snapshot ID")
        
        with col2:
            if st.form_submit_button("🔍 Retrieve Details"):
                if manual_snapshot_id:
                    with st.spinner("Retrieving details..."):
                        # Try to get filter details
                        filter_details = get_snapshot_filter_details(manual_snapshot_id)
                        metadata = get_snapshot_metadata(manual_snapshot_id)
                        
                        if metadata:
                            st.sidebar.success("✅ Retrieved metadata!")
                            st.sidebar.json(metadata)
                        else:
                            st.sidebar.warning("⚠️ No metadata found")
                        
                        if filter_details:
                            st.sidebar.success("✅ Filter details found!")
                            st.sidebar.json(filter_details)
                        else:
                            st.sidebar.info("ℹ️ No filter details in API response")
                else:
                    st.sidebar.error("❌ Please enter Snapshot ID")
    
    st.sidebar.divider()
    
    # Display all snapshots in sidebar
    for i, record in enumerate(records):
        status = record.get('status', 'unknown')
        date = record.get('submission_time', 'Unknown date')
        is_selected = st.session_state.get('selected_snapshot', {}).get('snapshot_id') == record['snapshot_id']
        
        if date != 'Unknown date':
            try:
                date_obj = datetime.fromisoformat(date.replace('Z', '+00:00'))
                date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
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
                'processing': '⏳',
                'building': '🔨',
                'submitted': '📤',
                'failed': '❌'
            }
            icon = status_icons.get(status, '📋')
            
            # Create clickable area
            if st.sidebar.button(
                f"{icon} {status.upper()}\n{record['snapshot_id'][:12]}...\n[{records_limit} Records] {filter_count} filters\n{date_str}",
                key=f"select_{i}",
                help="Click to select this snapshot",
                use_container_width=True
            ):
                st.session_state['selected_snapshot'] = record
                st.rerun()
    
    # Main content area controls
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📋 Snapshot Details")
    
    with col2:
        col2_1, col2_2 = st.columns(2)
        
        with col2_1:
            if st.button("🔄 Refresh", help="Check status of all non-completed snapshots"):
                with st.spinner("Checking snapshot statuses..."):
                    updated_count = 0
                    for record in records:
                        if update_snapshot_status(record):
                            updated_count += 1
                    
                    if updated_count > 0:
                        st.success(f"✅ Updated {updated_count} snapshot statuses")
                        st.rerun()
                    else:
                        st.info("ℹ️ No status updates needed")
        
        with col2_2:
            # Show auto-refresh status with countdown
            countdown_seconds = st.session_state.get('countdown_seconds', 0)
            
            if countdown_seconds > 0:
                st.info(f"🔄 Next refresh: {countdown_seconds}s")
            else:
                st.info("🔄 Ready to refresh")
                # Auto-refresh when countdown reaches 0
                if st.button("🔄 Auto Refresh", help="Check status of all snapshots"):
                    st.session_state['last_refresh'] = current_time
                    st.rerun()
    
    # Main content area
    # Get selected record (from session state or first record)
    if 'selected_snapshot' in st.session_state:
        selected_record = st.session_state['selected_snapshot']
    else:
        selected_record = records[0]
        st.session_state['selected_snapshot'] = selected_record
    
    snapshot_id = selected_record['snapshot_id']
    
    # Main content area
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Total Snapshots", len(records))
    
    with col2:
        completed_count = sum(1 for r in records if r.get('status') in ['completed', 'ready'])
        st.metric("✅ Completed", completed_count)
    
    with col3:
        processing_count = sum(1 for r in records if r.get('status') in ['submitted', 'processing', 'building'])
        st.metric("⏳ Processing", processing_count)
    
    with col4:
        failed_count = sum(1 for r in records if r.get('status') == 'failed')
        st.metric("❌ Failed", failed_count)
    
    st.divider()
    
    # Selected Snapshot Details - Basic Information and Filter Criteria side by side
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Basic info
        st.subheader("📊 Basic Information")
        info_data = {
            "Snapshot ID": selected_record['snapshot_id'],
            "Dataset ID": selected_record.get('dataset_id', 'N/A'),
            "Records Limit": selected_record.get('records_limit', 'N/A'),
            "Submission Time": selected_record.get('submission_time', 'N/A'),
            "Status": selected_record.get('status', 'unknown'),
            "Completion Time": selected_record.get('completion_time', 'N/A'),
            "Cost": selected_record.get('metadata', {}).get('cost', 'N/A')
        }
        
        for key, value in info_data.items():
            if key == "Status":
                st.markdown(f"**{key}:** {get_snapshot_status_badge(value)}", unsafe_allow_html=True)
            else:
                st.write(f"**{key}:** {value}")
    
    with col2:
        # Filter Criteria
        st.subheader("🔍 Filter Criteria")
        filter_criteria = selected_record.get('filter_criteria', {})
        if filter_criteria:
            # Check if it's a manual entry
            if filter_criteria.get('manual_entry'):
                st.info("📝 **Manually Added Snapshot**")
                st.write(f"**Description:** {filter_criteria.get('description', 'No description')}")
                st.write(f"**Entry Type:** Manual addition")
                
                # Show API retrieval status
                if filter_criteria.get('api_retrieved'):
                    st.success("✅ **Details retrieved from API**")
                else:
                    st.warning("⚠️ **Basic record created** (API retrieval failed)")
                
                # Show parsed filters if available
                if filter_criteria.get('filters'):
                    st.write("**Parsed Filters:**")
                    st.json(filter_criteria['filters'])
                else:
                    st.write("**Parsed Filters:** No filter criteria available")
                
                # Show original criteria if available
                if filter_criteria.get('original_criteria'):
                    st.write("**Original Filter Criteria:**")
                    st.code(filter_criteria['original_criteria'], language='json')
                else:
                    st.write("**Original Filter Criteria:** Not provided")
            else:
                st.json(filter_criteria)
        else:
            st.info("No filter criteria available")
    
    # Actions section below the two sections
    st.subheader("🛠️ Actions")
    
    # Check if data is available
    data_file = Path("downloads") / f"{snapshot_id}.json"
    data_available = data_file.exists()
    
    col1, col2 = st.columns(2)
    
    with col1:
        if data_available:
            st.success("✅ Data available for analysis")
        else:
            st.warning("⚠️ Data not downloaded yet")
            if st.button("📥 Download Data"):
                try:
                    # Initialize BrightData filter
                    dataset_id = selected_record.get('dataset_id')
                    if dataset_id:
                        brightdata = BrightDataFilter(dataset_id)
                        
                        # Try to download
                        with st.spinner("Downloading data..."):
                            # This would use the snapshot manager functionality
                            st.info("💡 Use the snapshot manager to download data:")
                            st.code(f"python snapshot_manager.py -d")
                    else:
                        st.error("No dataset ID found in record")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with col2:
        # Delete button with confirmation
        if st.button("🗑️ Delete Snapshot", type="secondary"):
            st.session_state['show_delete_confirm'] = True
        
        # Delete confirmation dialog
        if st.session_state.get('show_delete_confirm', False):
            st.warning("⚠️ **Delete Confirmation**")
            st.write(f"Are you sure you want to delete snapshot `{snapshot_id[:12]}...`?")
            st.write("This will permanently remove:")
            st.write("• Snapshot record and metadata")
            st.write("• Downloaded data (if any)")
            
            confirm_col1, confirm_col2 = st.columns(2)
            with confirm_col1:
                if st.button("✅ Yes, Delete", type="primary"):
                    if delete_snapshot_record(snapshot_id):
                        st.success("✅ Snapshot deleted successfully!")
                        # Clear session state and refresh
                        if 'selected_snapshot' in st.session_state:
                            del st.session_state['selected_snapshot']
                        st.session_state['show_delete_confirm'] = False
                        st.rerun()
                    else:
                        st.error("❌ Failed to delete snapshot")
            
            with confirm_col2:
                if st.button("❌ Cancel"):
                    st.session_state['show_delete_confirm'] = False
                    st.rerun()
    
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
            st.dataframe(df.head(10), use_container_width=True)
            
            # Column information
            st.subheader("📋 Column Information")
            st.dataframe(pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes,
                'Non-Null Count': df.count(),
                'Null Count': df.isnull().sum(),
                'Null %': (df.isnull().sum() / len(df) * 100).round(2)
            }), use_container_width=True)
            
            # Statistical analysis
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                st.subheader("📊 Statistical Summary")
                st.dataframe(df[numeric_cols].describe(), use_container_width=True)
                
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
                        st.dataframe(value_counts.to_frame('Count'), use_container_width=True)
                    
                    with col2:
                        fig_bar = px.bar(x=value_counts.index, y=value_counts.values,
                                       title=f"Top Values in {selected_cat_col}")
                        st.plotly_chart(fig_bar, use_container_width=True)
    
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
