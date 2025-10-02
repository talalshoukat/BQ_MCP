"""
BigQuery MCP Agent using Google ADK with BigQuery Tools Integration
Leverages MCP toolbox BigQuery tools for comprehensive data analysis
"""

import json
import logging
import yaml
from typing import Dict, Any, Optional, List
from pathlib import Path

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.cloud import bigquery
from google.auth import default
import litellm

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BigQueryMCPTool:
    """MCP Tool wrapper for BigQuery operations"""
    
    def __init__(self, client: bigquery.Client):
        self.client = client
    
    def execute_sql(self, query: str) -> Dict[str, Any]:
        """Execute SQL query and return results"""
        try:
            query_job = self.client.query(query)
            results = query_job.result()
            
            # Convert results to list of dictionaries
            rows = []
            for row in results:
                rows.append(dict(row))
            
            return {
                "success": True,
                "data": rows,
                "total_rows": len(rows),
                "query": query
            }
        except Exception as e:
            logger.error(f"Error executing SQL query: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
    
    def get_table_info(self, project_id: str, dataset_id: str, table_id: str) -> Dict[str, Any]:
        """Get table schema and metadata"""
        try:
            table_ref = f"{project_id}.{dataset_id}.{table_id}"
            table = self.client.get_table(table_ref)
            
            schema_info = []
            for field in table.schema:
                schema_info.append({
                    "name": field.name,
                    "type": field.field_type,
                    "mode": field.mode,
                    "description": field.description or ""
                })
            
            return {
                "success": True,
                "table_id": table_ref,
                "description": table.description or "",
                "num_rows": table.num_rows,
                "num_bytes": table.num_bytes,
                "created": str(table.created),
                "modified": str(table.modified),
                "schema": schema_info
            }
        except Exception as e:
            logger.error(f"Error getting table info: {e}")
            return {
                "success": False,
                "error": str(e),
                "table_id": f"{project_id}.{dataset_id}.{table_id}"
            }
    
    def get_dataset_info(self, project_id: str, dataset_id: str) -> Dict[str, Any]:
        """Get dataset information"""
        try:
            dataset_ref = f"{project_id}.{dataset_id}"
            dataset = self.client.get_dataset(dataset_ref)
            
            tables = list(self.client.list_tables(dataset_ref))
            table_list = [f"{table.project}.{table.dataset_id}.{table.table_id}" for table in tables]
            
            return {
                "success": True,
                "dataset_id": dataset_ref,
                "description": dataset.description or "",
                "location": dataset.location,
                "created": str(dataset.created),
                "modified": str(dataset.modified),
                "tables": table_list,
                "num_tables": len(table_list)
            }
        except Exception as e:
            logger.error(f"Error getting dataset info: {e}")
            return {
                "success": False,
                "error": str(e),
                "dataset_id": f"{project_id}.{dataset_id}"
            }
    
    def list_tables(self, project_id: str, dataset_id: str) -> Dict[str, Any]:
        """List all tables in a dataset"""
        try:
            dataset_ref = f"{project_id}.{dataset_id}"
            tables = list(self.client.list_tables(dataset_ref))
            
            table_list = []
            for table in tables:
                table_list.append({
                    "table_id": f"{table.project}.{table.dataset_id}.{table.table_id}",
                    "dataset_id": table.dataset_id,
                    "table_name": table.table_id
                })
            
            return {
                "success": True,
                "dataset_id": dataset_ref,
                "tables": table_list,
                "count": len(table_list)
            }
        except Exception as e:
            logger.error(f"Error listing tables: {e}")
            return {
                "success": False,
                "error": str(e),
                "dataset_id": f"{project_id}.{dataset_id}"
            }

class BigQueryMCPAgent:
    """BigQuery MCP Agent using Google ADK"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self._setup_llm()
        self._setup_bigquery()
        self._setup_tools()
        self._create_agent()
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                config = yaml.safe_load(file)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise
    
    def _setup_llm(self):
        """Setup the LLM model"""
        try:
            model_name = self.config.get('agent', {}).get('model', 'gemini-2.0-flash-exp')
            self.llm = LiteLlm(model=model_name)
            logger.info(f"LLM initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Error setting up LLM: {e}")
            raise
    
    def _setup_bigquery(self):
        """Setup BigQuery client"""
        try:
            # Use default credentials
            credentials, project = default()
            self.bigquery_client = bigquery.Client(credentials=credentials, project=project)
            logger.info(f"BigQuery client initialized with project: {project}")
        except Exception as e:
            logger.error(f"Error setting up BigQuery client: {e}")
            raise
    
    def _setup_tools(self):
        """Setup BigQuery MCP tools"""
        self.mcp_tool = BigQueryMCPTool(self.bigquery_client)
        logger.info("BigQuery MCP tools initialized")
    
    def _create_agent(self):
        """Create the Google ADK agent"""
        agent_config = self.config.get('agent', {})
        bigquery_config = self.config.get('bigquery', {})
        
        # Create instruction for the agent
        instruction = f"""
        You are an expert BigQuery data analyst with access to comprehensive BigQuery tools through the MCP (Model Context Protocol) framework.
        
        **Your Configuration:**
        - Project ID: {bigquery_config.get('project_id', 'your-gcp-project-id')}
        - Default Dataset: {bigquery_config.get('dataset_id', 'your_dataset')}
        - Location: {bigquery_config.get('location', 'US')}
        
        **Available BigQuery MCP Tools:**
        1. **execute_sql**: Execute SQL queries directly on BigQuery
           - Use this for data retrieval, aggregations, and analysis
           - Always use proper BigQuery SQL syntax
           - Include appropriate WHERE clauses for filtering
           - Use LIMIT for large result sets
        
        2. **get_table_info**: Get table schema and metadata
           - Use this to understand table structure before querying
           - Returns column names, types, and descriptions
        
        3. **get_dataset_info**: Get dataset information
           - Use this to explore available datasets
           - Returns dataset metadata and table listings
        
        4. **list_tables**: List all tables in a dataset
           - Use this to discover available tables
           - Returns table names and basic info
        
        **Analysis Capabilities:**
        - **Data Exploration**: Understand table schemas and relationships
        - **Statistical Analysis**: Calculate metrics, aggregations, and summaries
        - **Trend Analysis**: Analyze data over time with date functions
        - **Comparative Analysis**: Compare data across different dimensions
        - **Data Quality**: Identify missing values, duplicates, and anomalies
        
        **Best Practices:**
        - Always start by understanding the data structure using get_table_info or get_dataset_info
        - Use descriptive column aliases in SELECT statements
        - Apply appropriate filters to focus on relevant data
        - Use GROUP BY for aggregations
        - Order results logically (DESC for counts, ASC for dates)
        - Limit results to reasonable numbers (use LIMIT 100 for large result sets)
        - Provide clear explanations of findings
        - Include relevant statistics and insights
        - Show the SQL query used when relevant
        
        **Response Format:**
        - Provide clear explanations of your analysis
        - Include relevant statistics and percentages
        - Highlight key patterns and insights
        - Show the SQL query used when relevant
        - Suggest follow-up questions or analyses when appropriate
        
        **Example Queries:**
        - Data overview: `SELECT COUNT(*) as total_records FROM \`project.dataset.table\``
        - Top values: `SELECT column, COUNT(*) as count FROM \`project.dataset.table\` GROUP BY column ORDER BY count DESC LIMIT 10`
        - Time trends: `SELECT DATE(timestamp_column) as date, COUNT(*) as count FROM \`project.dataset.table\` GROUP BY date ORDER BY date DESC LIMIT 30`
        """
        
        # Create the agent
        self.agent = Agent(
            model=self.llm,
            name=agent_config.get('name', 'bigquery_mcp_agent'),
            description=agent_config.get('description', 'MCP Agent for BigQuery data analysis'),
            instruction=instruction,
            tools=[self.mcp_tool]
        )
        
        logger.info("BigQuery MCP Agent created successfully")
    
    def query(self, user_question: str) -> str:
        """Process user query and return analysis"""
        try:
            logger.info(f"Processing query: {user_question}")
            
            # Use the agent to process the query
            response = self.agent.run(input_text=user_question)
            
            logger.info("Query processed successfully")
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return f"I encountered an error while processing your query: {str(e)}"
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        return [
            "execute_sql - Execute SQL queries on BigQuery",
            "get_table_info - Get table schema and metadata", 
            "get_dataset_info - Get dataset information",
            "list_tables - List tables in a dataset"
        ]
    
    def execute_sql_directly(self, sql_query: str) -> Dict[str, Any]:
        """Execute SQL query directly (for testing/debugging)"""
        return self.mcp_tool.execute_sql(sql_query)
    
    def get_table_info_directly(self, project_id: str, dataset_id: str, table_id: str) -> Dict[str, Any]:
        """Get table info directly (for testing/debugging)"""
        return self.mcp_tool.get_table_info(project_id, dataset_id, table_id)

def main():
    """Main function to run the BigQuery MCP Agent"""
    try:
        # Initialize the agent
        agent = BigQueryMCPAgent()
        
        print("BigQuery MCP Agent initialized successfully!")
        print(f"Available tools: {len(agent.get_available_tools())}")
        
        # Interactive mode
        print("\nEnter your BigQuery questions (type 'quit' to exit):")
        
        while True:
            user_input = input("\nQuery: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Process the query
            response = agent.query(user_input)
            print(f"\nResponse: {response}")
            
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"Error initializing agent: {e}")

if __name__ == "__main__":
    main()
