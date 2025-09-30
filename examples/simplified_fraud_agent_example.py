"""
Simplified Fraud Data Analysis Agent Example
Demonstrates the streamlined fraud agent with LLM-powered query generation
"""

import asyncio
import os
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent.sub_agents.fraud_agent import fraud_agent

# Configuration
APP_NAME = "simplified_fraud_analysis"
USER_ID = "fraud_analyst"
SESSION_ID = "fraud_session_002"

# Set environment variables for simplified configuration
os.environ.setdefault("FRAUD_PROJECT_ID", "your-gcp-project-id")
os.environ.setdefault("FRAUD_DATASET_ID", "fraud_data")
os.environ.setdefault("FRAUD_TABLE_NAME", "aggregated_fraud_table")
os.environ.setdefault("OPENAI_API_KEY", "your-openai-api-key")

async def setup_session_and_runner():
    """Setup session and runner for simplified fraud agent"""
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
    """Call the simplified fraud agent with a query"""
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
    """Main function demonstrating simplified fraud agent capabilities"""
    print("🚀 Simplified Fraud Data Analysis Agent Demo")
    print("=" * 60)
    print("✨ Features:")
    print("   • Direct table reference (no schema discovery)")
    print("   • LLM-powered SQL query generation")
    print("   • Simplified configuration")
    print("   • Faster execution")
    print("=" * 60)
    
    # Example queries demonstrating simplified fraud analysis
    example_queries = [
        # Natural language queries that will be converted to SQL by LLM
        "Show me fraud cases broken down by gender",
        "What are the fraud patterns by age bracket?",
        "Which regions have the highest fraud rates?",
        "Analyze fraud trends over the last 6 months",
        "Show me fraud statistics by company",
        "What percentage of fraud cases are from each income bracket?",
        "Give me a comprehensive overview of our fraud data",
        "Show me the top 10 occupations with highest fraud rates",
        "Analyze fraud patterns by education level",
        "What are the key insights from our fraud data?"
    ]
    
    print("📊 Running Simplified Fraud Analysis Examples...")
    
    for i, query in enumerate(example_queries, 1):
        print(f"\n📋 Example {i}/{len(example_queries)}")
        await call_fraud_agent(query)
        
        # Add a small delay between queries
        await asyncio.sleep(1)
    
    print("\n✅ Simplified Fraud Analysis Demo Complete!")
    print("\n💡 Key Improvements:")
    print("   • Removed unnecessary schema discovery")
    print("   • Direct table reference for faster setup")
    print("   • LLM-powered query generation")
    print("   • Simplified configuration")
    print("   • Better performance and reliability")

if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
