#!/usr/bin/env python3
"""
BrightData Manager - Multi-page Streamlit Application

Main entry point for the BrightData query builder, snapshot viewer, and settings.
"""

import streamlit as st
from pathlib import Path
import sys

# Add the util directory to the path
sys.path.append(str(Path(__file__).parent / "util"))

# Page configuration
st.set_page_config(
    page_title="BrightData Manager",
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
    .page-description {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 3rem;
    }
    .feature-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .nav-instruction {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #1f77b4;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application entry point"""
    
    # Header
    st.markdown('<h1 class="main-header">📊 BrightData Manager</h1>', unsafe_allow_html=True)
    st.markdown('<p class="page-description">Comprehensive data analysis and query building for BrightData datasets</p>', unsafe_allow_html=True)
    
    # Navigation instructions
    st.markdown("""
    <div class="nav-instruction">
        <h3>🚀 Getting Started</h3>
        <p>Use the sidebar to navigate between pages:</p>
        <ul>
            <li><strong>Query Builder</strong> - Create and submit data queries</li>
            <li><strong>Snapshot Viewer</strong> - View and analyze downloaded snapshots</li>
            <li><strong>Settings</strong> - Manage API credentials and configuration</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature overview
    st.header("🎯 Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🔍 Query Builder</h3>
            <p>Build complex data queries with visual interface:</p>
            <ul>
                <li>Select from multiple datasets</li>
                <li>Create custom filters</li>
                <li>Preview query before submission</li>
                <li>Submit queries to BrightData API</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Snapshot Viewer</h3>
            <p>Analyze downloaded data snapshots:</p>
            <ul>
                <li>Browse all snapshots</li>
                <li>Download data files</li>
                <li>Interactive data analysis</li>
                <li>Statistical summaries</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>⚙️ Settings</h3>
            <p>Manage your configuration:</p>
            <ul>
                <li>API key management</li>
                <li>Data path configuration</li>
                <li>Credential validation</li>
                <li>Security settings</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick start guide
    st.header("🚀 Quick Start Guide")
    
    st.markdown("""
    ### 1. Configure Your Credentials
    Go to **Settings** page and enter your BrightData API key. The system will automatically 
    validate your credentials and save them securely.
    
    ### 2. Build Your First Query
    Navigate to **Query Builder** and:
    - Select a dataset (Amazon Products, Walmart, etc.)
    - Add filter conditions
    - Preview your query
    - Submit to get a snapshot ID
    
    ### 3. Analyze Your Data
    Go to **Snapshot Viewer** to:
    - View your submitted queries
    - Download data when ready
    - Perform interactive analysis
    - Export results
    
    ### 4. Advanced Features
    - **Multiple Datasets**: Switch between Amazon, Walmart, Shopee, TikTok, and Target
    - **Complex Filters**: Combine multiple conditions with AND/OR logic
    - **Data Analysis**: Built-in statistical analysis and visualizations
    - **Export Options**: Download data in CSV or JSON format
    """)
    
    # System status
    st.header("📋 System Status")
    
    col1, col2, col3 = st.columns(3)
    
    # Check if secrets.yaml exists
    secrets_exists = Path("secrets.yaml").exists()
    with col1:
        if secrets_exists:
            st.success("✅ Configuration file found")
        else:
            st.warning("⚠️ Configuration file missing")
    
    # Check if data directory exists
    data_dir_exists = Path("data/snapshots").exists()
    with col2:
        if data_dir_exists:
            st.success("✅ Data directory found")
        else:
            st.warning("⚠️ Data directory missing")
    
    # Check if dataset config exists
    config_exists = Path("config/datasets.yaml").exists()
    with col3:
        if config_exists:
            st.success("✅ Dataset configuration found")
        else:
            st.error("❌ Dataset configuration missing")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
        <p>BrightData Manager v1.0 | Built with Streamlit</p>
        <p>For support, check the documentation or contact your administrator.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
