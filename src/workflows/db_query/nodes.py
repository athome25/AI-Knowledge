import json
from .state import QueryState
from .database import get_all_tables, get_table_schema, execute_query
from .prompts import (
    IDENTIFY_RELEVANT_TABLES_PROMPT,
    GENERATE_SQL_PROMPT,
    NATURAL_LANGUAGE_RESPONSE_PROMPT,
)
from src.core.llm import llm


def list_tables_node(state: QueryState) -> QueryState:
    """Node 1: List all tables in the database."""
    state.all_tables = get_all_tables(state.db_path)
    return state


def identify_relevant_tables_node(state: QueryState) -> QueryState:
    """Node 2: Identify which tables are relevant to the user query."""
    prompt = IDENTIFY_RELEVANT_TABLES_PROMPT.format(
        tables=", ".join(state.all_tables),
        user_query=state.user_query
    )
    
    response = llm.invoke(prompt)
    response_text = response.content if hasattr(response, 'content') else str(response)
    
    try:
        relevant_tables = json.loads(response_text)
        state.relevant_tables = relevant_tables if isinstance(relevant_tables, list) else []
    except json.JSONDecodeError:
        state.relevant_tables = []
    return state


def get_table_schemas_node(state: QueryState) -> QueryState:
    """Node 3: Get the schemas of the relevant tables."""
    schemas = {}
    for table in state.relevant_tables:
        schemas[table] = get_table_schema(state.db_path, table)
    
    state.table_schemas = schemas
    return state


def generate_sql_node(state: QueryState) -> QueryState:
    """Node 4: Generate SQL query from the user query and table schemas."""
    schemas_text = "\n".join(state.table_schemas.values())
    
    prompt = GENERATE_SQL_PROMPT.format(
        user_query=state.user_query,
        schemas=schemas_text
    )
    
    response = llm.invoke(prompt)
    sql_query = response.content if hasattr(response, 'content') else str(response)
    
    state.generated_sql = sql_query.strip()
    return state


def execute_query_node(state: QueryState) -> QueryState:
    """Node 5: Execute the SQL query and store results."""
    state.query_result = execute_query(state.db_path, state.generated_sql)
    return state


def generate_response_node(state: QueryState) -> QueryState:
    """Node 6: Generate natural language response from query results."""
    query_results_str = json.dumps(state.query_result, indent=2)
    
    prompt = NATURAL_LANGUAGE_RESPONSE_PROMPT.format(
        user_query=state.user_query,
        query_results=query_results_str
    )
    
    response = llm.invoke(prompt)
    state.natural_language_response = response.content if hasattr(response, 'content') else str(response)
    
    return state
