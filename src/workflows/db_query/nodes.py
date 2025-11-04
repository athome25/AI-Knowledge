import json
from .state import QueryState
from .database import get_all_tables, get_table_schema, execute_query
from .prompts import (
    IDENTIFY_RELEVANT_TABLES_PROMPT,
    GENERATE_SQL_PROMPT,
    NATURAL_LANGUAGE_RESPONSE_PROMPT,
)
from src.core.llm import llm


def _format_conversation_history(history: list[dict]) -> str:
    if not history:
        return ""

    formatted = "Previous conversation:\n"
    for msg in history:
        role = msg.get("role", "").capitalize()
        content = msg.get("content", "")
        formatted += f"{role}: {content}\n"

    return formatted


def list_tables_node(state: QueryState) -> QueryState:
    state.all_tables = get_all_tables(state.db_path)
    return state


def identify_relevant_tables_node(state: QueryState) -> QueryState:
    conversation_context = _format_conversation_history(state.conversation_history)
    prompt = IDENTIFY_RELEVANT_TABLES_PROMPT.format(
        tables=", ".join(state.all_tables),
        user_query=state.user_query,
        conversation_context=conversation_context
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
    schemas = {}
    for table in state.relevant_tables:
        schemas[table] = get_table_schema(state.db_path, table)
    
    state.table_schemas = schemas
    return state


def generate_sql_node(state: QueryState) -> QueryState:
    schemas_text = "\n".join(state.table_schemas.values())
    conversation_context = _format_conversation_history(state.conversation_history)

    prompt = GENERATE_SQL_PROMPT.format(
        user_query=state.user_query,
        schemas=schemas_text,
        conversation_context=conversation_context
    )
    
    response = llm.invoke(prompt)
    sql_query = response.content if hasattr(response, 'content') else str(response)
    
    state.generated_sql = sql_query.strip()
    return state


def execute_query_node(state: QueryState) -> QueryState:
    state.query_result = execute_query(state.db_path, state.generated_sql)
    return state


def generate_response_node(state: QueryState) -> QueryState:
    query_results_str = json.dumps(state.query_result, indent=2)
    conversation_context = _format_conversation_history(state.conversation_history)
    schemas_text = "\n".join(state.table_schemas.values())

    prompt = NATURAL_LANGUAGE_RESPONSE_PROMPT.format(
        user_query=state.user_query,
        query_results=query_results_str,
        conversation_context=conversation_context,
        schemas=schemas_text
    )
    
    response = llm.invoke(prompt)
    state.natural_language_response = response.content if hasattr(response, 'content') else str(response)
    
    return state
