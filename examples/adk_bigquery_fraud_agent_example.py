"""
ADK Built-in BigQuery Fraud Agent Example
Demonstrates the fraud agent using Google ADK's native BigQuery tools
"""

import asyncio
import os
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent.sub_agents.fraud_agent import fraud_agent

# Configuration
APP_NAME = "adk_bigquery_fraud_analysis"
USER_ID = "fraud_analyst"
SESSION_ID = "fraud_session_003"

# Set environment variables for ADK BigQuery configuration
os.environ.setdefault("FRAUD_PROJECT_ID", "your-gcp-project-id")
os.environ.setdefault("FRAUD_DATASET_ID", "fraud_data")
os.environ.setdefault("FRAUD_TABLE_NAME", "aggregated_fraud_table")

async def setup_session_and_runner():
    """Setup session and runner for ADK BigQuery fraud agent"""
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=APP_NAME, 
        user_id=USER_ID, 
        session_id=SESSION_ID
    )
    runner = Runner(
        agent=fraud_agent, 
        app_name=APP_NAME, 
        session_service=session_service
    )
    return session, runner

async def call_fraud_agent(query: str):
    """Call the ADK BigQuery fraud agent with a query"""
    content = types.Content(role='user', parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    print(f"\n🔍 USER QUERY: {query}")
    print("=" * 60)
    
    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print(f"🤖 FRAUD AGENT RESPONSE:\n{final_response}")
            print("=" * 60)

async def main():
    """Main function demonstrating ADK BigQuery fraud agent capabilities"""
    print("🚀 ADK Built-in BigQuery Fraud Agent Demo")
    print("=" * 60)
    print("✨ Features:")
    print("   • Native ADK BigQuery integration")
    print("   • Built-in execute_sql, get_table_metadata tools")
    print("   • No custom MCP tools needed")
    print("   • Direct BigQuery access")
    print("   • Simplified architecture")
    print("=" * 60)
    
    # Example queries demonstrating ADK BigQuery capabilities
    example_queries = [
        # Basic queries using ADK's execute_sql tool
        "Show me the total number of fraud cases in our dataset",
        "What is the table structure and schema of our fraud data?",
        "List all available tables in our fraud dataset",
        
        # Demographic analysis
        "Show me fraud cases broken down by gender",
        "What are the fraud patterns by age bracket?",
        "Analyze fraud cases by education level",
        "Show me fraud statistics by occupation",
        
        # Geographic analysis
        "Which regions have the highest fraud rates?",
        "Show me fraud distribution by region and company",
        "What are the geographic patterns in our fraud data?",
        
        # Temporal analysis
        "Show me fraud trends over the last 12 months",
        "What are the monthly fraud patterns?",
        "Analyze fraud cases by year and month",
        
        # Company analysis
        "Which companies have the most fraud cases?",
        "Show me fraud patterns by company and occupation",
        "What are the top 10 companies with highest fraud rates?",
        
        # Income analysis
        "Show me fraud cases by income bracket",
        "What percentage of fraud cases are from each income bracket?",
        "Analyze the relationship between income and fraud type",
        
        # Comprehensive analysis
        "Give me a comprehensive overview of our fraud data",
        "What are the key insights and patterns from our fraud data?",
        "Show me the most significant fraud trends and anomalies",
        
        # Advanced queries
        "Show me fraud cases where the amount is greater than $10,000",
        "What are the fraud patterns for cases reported in the last 30 days?",
        "Show me the correlation between fraud type and region"
    ]
    
    print("📊 Running ADK BigQuery Fraud Analysis Examples...")
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n📋 Example {i}/{len(example_queries)}")
        await call_fraud_agent(query)
        
        # Add a small delay between queries
        await asyncio.sleep(1)
    
    print("\n✅ ADK BigQuery Fraud Analysis Demo Complete!")
    print("\n💡 Key Benefits of ADK Built-in Tools:")
    print("   • Native BigQuery integration")
    print("   • No custom MCP tools required")
    print("   • Built-in execute_sql functionality")
    print("   • Automatic table metadata access")
    print("   • Simplified configuration")
    print("   • Better performance and reliability")
    print("   • Direct access to BigQuery features")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
