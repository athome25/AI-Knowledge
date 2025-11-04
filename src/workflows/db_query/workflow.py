from langgraph.graph import StateGraph, END
from .state import QueryState
from .nodes import (
    list_tables_node,
    identify_relevant_tables_node,
    get_table_schemas_node,
    generate_sql_node,
    execute_query_node,
    generate_response_node,
)


def create_db_query_workflow():
    workflow = StateGraph(QueryState)

    workflow.add_node("list_tables", list_tables_node)
    workflow.add_node("identify_tables", identify_relevant_tables_node)
    workflow.add_node("get_schemas", get_table_schemas_node)
    workflow.add_node("generate_sql", generate_sql_node)
    workflow.add_node("execute_query", execute_query_node)
    workflow.add_node("generate_response", generate_response_node)
    
    workflow.add_edge("list_tables", "identify_tables")
    workflow.add_edge("identify_tables", "get_schemas")
    workflow.add_edge("get_schemas", "generate_sql")
    workflow.add_edge("generate_sql", "execute_query")
    workflow.add_edge("execute_query", "generate_response")
    workflow.add_edge("generate_response", END)
    
    workflow.set_entry_point("list_tables")
    
    return workflow.compile()


def run_query(user_query: str, db_path: str = "data/chinook.db", conversation_history: list[dict] = None) -> str:
    workflow = create_db_query_workflow()
    initial_state = QueryState(
        user_query=user_query,
        db_path=db_path,
        conversation_history=conversation_history or []
    )

    final_state = None
    for event in workflow.stream(initial_state):
        print(f"{event}\n")
        final_state = event

    node_name = list(final_state.keys())[0]
    return final_state[node_name]["natural_language_response"]
