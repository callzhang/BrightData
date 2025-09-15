# 📊 BrightData Snapshot Manager

A comprehensive utility for managing local BrightData snapshot records, monitoring processing status, and handling downloads.

## 🎯 Features

- **📋 List Records**: View all local snapshot records in a formatted table
- **🔍 Status Checking**: Check current status of all snapshots from BrightData API
- **📥 Download Management**: Download ready snapshots (incurs fees)
- **👁️ Data Viewing**: View downloaded data locally
- **⏳ Progress Monitoring**: Monitor processing snapshots in real-time
- **💾 Persistent Storage**: All records stored in JSON files with snapshot ID as filename

## 🚀 Quick Start

### 1. Create Some Snapshots First
```python
from util import BrightDataFilter, AMAZON_FIELDS as AF, get_brightdata_api_key

# Initialize filter
api_key = get_brightdata_api_key()
amazon_filter = BrightDataFilter(api_key, "gd_l7q7dkf244hwjntr0", "snapshot_records")

# Submit a filter
filter = (AF.rating >= 4.0) & (AF.reviews_count > 100)
response = amazon_filter.search_data(filter, records_limit=1000)
print(f"Snapshot ID: {response['snapshot_id']}")
```

### 2. Use the Snapshot Manager
```bash
# List all snapshot records
python snapshot_manager.py --list

# Check status of all snapshots
python snapshot_manager.py --status

# Download ready snapshots
python snapshot_manager.py --download

# View downloaded data
python snapshot_manager.py --view snap_abc123

# Monitor processing snapshots
python snapshot_manager.py --monitor
```

## 📖 Command Reference

### List Records (`--list`, `-l`)
Shows all local snapshot records in a formatted table:
```
📊 Found 2 snapshot records:
========================================================================================================================
Snapshot ID          Status       Dataset              Limit    Cost     Submitted           
========================================================================================================================
snap_mflgxpdw1xqp0... ⏳ scheduled  gd_l7q7dkf244hwjnt... 100      $0       2025-09-15T11:39:41 
snap_abc123def456... ✅ ready      gd_l7q7dkf244hwjnt... 1000     $5.50    2025-09-15T10:15:30 
========================================================================================================================
```

### Check Status (`--status`, `-s`)
Checks current status of all snapshots from BrightData API:
```
🔍 Checking status of 2 snapshots...

[1/2] Checking snap_mflgxpdw1xqp0hpiav...
📊 Status: scheduled
💰 Cost: $0
📈 Records: N/A
💾 Size: N/A bytes
⏳ Still processing...

[2/2] Checking snap_abc123def456...
📊 Status: ready
💰 Cost: $5.50
📈 Records: 847
💾 Size: 2048576 bytes
✅ Ready for download!
```

### Download Ready Snapshots (`--download`, `-d`)
Downloads all snapshots with "ready" status:
```
📥 Found 1 ready snapshots

--- Downloading snap_abc123def456 ---
📥 Downloading snap_abc123def456...
✅ Downloaded to: downloads/snap_abc123def456.json
```

### View Downloaded Data (`--view`, `-v`)
Views downloaded data for a specific snapshot:
```bash
python snapshot_manager.py --view snap_abc123def456 --lines 50
```

### Monitor Processing (`--monitor`, `-m`)
Continuously monitors all processing snapshots:
```
🔍 Monitoring 1 processing snapshots...
Press Ctrl+C to stop monitoring

⏰ 11:45:30 - Checking status...
  snap_mflgxpdw1xqp0hpiav: scheduled
⏳ Waiting 30 seconds...

⏰ 11:46:00 - Checking status...
  snap_mflgxpdw1xqp0hpiav: building
⏳ Waiting 30 seconds...

⏰ 11:46:30 - Checking status...
  snap_mflgxpdw1xqp0hpiav: ready
    ✅ snap_mflgxpdw1xqp0hpiav is ready for download!
```

## 📁 File Structure

