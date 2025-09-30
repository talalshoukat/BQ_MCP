"""
Example script demonstrating the Fraud Data Analysis Agent
Shows how to use the agent for comprehensive fraud data analysis
"""

import asyncio
import os
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent.sub_agents.fraud_agent import fraud_agent

# Configuration
APP_NAME = "fraud_analysis_app"
USER_ID = "fraud_analyst"
SESSION_ID = "fraud_session_001"

# Set environment variables for BigQuery configuration
os.environ.setdefault("FRAUD_PROJECT_ID", "your-gcp-project-id")
os.environ.setdefault("FRAUD_DATASET_ID", "fraud_data")
os.environ.setdefault("FRAUD_TABLE_NAME", "fraud_records")

async def setup_session_and_runner():
    """Setup session and runner for fraud agent"""
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
    """Call the fraud agent with a query"""
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
    """Main function demonstrating fraud agent capabilities"""
    print("🚀 Fraud Data Analysis Agent Demo")
    print("=" * 60)
    
    # Example queries demonstrating different fraud analysis capabilities
    example_queries = [
        # Schema Discovery
        "What tables and columns are available in the fraud dataset?",
        
        # Demographic Analysis
        "Show me fraud cases broken down by gender and age bracket",
        "What are the fraud patterns by education level?",
        
        # Geographic Analysis
        "Which regions have the highest fraud rates?",
        "Show me fraud distribution by region and company",
        
        # Temporal Analysis
        "What are the fraud trends over the last 12 months?",
        "Show me monthly fraud patterns",
        
        # Company Analysis
        "Which companies have the most fraud cases?",
        "Analyze fraud patterns by company and occupation",
        
        # Comprehensive Analysis
        "Give me a comprehensive overview of fraud statistics",
        "What are the key fraud patterns and insights?",
        
        # Specific Queries
        "How many total fraud cases do we have?",
        "What percentage of fraud cases are from each income bracket?",
        "Show me the top 10 occupations with highest fraud rates"
    ]
    
    print("📊 Running Fraud Analysis Examples...")
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n📋 Example {i}/{len(example_queries)}")
        await call_fraud_agent(query)
        
        # Add a small delay between queries
        await asyncio.sleep(1)
    
    print("\n✅ Fraud Analysis Demo Complete!")
    print("\n💡 Key Features Demonstrated:")
    print("   • Dynamic schema discovery")
    print("   • Natural language query generation")
    print("   • Multi-dimensional fraud analysis")
    print("   • Statistical insights and patterns")
    print("   • BigQuery integration with Google ADK")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
