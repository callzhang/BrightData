# Bright Data Marketplace Dataset API - Filter Dataset (BETA)

## Overview

The Filter Dataset API allows you to create dataset snapshots based on provided filters. This endpoint starts an async job to filter the dataset and create a snapshot with filtered data in your account.

### Key Features

- **Async Processing**: Creates filtered snapshots asynchronously
- **Time Limit**: Maximum 5 minutes for job completion
- **Charges**: Subject to charges based on snapshot size and record price
- **Nesting Depth**: Maximum 3 levels of filter group nesting

## Authentication

Use your Bright Data API Key as a Bearer token in the Authorization header.

```
Authorization: Bearer <your_api_key>
```

Get your API key from: https://brightdata.com/cp/setting/users

## Endpoint

```
POST https://api.brightdata.com/datasets/filter
```

## Request Modes

### 1. JSON Mode (No File Uploads)

Use this mode when you are not uploading any files.

**Headers:**
```
Content-Type: application/json
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "dataset_id": "gd_l1viktl72bvl7bjuj0",
  "records_limit": 1000,
  "filter": {
    "name": "name",
    "operator": "=",
    "value": "John"
  }
}
```

**cURL Example:**
```bash
curl --request POST \
  --url https://api.brightdata.com/datasets/filter \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: application/json' \
  --data '{
    "dataset_id": "gd_l1viktl72bvl7bjuj0",
    "records_limit": 100,
    "filter": {
      "name": "name",
      "operator": "=",
      "value": "John"
    }
  }'
```

### 2. Multipart/Form-Data Mode (File Uploads)

Use this mode when uploading CSV or JSON files containing filter values.

**Headers:**
```
Content-Type: multipart/form-data
Authorization: Bearer <token>
```

**Query Parameters:**
- `dataset_id`: ID of the dataset to filter (required)
- `records_limit`: Limit the number of records in the snapshot

**Form Data:**
- `filter`: JSON string containing the filter configuration
- `files[]`: Uploaded CSV or JSON files

**cURL Example:**
```bash
curl --request POST \
  --url "https://api.brightdata.com/datasets/filter?dataset_id=gd_l1vijqt9jfj7olije&records_limit=100" \
  --header 'Authorization: Bearer <token>' \
  --header 'Content-Type: multipart/form-data' \
  --form 'filter={"operator":"and","filters":[{"name":"industries:value","operator":"includes","value":"industries.csv"}]}' \
  --form 'files[]=@/path/to/industries.csv'
```

## Filter Syntax

### Operators

| Operator | Field Types | Description |
|----------|-------------|-------------|
| `=` | Any | Equal to |
| `!=` | Any | Not equal to |
| `<` | Number, Date | Lower than |
| `<=` | Number, Date | Lower than or equal |
| `>` | Number, Date | Greater than |
| `>=` | Number, Date | Greater than or equal |
| `in` | Any | Tests if field value is equal to any of the values provided in filter's value |
| `not_in` | Any | Tests if field value is not equal to all of the values provided in filter's value |
| `includes` | Array, Text | Tests if the field value contains the filter value. For single string, matches records where field contains that string. For array of strings, matches records where field contains at least one string from the array. |
| `not_includes` | Array, Text | Tests if the field value does not contain the filter value. For single string, matches records where field does not contain that string. For array of strings, matches records where field does not contain any strings from the array. |
| `array_includes` | Array | Tests if filter value is in field value (exact match) |
| `not_array_includes` | Array | Tests if filter value is not in field value (exact match) |
| `is_null` | Any | Tests if the field value is equal to NULL. Operator does not accept any value. |
| `is_not_null` | Any | Tests if the field value is not equal to NULL. Operator does not accept any value. |

### Combining Multiple Filters

Multiple field filters can be combined using logical operators `and` and `or`. Maximum nesting depth is 3 levels.

**Filter Group Example:**
```json
{
  "operator": "and",
  "filters": [
    {
      "name": "reviews_count",
      "operator": ">",
      "value": "200"
    },
    {
      "name": "rating",
      "operator": ">",
      "value": "4.5"
    }
  ]
}
```

## Request Parameters

### Query Parameters (Multipart Mode Only)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dataset_id` | string | Yes | ID of the dataset to filter |
| `records_limit` | integer | No | Limit the number of records to be included in the snapshot |

### Request Body Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `dataset_id` | string | Yes (JSON mode) | ID of the dataset to filter |
| `records_limit` | integer | No | Limit the number of records to be included in the snapshot |
| `filter` | object | Yes | Filter configuration object |

## Response

### Success Response (200)

```json
{
  "snapshot_id": "<string>"
}
```

The response contains a `snapshot_id` that you can use to track the progress and retrieve the filtered dataset snapshot.

### Error Responses

- **400**: Bad Request
- **402**: Payment Required
- **422**: Unprocessable Entity
- **429**: Too Many Requests

## Usage Notes

1. **Job Processing**: The filtering job runs asynchronously and may take up to 5 minutes to complete
2. **Charges**: Creating dataset snapshots is subject to charges based on snapshot size and record price
3. **File Uploads**: When using multipart mode, ensure files are properly formatted CSV or JSON
4. **Filter Complexity**: Keep filter nesting to a maximum of 3 levels for optimal performance
5. **Rate Limits**: Be mindful of API rate limits to avoid 429 errors

## Example Use Cases

1. **Simple Field Filter**: Filter products by name
2. **Range Filter**: Filter products by price range
3. **Array Filter**: Filter products by multiple categories
4. **Complex Logic**: Combine multiple conditions with AND/OR operators
5. **File-based Filtering**: Upload lists of values to filter against

## Related Documentation

- [Get Dataset Metadata](https://docs.brightdata.com/api-reference/marketplace-dataset-api/get-dataset-metadata)
- [Get Snapshot Metadata](https://docs.brightdata.com/api-reference/marketplace-dataset-api/get-snapshot-metadata)
- [Snapshot Content](https://docs.brightdata.com/api-reference/marketplace-dataset-api/snapshot-content)
