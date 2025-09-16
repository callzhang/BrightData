# 📊 BrightData Snapshot Viewer - Web UI

A simple, intuitive web interface for viewing and analyzing your locally stored BrightData snapshots.

## 🚀 Quick Start

### Option 1: Easy Launch (Recommended)
```bash
python launch_viewer.py
```

### Option 2: Manual Launch
```bash
# Install requirements
pip install -r requirements_ui.txt

# Launch the app
streamlit run snapshot_viewer.py
```

The app will open in your browser at `http://localhost:8501`

## 🎯 Features

### 📋 Snapshot Management
- **View all snapshots**: See all your submitted snapshots in one place
- **Status tracking**: Monitor processing status with color-coded badges
- **Quick selection**: Easy dropdown to switch between snapshots
- **Metadata display**: View submission time, cost, and other details

### 📊 Data Analysis
- **Interactive data preview**: Browse your data in a clean table format
- **Statistical summaries**: Automatic descriptive statistics for numeric columns
- **Data quality insights**: Missing data analysis and data type information
- **Column information**: Detailed breakdown of all columns

### 📈 Visualizations
- **Histograms**: Distribution plots for numeric variables
- **Scatter plots**: Relationship analysis between variables
- **Bar charts**: Categorical data analysis
- **Interactive charts**: Powered by Plotly for zooming and exploration

### 🛠️ Operations
- **Download integration**: Direct links to download missing data
- **Filter criteria display**: View the exact filters used for each snapshot
- **Status monitoring**: Real-time status updates
- **Data export**: Easy access to your analyzed data

## 📱 Interface Overview

### Sidebar
- **Snapshot Selection**: Choose from all available snapshots
- **Status Overview**: Quick metrics on completed/processing/failed snapshots

### Main Area
- **Snapshot Details**: Complete information about the selected snapshot
- **Filter Criteria**: JSON display of the original filter conditions
- **Data Analysis**: Interactive data exploration and visualization
- **Actions**: Download and management operations

## 🎨 Visual Features

### Status Badges
- 🟢 **COMPLETED**: Data ready for analysis
- 🟡 **PROCESSING**: Currently being processed
- 🔴 **FAILED**: Processing failed
- 🔵 **SUBMITTED**: Waiting to be processed

### Metrics Dashboard
- Total snapshots count
- Completed snapshots
- Processing snapshots
- Failed snapshots

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web framework
- **Pandas**: Data manipulation
- **Plotly**: Interactive visualizations
- **PyYAML**: Configuration handling

### Data Sources
- **Snapshot Records**: `snapshot_records/*.json`
- **Downloaded Data**: `data/downloads/*.json`
- **Configuration**: `secrets.yaml`

### Browser Compatibility
- Chrome (recommended)
- Firefox
- Safari
- Edge

## 💡 Usage Tips

### For Data Scientists
1. **Start with overview**: Check the metrics dashboard for snapshot status
2. **Select your snapshot**: Use the sidebar to choose the data you want to analyze
3. **Explore the data**: Use the data preview and column information
4. **Create visualizations**: Select numeric columns for automatic charts
5. **Analyze categories**: Use the categorical analysis for text data

### For Project Managers
1. **Monitor progress**: Check the status badges and metrics
2. **Track costs**: View cost information for each snapshot
3. **Review filters**: Understand what data was requested
4. **Download status**: See which snapshots are ready for download

## 🚨 Troubleshooting

### Common Issues

**App won't start:**
```bash
# Check if you're in the right directory
ls snapshot_records/

# Install requirements
pip install -r requirements_ui.txt
```

**No snapshots shown:**
- Make sure you have submitted some filters first
- Check that `snapshot_records/` directory exists and contains JSON files

**Data not loading:**
- Ensure the snapshot data has been downloaded
- Check that `data/downloads/` directory contains the corresponding JSON files

**Visualizations not working:**
- Make sure your data has numeric columns for charts
- Check that Plotly is properly installed

### Getting Help
- Check the console output for error messages
- Ensure all dependencies are installed correctly
- Verify your data files are in the correct format

## 🔄 Integration with Existing Tools

### Snapshot Manager
The UI works alongside the existing snapshot manager:
```bash
# Download data using snapshot manager
python snapshot_manager.py -d

# Then view in the web UI
python launch_viewer.py
```

### Jupyter Notebooks
Use the UI for quick data exploration, then switch to Jupyter for advanced analysis:
```python
# In Jupyter, load the same data
import pandas as pd
df = pd.read_json("data/downloads/snap_xxx.json")
```

## 🎉 Benefits

- **No coding required**: Point-and-click interface
- **Real-time updates**: See status changes immediately
- **Professional visualizations**: Publication-ready charts
- **Data quality insights**: Automatic data profiling
- **Easy sharing**: Share the web interface with team members
- **Mobile friendly**: Works on tablets and phones

---

**Happy analyzing! 📊✨**

