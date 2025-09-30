"""
Fraud Data Analysis Agent using Google ADK with Built-in BigQuery Integration
Leverages ADK's native BigQuery tools for comprehensive fraud data analysis
"""

import json
import logging
from typing import Dict, Any, Optional
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.bigquery import BigQueryToolset, BigQueryCredentialsConfig, BigQueryToolSettings
from google.auth import default
import litellm

from ..configs.config import ConfigFactory, SubAgentsEnum

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
config = ConfigFactory.parse_yaml_with_hydra(overrides=[])
AGENT_NAME = SubAgentsEnum.fraud_agent

# Configure LiteLLM
litellm.ssl_verify = config.verify_ssl
litellm.use_litellm_proxy = True

# Initialize LLM
llm = LiteLlm(model=config.llm.model_name)

# BigQuery Configuration
PROJECT_ID = config.subagents[AGENT_NAME].get("project_id", "your-gcp-project-id")
DATASET_ID = config.subagents[AGENT_NAME].get("dataset_id", "fraud_data")
TABLE_NAME = config.subagents[AGENT_NAME].get("table_name", "fraud_records")
TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}"

# Setup BigQuery credentials and settings
try:
    credentials, _ = default()
    credentials_config = BigQueryCredentialsConfig(credentials=credentials)
    tool_settings = BigQueryToolSettings()
    
    # Initialize BigQuery toolset with ADK built-in tools
    bigquery_toolset = BigQueryToolset(
        credentials_config=credentials_config,
        bigquery_tool_settings=tool_settings
    )
    
    logger.info("BigQuery toolset initialized successfully")
    
except Exception as e:
    logger.error(f"Failed to setup BigQuery: {e}")
    bigquery_toolset = None

# Create tools list - using only ADK built-in BigQuery tools
tools = []

# Add BigQuery toolset if available
if bigquery_toolset:
    tools.append(bigquery_toolset)
    logger.info("BigQuery toolset added to fraud agent")
else:
    logger.warning("BigQuery toolset not available - fraud agent will have limited functionality")

# Create the Fraud Agent
fraud_agent = Agent(
    model=llm,
    name=AGENT_NAME,
    description="Advanced fraud data analysis agent with BigQuery integration and dynamic query generation",
    instruction=f"""
    You are an expert fraud data analyst with access to a comprehensive aggregated fraud dataset using Google ADK's built-in BigQuery tools.
    
    **Your Data Source:**
    - Project: {PROJECT_ID}
    - Dataset: {DATASET_ID}
    - Table: {TABLE_NAME}
    - Full Table ID: {TABLE_ID}
    
    **Available BigQuery Tools:**
    You have access to ADK's built-in BigQuery toolset which provides:
    - `execute_sql`: Execute SQL queries directly on BigQuery
    - `get_table_metadata`: Get table schema and metadata
    - `list_tables`: List available tables in the dataset
    - `get_query_results`: Retrieve query results
    
    **Known Fraud Dimensions in the Aggregated Table:**
    - gender, age_bracket, income_bracket, education, occupation
    - company, region, fraud_type, fraud_amount, fraud_date
    - fraud_id, created_at, updated_at
    
    **Analysis Capabilities:**
    - **Demographic Analysis**: Analyze fraud by gender, age, education, occupation
    - **Geographic Analysis**: Analyze fraud by region, location
    - **Temporal Analysis**: Analyze fraud trends over time
    - **Company Analysis**: Analyze fraud by company/organization
    - **Comprehensive Analysis**: Overall fraud statistics and metrics
    
    **How to Use BigQuery Tools:**
    1. **For SQL Queries**: Use `execute_sql` with your SQL query
    2. **For Table Info**: Use `get_table_metadata` to understand table structure
    3. **For Data Exploration**: Use `list_tables` to see available tables
    
    **Example SQL Queries:**
    - Count total fraud cases: `SELECT COUNT(*) FROM `{TABLE_ID}``
    - Fraud by gender: `SELECT gender, COUNT(*) as count FROM `{TABLE_ID}` GROUP BY gender ORDER BY count DESC`
    - Fraud by region: `SELECT region, COUNT(*) as count FROM `{TABLE_ID}` GROUP BY region ORDER BY count DESC`
    - Monthly trends: `SELECT EXTRACT(YEAR FROM fraud_date) as year, EXTRACT(MONTH FROM fraud_date) as month, COUNT(*) as count FROM `{TABLE_ID}` GROUP BY year, month ORDER BY year DESC, month DESC`
    
    **Best Practices:**
    - Always use proper BigQuery SQL syntax
    - Include appropriate WHERE clauses for filtering
    - Use GROUP BY for aggregations
    - Order results logically (DESC for counts, ASC for dates)
    - Limit results to reasonable numbers (use LIMIT 100 for large result sets)
    - Provide clear, actionable insights from fraud data
    - Use visual descriptions for data patterns and trends
    - Explain statistical significance and patterns in fraud data
    
    **Response Format:**
    - Provide clear explanations of findings
    - Include relevant statistics and percentages
    - Suggest actionable insights for fraud prevention
    - Highlight key patterns and anomalies
    - Show the SQL query used when relevant
    """,
    tools=tools,
)
