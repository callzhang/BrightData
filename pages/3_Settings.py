#!/usr/bin/env python3
"""
Settings Page - Manage credentials and configuration

This page allows users to configure API credentials, data paths,
and other settings for the BrightData application.
"""

import streamlit as st
import yaml
import requests
from pathlib import Path
import sys
from datetime import datetime

# Add the util directory to the path
sys.path.append(str(Path(__file__).parent.parent / "util"))

try:
    from util.config import get_brightdata_api_key, get_secret
except ImportError as e:
    st.error(f"❌ Could not import utilities: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Settings - BrightData Manager",
    page_icon="⚙️",
    layout="wide"
)

def load_secrets():
    """Load secrets from secrets.yaml file"""
    secrets_file = Path("secrets.yaml")
    if secrets_file.exists():
        with open(secrets_file, 'r') as f:
            return yaml.safe_load(f)
    return {}

def save_secrets(secrets):
    """Save secrets to secrets.yaml file"""
    secrets_file = Path("secrets.yaml")
    with open(secrets_file, 'w') as f:
        yaml.dump(secrets, f, default_flow_style=False, indent=2)

def test_api_key(api_key):
    """Test if API key is valid by making a test request"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Test with a simple filter request using the correct payload format
        # This matches the format used by BrightDataFilter.search_data()
        test_payload = {
            "dataset_id": "gd_l7q7dkf244hwjntr0",  # Amazon Products dataset
            "records_limit": 1,
            "filter": {
                "name": "title",
                "operator": "=", 
                "value": "test"
            }
        }
        
        response = requests.post(
            "https://api.brightdata.com/datasets/filter",
            headers=headers,
            json=test_payload,
            timeout=10
        )
        
        # Accept both 200 (success) and 202 (accepted/processing)
        if response.status_code in [200, 202]:
            return True, response.status_code, "API key is valid"
        else:
            return False, response.status_code, response.text
            
    except requests.exceptions.Timeout:
        return False, 0, "Request timeout - API may be slow"
    except requests.exceptions.ConnectionError:
        return False, 0, "Connection error - check your internet connection"
    except Exception as e:
        return False, 0, str(e)

def main():
    """Main settings interface"""
    
    st.title("⚙️ Settings")
    st.markdown("Configure your BrightData API credentials and application settings")
    
    # Load current settings
    secrets = load_secrets()
    brightdata_config = secrets.get('brightdata', {})
    
    # Current settings display
    st.header("📋 Current Settings")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        api_key = brightdata_config.get('api_key', 'Not configured')
        if api_key != 'Not configured':
            masked_key = api_key[:8] + "..." + api_key[-4:] if len(api_key) > 12 else "***"
            st.metric("API Key", masked_key)
        else:
            st.metric("API Key", "Not configured")
    
    with col2:
        base_url = brightdata_config.get('base_url', 'https://api.brightdata.com/datasets')
        st.metric("Base URL", base_url)
    
    with col3:
        data_path = brightdata_config.get('data_path', 'data')
        st.metric("Data Path", data_path)
    
    st.divider()
    
    # Configuration form
    st.header("🔧 Configuration")
    
    with st.form("settings_form"):
        st.subheader("API Credentials")
        
        # API Key input
        current_api_key = brightdata_config.get('api_key', '')
        api_key = st.text_input(
            "BrightData API Key:",
            value=current_api_key,
            type="password",
            help="Enter your BrightData API key. You can find this in your BrightData dashboard.",
            placeholder="Enter your API key here..."
        )
        
        # Data path input
        st.subheader("Data Configuration")
        data_path = st.text_input(
            "Data Path:",
            value=brightdata_config.get('data_path', 'data'),
            help="Directory path where data files will be stored",
            placeholder="data"
        )
        
        # Base URL input
        base_url = st.text_input(
            "Base URL:",
            value=brightdata_config.get('base_url', 'https://api.brightdata.com/datasets'),
            help="BrightData API base URL",
            placeholder="https://api.brightdata.com/datasets"
        )
        
        # Form buttons
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            save_button = st.form_submit_button("💾 Save Settings", type="primary")
        
        with col2:
            test_button = st.form_submit_button("🧪 Test API Key")
        
        with col3:
            reset_button = st.form_submit_button("🔄 Reset to Defaults")
        
        # Handle form submissions
        if save_button:
            if not api_key:
                st.error("❌ API key is required")
            else:
                # Update secrets
                if 'brightdata' not in secrets:
                    secrets['brightdata'] = {}
                
                secrets['brightdata']['api_key'] = api_key
                secrets['brightdata']['data_path'] = data_path
                secrets['brightdata']['base_url'] = base_url
                
                try:
                    save_secrets(secrets)
                    st.success("✅ Settings saved successfully!")
                    st.info("🔄 Please refresh the page to see updated settings")
                except Exception as e:
                    st.error(f"❌ Failed to save settings: {e}")
        
        if test_button:
            if not api_key:
                st.error("❌ Please enter an API key first")
            else:
                with st.spinner("Testing API key..."):
                    is_valid, status_code, response_text = test_api_key(api_key)
                    
                    if is_valid:
                        st.success("✅ API key is valid!")
                        st.info("🎉 You can now use the Query Builder and Snapshot Viewer")
                    else:
                        st.error(f"❌ API key test failed (HTTP {status_code})")
                        st.error(f"Response: {response_text}")
                        st.info("💡 Please check your API key in the BrightData dashboard")
        
        if reset_button:
            # Reset to default values
            if 'brightdata' not in secrets:
                secrets['brightdata'] = {}
            
            secrets['brightdata']['api_key'] = ''
            secrets['brightdata']['data_path'] = 'data'
            secrets['brightdata']['base_url'] = 'https://api.brightdata.com/datasets'
            
            try:
                save_secrets(secrets)
                st.success("✅ Settings reset to defaults!")
                st.info("🔄 Please refresh the page to see updated settings")
            except Exception as e:
                st.error(f"❌ Failed to reset settings: {e}")
    
    st.divider()
    
    # Security information
    st.header("🔒 Security Information")
    
    st.info("""
    **Security Notes:**
    - Your API key is stored locally in `secrets.yaml`
    - The `secrets.yaml` file is excluded from version control (git-ignored)
    - Never share your API key with others
    - Keep your `secrets.yaml` file secure and backed up
    """)
    
    # File status
    st.subheader("📁 File Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        secrets_file = Path("secrets.yaml")
        if secrets_file.exists():
            st.success("✅ secrets.yaml file exists")
            st.caption(f"Last modified: {datetime.fromtimestamp(secrets_file.stat().st_mtime)}")
        else:
            st.warning("⚠️ secrets.yaml file not found")
    
    with col2:
        data_dir = Path(data_path)
        if data_dir.exists():
            st.success("✅ Data directory exists")
        else:
            st.warning("⚠️ Data directory not found")
            st.caption("The directory will be created when needed")
    
    # Advanced settings
    with st.expander("🔧 Advanced Settings"):
        st.subheader("Environment Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            debug_mode = st.checkbox(
                "Debug Mode",
                value=secrets.get('environment', {}).get('debug', False),
                help="Enable debug logging"
            )
        
        with col2:
            log_level = st.selectbox(
                "Log Level",
                options=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                index=1,
                help="Set the logging level"
            )
        
        if st.button("💾 Save Advanced Settings"):
            if 'environment' not in secrets:
                secrets['environment'] = {}
            
            secrets['environment']['debug'] = debug_mode
            secrets['environment']['log_level'] = log_level
            
            try:
                save_secrets(secrets)
                st.success("✅ Advanced settings saved!")
            except Exception as e:
                st.error(f"❌ Failed to save advanced settings: {e}")
    
    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 2rem;'>
        <p>BrightData Manager Settings | Configuration saved locally</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
