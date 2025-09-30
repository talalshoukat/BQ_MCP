"""
Fraud Data Analysis Agent using Google ADK with BigQuery Integration
Provides comprehensive fraud data analysis capabilities with dynamic query generation
"""

import json
import logging
from typing import Dict, Any, Optional
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import GoogleTool
from google.adk.tools.bigquery import BigQueryToolset, BigQueryCredentialsConfig, BigQueryToolSettings
from google.auth import default
import litellm

from ..configs.config import ConfigFactory, SubAgentsEnum
from ...tools.bigquery_mcp_tools import (
    generate_fraud_query, 
    execute_fraud_query,
    get_fraud_statistics
)

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

# BigQuery Configuration - Direct table reference
PROJECT_ID = config.subagents[AGENT_NAME].get("project_id", "your-gcp-project-id")
DATASET_ID = config.subagents[AGENT_NAME].get("dataset_id", "fraud_data")
TABLE_NAME = config.subagents[AGENT_NAME].get("table_name", "fraud_records")
TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_NAME}"

# Setup BigQuery credentials and settings
try:
    credentials, _ = default()
    credentials_config = BigQueryCredentialsConfig(credentials=credentials)
    tool_settings = BigQueryToolSettings()
except Exception as e:
    logger.error(f"Failed to setup BigQuery credentials: {e}")
    credentials_config = None
    tool_settings = None

# Initialize BigQuery toolset
bigquery_toolset = None
if credentials_config and tool_settings:
    try:
        bigquery_toolset = BigQueryToolset(
            credentials_config=credentials_config,
            bigquery_tool_settings=tool_settings
        )
    except Exception as e:
        logger.error(f"Failed to initialize BigQuery toolset: {e}")


def generate_dynamic_query(user_request: str) -> str:
    """
    Generate dynamic BigQuery query using LLM based on user request
    Args:
        user_request: Natural language request from user
    Returns:
        JSON string containing generated query and metadata
    """
    try:
        result = generate_fraud_query(PROJECT_ID, DATASET_ID, TABLE_NAME, user_request)
        return result
    except Exception as e:
        logger.error(f"Error generating query: {e}")
        return json.dumps({"error": str(e)}, indent=2)


def execute_dynamic_query(query: str) -> str:
    """
    Execute BigQuery query and return results
    Args:
        query: SQL query to execute
    Returns:
        JSON string containing query results
    """
    try:
        result = execute_fraud_query(PROJECT_ID, DATASET_ID, TABLE_NAME, query)
        return result
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        return json.dumps({"error": str(e)}, indent=2)


def get_fraud_analytics(dimension: str = None) -> str:
    """
    Get fraud analytics and statistics
    Args:
        dimension: Dimension to analyze (gender, age_bracket, region, etc.)
    Returns:
        JSON string containing fraud analytics
    """
    try:
        result = get_fraud_statistics(PROJECT_ID, DATASET_ID, TABLE_NAME, dimension)
        return result
    except Exception as e:
        logger.error(f"Error getting fraud analytics: {e}")
        return json.dumps({"error": str(e)}, indent=2)


def analyze_fraud_patterns(analysis_type: str, filters: str = None) -> str:
    """
    Analyze fraud patterns based on different dimensions using LLM-generated queries
    Args:
        analysis_type: Type of analysis (demographic, temporal, geographic, etc.)
        filters: Optional filters to apply
    Returns:
        JSON string containing fraud pattern analysis
    """
    try:
        # Create a natural language request for the LLM
        user_request = f"Analyze fraud patterns for {analysis_type} analysis"
        if filters:
            user_request += f" with filters: {filters}"
        
        # Use LLM to generate the query
        query_result = generate_dynamic_query(user_request)
        query_data = json.loads(query_result)
        
        if "error" in query_data:
            return query_result
        
        # Execute the generated query
        result = execute_dynamic_query(query_data["query"])
        return result
        
    except Exception as e:
        logger.error(f"Error analyzing fraud patterns: {e}")
        return json.dumps({"error": str(e)}, indent=2)


# Create Google Tools for ADK integration
tools = []

# Add BigQuery toolset if available
if bigquery_toolset:
    tools.append(bigquery_toolset)

# Add custom MCP tools (simplified - no schema discovery)
tools.extend([
    GoogleTool(
        func=generate_dynamic_query,
        credentials_config=credentials_config,
        tool_settings=tool_settings,
    ),
    GoogleTool(
        func=execute_dynamic_query,
        credentials_config=credentials_config,
        tool_settings=tool_settings,
    ),
    GoogleTool(
        func=get_fraud_analytics,
        credentials_config=credentials_config,
        tool_settings=tool_settings,
    ),
    GoogleTool(
        func=analyze_fraud_patterns,
        credentials_config=credentials_config,
        tool_settings=tool_settings,
    ),
])

# Create the Fraud Agent
fraud_agent = Agent(
    model=llm,
    name=AGENT_NAME,
    description="Advanced fraud data analysis agent with BigQuery integration and dynamic query generation",
    instruction="""
    You are an expert fraud data analyst with access to a comprehensive aggregated fraud dataset. 
    Your capabilities include:
    
    1. **Dynamic Query Generation**: Use `generate_dynamic_query(user_request)` to create SQL queries using LLM based on natural language requests
    2. **Query Execution**: Use `execute_dynamic_query(query)` to run BigQuery queries and get results
    3. **Fraud Analytics**: Use `get_fraud_analytics(dimension)` to get statistics for specific dimensions
    4. **Pattern Analysis**: Use `analyze_fraud_patterns(analysis_type, filters)` for comprehensive fraud pattern analysis
    
    **Available Analysis Types:**
    - demographic: Analyze fraud by gender, age, education, occupation
    - geographic: Analyze fraud by region, location
    - temporal: Analyze fraud trends over time
    - company: Analyze fraud by company/organization
    - comprehensive: Overall fraud statistics and metrics
    
    **Known Fraud Dimensions in the Aggregated Table:**
    - gender, age_bracket, income_bracket, education, occupation
    - company, region, fraud_type, fraud_amount, fraud_date
    - fraud_id, created_at, updated_at
    
    **Best Practices:**
    - Use natural language to describe what you want to analyze
    - The system will automatically generate appropriate SQL queries using LLM
    - Provide clear, actionable insights from fraud data
    - Use visual descriptions for data patterns and trends
    - Explain statistical significance and patterns in fraud data
    
    **Response Format:**
    - Provide clear explanations of findings
    - Include relevant statistics and percentages
    - Suggest actionable insights for fraud prevention
    - Highlight key patterns and anomalies
    """,
    tools=tools,
)
