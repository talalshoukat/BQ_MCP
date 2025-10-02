# BigQuery MCP Agent

A Model Context Protocol (MCP) agent built with Google ADK that provides intelligent BigQuery data analysis capabilities using natural language queries.

## Features

- **Natural Language Queries**: Ask questions about your BigQuery data in plain English
- **MCP Tool Integration**: Uses BigQuery tools from the genai-toolbox repository
- **Google ADK Integration**: Built with Google's Agent Development Kit
- **Comprehensive Analysis**: Supports data exploration, statistical analysis, and trend analysis
- **Interactive Mode**: Command-line interface for real-time querying

## Available BigQuery MCP Tools

1. **execute_sql** - Execute SQL queries directly on BigQuery
2. **get_table_info** - Get table schema and metadata
3. **get_dataset_info** - Get dataset information
4. **list_tables** - List all tables in a dataset

## Prerequisites

- Python 3.8+
- Google Cloud credentials configured
- Access to BigQuery datasets

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your BigQuery settings in `config.yaml`:
   ```yaml
   bigquery:
     project_id: "your-gcp-project-id"
     dataset_id: "your_dataset"
     location: "US"
   ```

4. Ensure your Google Cloud credentials are configured:
   ```bash
   gcloud auth application-default login
   ```

## Usage

### Interactive Mode
```bash
python main.py
```

### Single Query Mode
```bash
python main.py "What are the top 10 products by sales?"
```

## Example Queries

- **Data Exploration**:
  - "Show me the schema of the users table"
  - "What columns are available in the orders dataset?"
  - "List all tables in the analytics dataset"

- **Statistical Analysis**:
  - "What are the top 10 products by sales?"
  - "How many orders were placed last month?"
  - "What's the average order value by region?"

- **Trend Analysis**:
  - "Show me sales trends over the last 6 months"
  - "How has user engagement changed over time?"

## Configuration

Edit `config.yaml` to customize:

- **Agent settings**: Name, description, model
- **BigQuery settings**: Project ID, dataset, location
- **Tool configuration**: Available BigQuery tools
- **Logging**: Log level and format

## Architecture

The agent follows the MCP (Model Context Protocol) pattern:

1. **BigQueryMCPTool**: Wraps BigQuery operations as MCP tools
2. **BigQueryMCPAgent**: Google ADK agent that orchestrates tools
3. **Natural Language Processing**: Converts user questions to BigQuery operations
4. **Response Generation**: Provides insights and analysis

## Inspired by

This implementation takes inspiration from the `fraud_subagent` pattern used in fraud detection systems, adapted for general BigQuery data analysis using MCP tools.

## License

MIT License
