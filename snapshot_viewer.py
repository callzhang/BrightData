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
        padding: 0.25rem 0.5rem;
        border-radius: 0.25rem;
        font-size: 0.8rem;
        font-weight: bold;
    }
    .status-completed { background-color: #d4edda; color: #155724; }
    .status-processing { background-color: #fff3cd; color: #856404; }
    .status-failed { background-color: #f8d7da; color: #721c24; }
    .status-submitted { background-color: #cce5ff; color: #004085; }
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
            metadata = check_snapshot_status(record['snapshot_id'], record.get('dataset_id'))
            if metadata:
                new_status = metadata.get('status', current_status)
                
                # Only update if status actually changed
                if new_status != current_status:
                    # Update the record with new status
                    record['status'] = new_status
                    record['metadata'] = metadata
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
    """Get a styled status badge."""
    status_colors = {
        'completed': 'status-completed',
        'processing': 'status-processing', 
        'failed': 'status-failed',
        'submitted': 'status-submitted'
    }
    color_class = status_colors.get(status, 'status-submitted')
    return f'<span class="status-badge {color_class}">{status.upper()}</span>'

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
    if current_time - st.session_state['last_refresh'] >= 30:
        # Auto-refresh statuses
        updated_count = 0
        for record in records:
            if update_snapshot_status(record):
                updated_count += 1
        
        if updated_count > 0:
            st.success(f"🔄 Auto-refresh: Updated {updated_count} snapshot statuses")
        
        st.session_state['last_refresh'] = current_time
        st.rerun()
    
    # Auto-refresh and status checking
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("📋 Snapshot List")
    
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
            time_since_refresh = current_time - st.session_state['last_refresh']
            time_until_next = 30 - time_since_refresh
            if time_until_next > 0:
                st.info(f"🔄 Next refresh: {int(time_until_next)}s")
            else:
                st.info("🔄 Refreshing...")
    
    # Create two-column layout
    left_col, right_col = st.columns([1, 2])
    
    with left_col:
        st.subheader("📊 All Snapshots")
        
        # Status summary
        status_counts = {}
        for record in records:
            status = record.get('status', 'unknown')
            status_counts[status] = status_counts.get(status, 0) + 1
        
        # Display status summary
        if status_counts:
            status_text = " | ".join([f"{status}: {count}" for status, count in status_counts.items()])
            st.caption(f"Status: {status_text}")
        
        st.divider()
        
        # Display all snapshots in a compact list
        for i, record in enumerate(records):
            status = record.get('status', 'unknown')
            date = record.get('submission_time', 'Unknown date')
            is_selected = st.session_state.get('selected_snapshot', {}).get('snapshot_id') == record['snapshot_id']
            
            if date != 'Unknown date':
                try:
                    date_obj = datetime.fromisoformat(date.replace('Z', '+00:00'))
                    date_str = date_obj.strftime('%m-%d %H:%M')
                except:
                    date_str = date[:10] if len(date) > 10 else date
            else:
                date_str = 'Unknown'
            
            # Create a clickable card for each snapshot
            with st.container():
                # Highlight selected snapshot
                if is_selected:
                    st.markdown("""
                    <div style="background-color: #e3f2fd; padding: 0.5rem; border-radius: 0.25rem; border-left: 3px solid #2196f3;">
                    """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**{record['snapshot_id'][:12]}...**")
                    st.caption(f"{date_str}")
                
                with col2:
                    st.markdown(get_snapshot_status_badge(status), unsafe_allow_html=True)
                
                with col3:
                    if st.button("📋", key=f"select_{i}", help="Select this snapshot"):
                        st.session_state['selected_snapshot'] = record
                        st.rerun()
                
                if is_selected:
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.divider()
    
    with right_col:
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
        completed_count = sum(1 for r in records if r.get('status') == 'completed')
        st.metric("✅ Completed", completed_count)
    
    with col3:
        processing_count = sum(1 for r in records if r.get('status') in ['submitted', 'processing'])
        st.metric("⏳ Processing", processing_count)
    
    with col4:
        failed_count = sum(1 for r in records if r.get('status') == 'failed')
        st.metric("❌ Failed", failed_count)
    
    st.divider()
    
    # Selected Snapshot Details
    st.header(f"📋 Snapshot Details: {snapshot_id}")
    
    col1, col2 = st.columns([2, 1])
    
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
        # Actions
        st.subheader("🛠️ Actions")
        
        # Check if data is available
        data_file = Path("downloads") / f"{snapshot_id}.json"
        data_available = data_file.exists()
        
        if data_available:
            st.success("✅ Data available for analysis")
            
            if st.button("📊 View Data", type="primary"):
                st.session_state['view_data'] = True
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
    
    # Filter Criteria
    st.subheader("🔍 Filter Criteria")
    filter_criteria = selected_record.get('filter_criteria', {})
    if filter_criteria:
        st.json(filter_criteria)
    else:
        st.info("No filter criteria available")
    
    # Data Analysis (if data is available and requested)
    if st.session_state.get('view_data', False) and data_available:
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
