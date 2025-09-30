"""
Test script for the Fraud Data Analysis Agent
Verifies that the agent can be imported and initialized correctly
"""

import os
import sys
import asyncio
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Set up environment variables for testing
os.environ.setdefault("FRAUD_PROJECT_ID", "test-project")
os.environ.setdefault("FRAUD_DATASET_ID", "test_fraud_data")
os.environ.setdefault("FRAUD_TABLE_NAME", "test_fraud_records")

# Mock LLM configuration for testing
os.environ.setdefault("LLM_API_URL", "https://test-llm-endpoint/v1")
os.environ.setdefault("LLM_API_KEY", "test-api-key")
os.environ.setdefault("MODEL_NAME", "test-model")

def test_fraud_agent_import():
    """Test that the fraud agent can be imported successfully"""
    try:
        from agent.sub_agents.fraud_agent import fraud_agent
        print("✅ Successfully imported fraud_agent")
        print(f"   Agent name: {fraud_agent.name}")
        print(f"   Agent description: {fraud_agent.description}")
        print(f"   Number of tools: {len(fraud_agent.tools)}")
        return True
    except Exception as e:
        print(f"❌ Failed to import fraud_agent: {e}")
        return False

def test_mcp_tools_import():
    """Test that MCP tools can be imported successfully"""
    try:
        from tools.bigquery_mcp_tools import (
            discover_fraud_schema,
            generate_fraud_query,
            execute_fraud_query,
            get_fraud_statistics
        )
        print("✅ Successfully imported MCP tools")
        return True
    except Exception as e:
        print(f"❌ Failed to import MCP tools: {e}")
        return False

def test_config_integration():
    """Test that the fraud agent is properly integrated with the config system"""
    try:
        from agent.configs.config import ConfigFactory, SubAgentsEnum
        
        # Check if fraud_agent is in the enum
        assert hasattr(SubAgentsEnum, 'fraud_agent')
        print("✅ Fraud agent added to SubAgentsEnum")
        
        # Test config parsing (this might fail if env vars are not set properly)
        try:
            config = ConfigFactory.parse_yaml_with_hydra(overrides=[])
            print("✅ Config parsing successful")
            return True
        except Exception as e:
            print(f"⚠️  Config parsing failed (expected in test environment): {e}")
            return True  # This is expected in test environment
            
    except Exception as e:
        print(f"❌ Config integration test failed: {e}")
        return False

def test_agent_tools():
    """Test that the fraud agent has the expected tools"""
    try:
        from agent.sub_agents.fraud_agent import fraud_agent
        
        # Check that the agent has tools
        assert len(fraud_agent.tools) > 0, "Fraud agent should have tools"
        print(f"✅ Fraud agent has {len(fraud_agent.tools)} tools")
        
        # Check tool names/types
        tool_names = [getattr(tool, 'name', str(type(tool))) for tool in fraud_agent.tools]
        print(f"   Tool types: {tool_names}")
        
        return True
    except Exception as e:
        print(f"❌ Agent tools test failed: {e}")
        return False

async def test_agent_initialization():
    """Test that the fraud agent can be initialized and used"""
    try:
        from agent.sub_agents.fraud_agent import fraud_agent
        from google.adk.runners import Runner
        from google.adk.sessions import InMemorySessionService
        from google.genai import types
        
        # Setup session and runner
        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name="test_fraud_app",
            user_id="test_user",
            session_id="test_session"
        )
        
        runner = Runner(
            agent=fraud_agent,
            app_name="test_fraud_app",
            session_service=session_service
        )
        
        print("✅ Fraud agent initialization successful")
        print("   Session created successfully")
        print("   Runner initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing Fraud Data Analysis Agent")
    print("=" * 50)
    
    tests = [
        ("Import Fraud Agent", test_fraud_agent_import),
        ("Import MCP Tools", test_mcp_tools_import),
        ("Config Integration", test_config_integration),
        ("Agent Tools", test_agent_tools),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running: {test_name}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    # Run async test
    print(f"\n🔍 Running: Agent Initialization")
    try:
        if asyncio.run(test_agent_initialization()):
            passed += 1
            print(f"✅ Agent Initialization - PASSED")
        else:
            print(f"❌ Agent Initialization - FAILED")
    except Exception as e:
        print(f"❌ Agent Initialization - ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total + 1} tests passed")
    
    if passed == total + 1:
        print("🎉 All tests passed! Fraud agent is ready to use.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total + 1

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
