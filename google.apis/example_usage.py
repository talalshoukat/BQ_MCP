#!/usr/bin/env python3
"""
Example usage of the BigQuery MCP Agent
"""

from bigquery_mcp_agent import BigQueryMCPAgent
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def example_basic_usage():
    """Example of basic agent usage"""
    print("🔍 Example 1: Basic Agent Usage")
    print("-" * 40)
    
    try:
        # Initialize the agent
        agent = BigQueryMCPAgent()
        
        # Ask a simple question
        question = "What tools are available for BigQuery analysis?"
        response = agent.query(question)
        
        print(f"Question: {question}")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")

def example_data_exploration():
    """Example of data exploration queries"""
    print("\n🔍 Example 2: Data Exploration Queries")
    print("-" * 40)
    
    try:
        agent = BigQueryMCPAgent()
        
        # List of exploration queries
        queries = [
            "How do I get information about a BigQuery table?",
            "What's the best way to explore BigQuery datasets?",
            "Show me how to list all tables in a dataset"
        ]
        
        for i, query in enumerate(queries, 1):
            print(f"\nQuery {i}: {query}")
            response = agent.query(query)
            print(f"Response: {response[:200]}...")  # Truncate for readability
            
    except Exception as e:
        print(f"Error: {e}")

def example_analysis_queries():
    """Example of analysis queries"""
    print("\n🔍 Example 3: Analysis Queries")
    print("-" * 40)
    
    try:
        agent = BigQueryMCPAgent()
        
        # List of analysis queries
        queries = [
            "How do I calculate the top 10 products by sales in BigQuery?",
            "What's the best way to analyze time series data in BigQuery?",
            "Show me how to create aggregations in BigQuery"
        ]
        
        for i, query in enumerate(queries, 1):
            print(f"\nQuery {i}: {query}")
            response = agent.query(query)
            print(f"Response: {response[:200]}...")  # Truncate for readability
            
    except Exception as e:
        print(f"Error: {e}")

def example_direct_tool_access():
    """Example of direct tool access"""
    print("\n🔍 Example 4: Direct Tool Access")
    print("-" * 40)
    
    try:
        agent = BigQueryMCPAgent()
        
        # Get available tools
        tools = agent.get_available_tools()
        print("Available tools:")
        for tool in tools:
            print(f"  - {tool}")
        
        # Note: Direct SQL execution would require valid BigQuery setup
        print("\nNote: Direct SQL execution requires valid BigQuery credentials and project setup")
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Run all examples"""
    print("🚀 BigQuery MCP Agent - Example Usage")
    print("=" * 50)
    
    try:
        example_basic_usage()
        example_data_exploration()
        example_analysis_queries()
        example_direct_tool_access()
        
        print("\n" + "=" * 50)
        print("✅ Examples completed!")
        print("\n💡 To use with real BigQuery data:")
        print("   1. Update config.yaml with your project details")
        print("   2. Configure Google Cloud credentials")
        print("   3. Run: python main.py")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")

if __name__ == "__main__":
    main()
