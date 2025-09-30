"""
BigQuery MCP Tools for Fraud Data Analysis
Simplified version for single aggregated fraud table with LLM-powered query generation
"""

import json
import logging
from typing import Dict, List, Any, Optional
from google.cloud import bigquery
from google.cloud.bigquery import Client
from google.auth import default
import pandas as pd
import openai
import os

logger = logging.getLogger(__name__)


class BigQueryMCPQueryTool:
    """Simplified MCP tool for generating and executing BigQuery queries using LLM"""
    
    def __init__(self, project_id: str, dataset_id: str, table_name: str):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_name = table_name
        self.table_id = f"{project_id}.{dataset_id}.{table_name}"
        self.client = self._get_bigquery_client()
        
        # Known fraud dimensions for the aggregated table
        self.fraud_dimensions = [
            'gender', 'age_bracket', 'income_bracket', 'education', 
            'occupation', 'company', 'region', 'fraud_type', 'fraud_amount',
            'fraud_date', 'fraud_id', 'created_at', 'updated_at'
        ]
    
    def _get_bigquery_client(self) -> Client:
        """Initialize BigQuery client with default credentials"""
        try:
            credentials, _ = default()
            return bigquery.Client(project=self.project_id, credentials=credentials)
        except Exception as e:
            logger.error(f"Failed to initialize BigQuery client: {e}")
            raise
    
    def _generate_sql_with_llm(self, user_request: str) -> str:
        """
        Use OpenAI to generate SQL query based on user request
        Args:
            user_request: Natural language request from user
        Returns: Generated SQL query
        """
        try:
            # Set up OpenAI client
            openai.api_key = os.getenv("OPENAI_API_KEY")
            
            # Create prompt for SQL generation
            prompt = f"""
            You are a SQL expert specializing in fraud data analysis. 
            Generate a BigQuery SQL query based on the user's request.
            
            Table: {self.table_id}
            Available columns: {', '.join(self.fraud_dimensions)}
            
            User Request: {user_request}
            
            Generate a SQL query that:
            1. Uses proper BigQuery syntax
            2. Includes appropriate WHERE clauses if needed
            3. Uses GROUP BY for aggregations
            4. Orders results logically
            5. Limits results to reasonable numbers (use LIMIT 100 for large result sets)
            
            Return ONLY the SQL query, no explanations.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a SQL expert. Generate BigQuery SQL queries for fraud data analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up the query (remove markdown formatting if present)
            if sql_query.startswith("```sql"):
                sql_query = sql_query.replace("```sql", "").replace("```", "").strip()
            elif sql_query.startswith("```"):
                sql_query = sql_query.replace("```", "").strip()
            
            return sql_query
            
        except Exception as e:
            logger.error(f"Error generating SQL with LLM: {e}")
            # Fallback to a simple query
            return f"SELECT * FROM `{self.table_id}` LIMIT 10"
    
    def generate_fraud_query(self, user_request: str) -> Dict[str, Any]:
        """
        Generate BigQuery SQL query using LLM based on user request
        Args:
            user_request: Natural language request from user
        Returns: Dictionary containing generated query and metadata
        """
        try:
            # Generate query using LLM
            query = self._generate_sql_with_llm(user_request)
            
            return {
                "query": query,
                "table_name": self.table_name,
                "table_id": self.table_id,
                "user_request": user_request,
                "available_dimensions": self.fraud_dimensions
            }
            
        except Exception as e:
            logger.error(f"Error generating fraud query: {e}")
            return {"error": str(e)}
    
    def execute_fraud_query(self, query: str) -> Dict[str, Any]:
        """
        Execute BigQuery query and return results
        Args:
            query: SQL query to execute
        Returns: Dictionary containing query results
        """
        try:
            # Execute the query
            query_job = self.client.query(query)
            results = query_job.result()
            
            # Convert results to list of dictionaries
            rows = []
            for row in results:
                rows.append(dict(row))
            
            # Get query metadata
            job = self.client.get_job(query_job.job_id)
            
            return {
                "success": True,
                "rows": rows,
                "num_rows": len(rows),
                "job_id": query_job.job_id,
                "total_bytes_processed": job.total_bytes_processed,
                "total_bytes_billed": job.total_bytes_billed,
                "query": query
            }
            
        except Exception as e:
            logger.error(f"Error executing fraud query: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
    
    def get_fraud_statistics(self, dimension: str = None) -> Dict[str, Any]:
        """
        Get fraud statistics for a specific dimension or overall
        Args:
            dimension: Dimension to analyze (gender, age_bracket, region, etc.)
        Returns: Dictionary containing fraud statistics
        """
        try:
            if dimension:
                query = f"""
                SELECT {dimension}, COUNT(*) as fraud_count
                FROM `{self.table_id}`
                GROUP BY {dimension}
                ORDER BY fraud_count DESC
                LIMIT 20
                """
            else:
                query = f"""
                SELECT 
                    COUNT(*) as total_fraud_cases,
                    COUNT(DISTINCT gender) as unique_genders,
                    COUNT(DISTINCT age_bracket) as unique_age_brackets,
                    COUNT(DISTINCT region) as unique_regions,
                    COUNT(DISTINCT company) as unique_companies
                FROM `{self.table_id}`
                """
            
            result = self.execute_fraud_query(query)
            return result
            
        except Exception as e:
            logger.error(f"Error getting fraud statistics: {e}")
            return {"error": str(e)}


# Simplified MCP Tool Functions for ADK Integration
def generate_fraud_query(project_id: str, dataset_id: str, table_name: str, user_request: str) -> str:
    """
    MCP tool function to generate fraud data queries using LLM
    Args:
        project_id: Google Cloud project ID
        dataset_id: BigQuery dataset ID containing fraud data
        table_name: Name of the fraud table
        user_request: Natural language request from user
    Returns:
        JSON string containing generated query and metadata
    """
    query_tool = BigQueryMCPQueryTool(project_id, dataset_id, table_name)
    result = query_tool.generate_fraud_query(user_request)
    return json.dumps(result, indent=2)


def execute_fraud_query(project_id: str, dataset_id: str, table_name: str, query: str) -> str:
    """
    MCP tool function to execute fraud data queries
    Args:
        project_id: Google Cloud project ID
        dataset_id: BigQuery dataset ID containing fraud data
        table_name: Name of the fraud table
        query: SQL query to execute
    Returns:
        JSON string containing query results
    """
    query_tool = BigQueryMCPQueryTool(project_id, dataset_id, table_name)
    result = query_tool.execute_fraud_query(query)
    return json.dumps(result, indent=2)


def get_fraud_statistics(project_id: str, dataset_id: str, table_name: str, dimension: str = None) -> str:
    """
    MCP tool function to get fraud statistics
    Args:
        project_id: Google Cloud project ID
        dataset_id: BigQuery dataset ID containing fraud data
        table_name: Name of the fraud table
        dimension: Dimension to analyze (optional)
    Returns:
        JSON string containing fraud statistics
    """
    query_tool = BigQueryMCPQueryTool(project_id, dataset_id, table_name)
    result = query_tool.get_fraud_statistics(dimension)
    return json.dumps(result, indent=2)
