# BigQuery MCP Agent - Quick Start Guide

## 🚀 Get Started in 3 Steps

### 1. Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Configure your BigQuery project
# Edit config.yaml with your project details
```

### 2. Configure Google Cloud
```bash
# Authenticate with Google Cloud
gcloud auth application-default login

# Set your project (optional)
gcloud config set project YOUR_PROJECT_ID
```

### 3. Run the Agent
```bash
# Interactive mode
python main.py

# Single query mode
python main.py "What are the top 10 products by sales?"
```

## 📋 Configuration

Edit `config.yaml`:
```yaml
bigquery:
  project_id: "your-gcp-project-id"  # Replace with your project
  dataset_id: "your_dataset"         # Replace with your dataset
  location: "US"                     # Your preferred location
```

## 🔧 Available Tools

1. **execute_sql** - Run SQL queries on BigQuery
2. **get_table_info** - Get table schema and metadata
3. **get_dataset_info** - Get dataset information
4. **list_tables** - List tables in a dataset

## 💡 Example Queries

- "Show me the schema of the users table"
- "What are the top 10 products by sales?"
- "How many records are in the orders dataset?"
- "List all tables in the analytics dataset"

## 🧪 Testing

```bash
# Run tests
python test_agent.py

# Run examples
python example_usage.py

# Run setup verification
python setup.py
```

## 📚 Key Features

- ✅ Uses Google ADK Agent framework
- ✅ Integrates BigQuery MCP tools
- ✅ Natural language query processing
- ✅ Interactive and programmatic interfaces
- ✅ Inspired by fraud_subagent patterns
- ✅ Comprehensive error handling

## 🆘 Troubleshooting

1. **Authentication issues**: Run `gcloud auth application-default login`
2. **Project not found**: Update `config.yaml` with correct project ID
3. **Permission denied**: Ensure your account has BigQuery access
4. **Import errors**: Run `pip install -r requirements.txt`

## 📖 Full Documentation

See `README.md` for complete documentation and advanced usage.
