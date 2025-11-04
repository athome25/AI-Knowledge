from pydantic import BaseModel, Field
from typing import Optional


class QueryState(BaseModel):
    user_query: str = Field(description="The original natural language query from the user")
    db_path: str = Field(default="data/chinook.db", description="Path to the SQLite database file")
    all_tables: list[str] = Field(default_factory=list, description="All available tables in the database")
    relevant_tables: list[str] = Field(default_factory=list, description="Tables identified as relevant to the query")
    table_schemas: dict[str, str] = Field(default_factory=dict, description="Mapping of table names to their schemas")
    generated_sql: str = Field(default="", description="The SQL query generated from the user query")
    query_result: list[dict] = Field(default_factory=list, description="Results from executing the SQL query")
    natural_language_response: str = Field(default="", description="Final natural language response to the user")
