IDENTIFY_RELEVANT_TABLES_PROMPT = """You are a database expert. Given a user's natural language query and a list of available tables in a database, identify which tables are most relevant to answering the query.

Available tables:
{tables}

User query: {user_query}

Return ONLY a valid JSON array of table names with no markdown formatting, no code blocks, and no additional text.
Example: ["table1", "table2"]
Empty example: []"""

GENERATE_SQL_PROMPT = """You are an expert SQL developer. Given a user's natural language query, the relevant database tables, and their schemas, generate the appropriate SQLite SQL query to answer the user's question.

IMPORTANT: This is a SQLite database. Use SQLite syntax:
- Use LIMIT instead of TOP
- Use DATETIME functions compatible with SQLite
- Use proper SQLite aggregate functions

User query: {user_query}

Relevant tables and their schemas:
{schemas}

Generate a SQLite query that will answer the user's question. Return ONLY the SQL query with no explanations, no markdown formatting, and no code blocks."""

NATURAL_LANGUAGE_RESPONSE_PROMPT = """You are a helpful assistant. Given a user's original query and the results from a database query, provide a natural language response that clearly answers their question.

Original user query: {user_query}

Query results:
{query_results}

Provide a clear, concise natural language response that answers the user's query based on the results above."""
