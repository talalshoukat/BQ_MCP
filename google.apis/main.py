#!/usr/bin/env python3
"""
Main script to run the BigQuery MCP Agent
"""

import sys
import logging
from bigquery_mcp_agent import BigQueryMCPAgent

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_interactive_mode():
    """Run the agent in interactive mode"""
    try:
        # Initialize the agent
        print("Initializing BigQuery MCP Agent...")
        agent = BigQueryMCPAgent()
        
        print("✅ BigQuery MCP Agent initialized successfully!")
        print(f"📊 Available tools: {len(agent.get_available_tools())}")
        
        # Show available tools
        print("\n🔧 Available BigQuery MCP Tools:")
        for i, tool in enumerate(agent.get_available_tools(), 1):
            print(f"   {i}. {tool}")
        
        print("\n" + "="*60)
        print("BigQuery MCP Agent - Interactive Mode")
        print("="*60)
        print("Ask questions about your BigQuery data!")
        print("Examples:")
        print("  - 'Show me the schema of the users table'")
        print("  - 'What are the top 10 products by sales?'")
        print("  - 'How many records are in the orders dataset?'")
        print("  - 'List all tables in the analytics dataset'")
        print("\nType 'quit', 'exit', or 'q' to exit")
        print("="*60)
        
        # Interactive loop
        while True:
            try:
                user_input = input("\n🔍 Your question: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    print("Please enter a question.")
                    continue
                
                # Process the query
                print("\n🤔 Processing your question...")
                response = agent.query(user_input)
                print(f"\n📋 Response:\n{response}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                logger.error(f"Error processing query: {e}")
                print(f"❌ Error: {e}")
                
    except Exception as e:
        logger.error(f"Error initializing agent: {e}")
        print(f"❌ Failed to initialize agent: {e}")
        sys.exit(1)

def run_single_query(query: str):
    """Run a single query"""
    try:
        print(f"Initializing BigQuery MCP Agent for query: '{query}'")
        agent = BigQueryMCPAgent()
        
        print("🤔 Processing your question...")
        response = agent.query(query)
        print(f"\n📋 Response:\n{response}")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)

def main():
    """Main function"""
    if len(sys.argv) > 1:
        # Single query mode
        query = " ".join(sys.argv[1:])
        run_single_query(query)
    else:
        # Interactive mode
        run_interactive_mode()

if __name__ == "__main__":
    main()