### Local Record Format
Each snapshot record is stored as `{snapshot_id}.json`:
```json
{
  "snapshot_id": "snap_mflgxpdw1xqp0hpiav",
  "submission_time": "2025-09-15T11:39:41.293571",
  "dataset_id": "gd_l7q7dkf244hwjntr0",
  "records_limit": 100,
  "filter_criteria": {
    "operator": "and",
    "filters": [
      {
        "name": "rating",
        "operator": ">=",
        "value": "4.0"
      }
    ]
  },
  "status": "scheduled",
  "metadata": {
    "id": "snap_mflgxpdw1xqp0hpiav",
    "created": "2025-09-15T18:39:41.203Z",
    "status": "scheduled",
    "dataset_id": "gd_l7q7dkf244hwjntr0",
    "customer_id": "hl_a6e6d183",
    "cost": 0,
    "initiation_type": "filter_api_snapshot"
  },
  "completion_time": null,
  "error": null,
  "downloaded_file": "downloads/snap_mflgxpdw1xqp0hpiav.json",
  "download_time": "2025-09-15T12:15:30.123456"
}
```

### Directory Structure
```
project/
├── snapshot_records/          # Local snapshot records
│   ├── snap_abc123.json
│   └── snap_def456.json
├── downloads/                 # Downloaded snapshot data
│   ├── snap_abc123.json
│   └── snap_def456.csv
└── snapshot_manager.py        # Main script
```

## 🔧 Configuration Options

### Storage Directory
```bash
python snapshot_manager.py --storage-dir my_snapshots --list
```

### Output Directory for Downloads
```bash
python snapshot_manager.py --download --output-dir my_downloads
```

### Number of Lines to Show
```bash
python snapshot_manager.py --view snap_abc123 --lines 100
```

## 📊 Status Meanings

| Status | Icon | Description |
|--------|------|-------------|
| `submitted` | 📤 | Filter submitted, waiting for processing |
| `scheduled` | ⏳ | Job queued for processing |
| `building` | 🔨 | Data being filtered and processed |
| `ready` | ✅ | Snapshot complete, ready for download |
| `failed` | ❌ | Processing failed with error |

## 💰 Cost Management

- **Free**: Status checking and metadata retrieval
- **Paid**: Downloading ready snapshots (cost shown in metadata)
- **No Cost**: Viewing already downloaded data

## 🔄 Workflow Example

1. **Submit Filters**: Use the BrightData filter system to submit filters
2. **Monitor Progress**: Use `--monitor` to watch processing
3. **Check Status**: Use `--status` to see current state
4. **Download Ready**: Use `--download` when snapshots are ready
5. **View Data**: Use `--view` to examine downloaded data

## 🛠️ Troubleshooting

### No Records Found
```
❌ Storage directory 'snapshot_records' not found
💡 Run some filters first to create snapshot records
```
**Solution**: Submit some filters using the BrightData filter system first.

### Download Failed
```
❌ Snapshot not ready. Status: scheduled
```
**Solution**: Wait for the snapshot to reach "ready" status before downloading.

### API Errors
```
❌ Error checking status: HTTP 401: Unauthorized
```
**Solution**: Check your BrightData API key in `secrets.yaml`.

## 🎯 Use Cases

### Research Projects
- Submit multiple filters for different research questions
- Monitor all processing in one place
- Download and analyze results systematically

### Business Intelligence
- Track filter costs and processing times
- Maintain audit trail of all data requests
- Batch download multiple datasets

### Development & Testing
- Test filter logic with small datasets
- Monitor API performance and reliability
- Debug filter issues with complete records

## 🔗 Integration

The snapshot manager integrates seamlessly with the BrightData filter system:

```python
from util import BrightDataFilter, AMAZON_FIELDS as AF, get_brightdata_api_key

# Submit filter (automatically creates local record)
api_key = get_brightdata_api_key()
amazon_filter = BrightDataFilter(api_key, "gd_l7q7dkf244hwjntr0", "snapshot_records")
response = amazon_filter.search_data(filter, records_limit=1000)

# Use snapshot manager to monitor and download
# python snapshot_manager.py --status
# python snapshot_manager.py --download
```

This provides a complete end-to-end solution for BrightData snapshot management! 🚀
