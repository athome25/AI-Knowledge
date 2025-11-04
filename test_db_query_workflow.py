from dotenv import load_dotenv
load_dotenv()

from src.workflows.db_query.workflow import run_query


if __name__ == "__main__":
    
    query = input("Enter your query: ")
    print(f"\n{'='*60}")
    print(f"Query: {query}")
    print(f"{'='*60}")
    
    try:
        response = run_query(query)
        print(f"Final Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
