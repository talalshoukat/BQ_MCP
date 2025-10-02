#!/usr/bin/env python3
"""
Test script for the BigQuery MCP Agent
"""

import logging
from bigquery_mcp_agent import BigQueryMCPAgent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_agent_initialization():
    """Test agent initialization"""
    print("🧪 Testing agent initialization...")
    try:
        agent = BigQueryMCPAgent()
        print("✅ Agent initialized successfully!")
        return agent
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return None

def test_available_tools(agent):
    """Test available tools"""
    print("\n🧪 Testing available tools...")
    try:
        tools = agent.get_available_tools()
        print(f"✅ Found {len(tools)} available tools:")
        for i, tool in enumerate(tools, 1):
            print(f"   {i}. {tool}")
        return True
    except Exception as e:
        print(f"❌ Error getting tools: {e}")
        return False

def test_sample_queries(agent):
    """Test sample queries"""
    print("\n🧪 Testing sample queries...")
    
    sample_queries = [
        "What tools are available for BigQuery analysis?",
        "How do I get table information from BigQuery?",
        "What's the best way to explore BigQuery data?",
        "Show me how to write a simple SQL query for BigQuery"
    ]
    
    for i, query in enumerate(sample_queries, 1):
        print(f"\n📝 Test Query {i}: {query}")
        try:
            response = agent.query(query)
            print(f"✅ Response received (length: {len(response)} characters)")
            print(f"📋 Preview: {response[:200]}...")
        except Exception as e:
            print(f"❌ Error processing query: {e}")

def test_direct_tool_access(agent):
    """Test direct tool access"""
    print("\n🧪 Testing direct tool access...")
    
    # Test with a simple query (this will fail if no valid BigQuery setup)
    test_query = "SELECT 1 as test_value"
    
    try:
        print(f"📝 Testing direct SQL execution: {test_query}")
        result = agent.execute_sql_directly(test_query)
        
        if result.get('success'):
            print("✅ Direct SQL execution successful!")
            print(f"📊 Result: {result.get('data', [])}")
        else:
            print(f"⚠️  SQL execution failed (expected if no BigQuery setup): {result.get('error')}")
            
    except Exception as e:
        print(f"⚠️  Direct SQL test failed (expected if no BigQuery setup): {e}")

def main():
    """Main test function"""
    print("🚀 Starting BigQuery MCP Agent Tests")
    print("=" * 50)
    
    # Test 1: Initialize agent
    agent = test_agent_initialization()
    if not agent:
        print("❌ Cannot continue tests - agent initialization failed")
        return
    
    # Test 2: Check available tools
    if not test_available_tools(agent):
        print("❌ Cannot continue tests - tools not available")
        return
    
    # Test 3: Test sample queries
    test_sample_queries(agent)
    
    # Test 4: Test direct tool access
    test_direct_tool_access(agent)
    
    print("\n" + "=" * 50)
    print("🎉 Tests completed!")
    print("\n💡 To use the agent with real BigQuery data:")
    print("   1. Update config.yaml with your BigQuery project details")
    print("   2. Ensure Google Cloud credentials are configured")
    print("   3. Run: python main.py")

if __name__ == "__main__":
    main()
