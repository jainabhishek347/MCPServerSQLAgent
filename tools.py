from server import mcp, schemas
from typing import Dict, List
from sqlalchemy import text
from helper import extract_database_schema_and_table, get_db_connection
import os
import json

@mcp.tool(name="get_tables_schema")
def get_tables_schema(tables:list) -> Dict:
  '''
  Returns schema of a tables as a  dictionary. Each entry consists of:
    Key: table name
    Values: Dictionary. Each sub dictionary contains:
      - column_name: name of a column
      - column_type: type of cilumn
      - column_description - descritpion of column values and purpose

  Examples:
  - Single table schema : get_tables_schema(["api_analytics_orders"])
  - Multiple tables schema : get_tables_schema(["api_analytics_orders", "api_analytics_products"])
  Args:
    tables: list of tables to get schema for
  Returns:
    Dictionary containing schema for each table in the input list.
  '''

  return {t: schemas[t] for t in tables if t in schemas}

@mcp.tool(name="run_sql_query")
def run_sql_query(query:str) -> Dict:
  '''
  Runs given sql query on redshift and returns the result.
  Args:
    query: sql querystring to execute
  Returns:
    Dictionary contianing sql query result.
  '''
  # Block query with blacklisted keywords
  blacklisted_keywords = ['INSERT', 'DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE']
  sql = query.upper().strip()
  for keyword in blacklisted_keywords:
    if keyword in sql and not sql.startswith('SELECT'):
      return {"error": f"Query contains blacklisted keyword: {keyword}"}
  
  # Check if select statement is not using any table outside permitted list
  if sql.startswith('SELECT'):
    database,schema, table =extract_database_schema_and_table(sql)[0]
    with open("sql_permitted_tables.json") as f:
      data = json.load(f)
  
    if not database is None and data['database'].upper() != database:
        return {"error": f"Database {database} access denied"}
    if data['schema'].upper() != schema:
        return {"error": f"Schema {schema} access denied in database"}
    if not table in [t.upper() for t in list(schemas.keys())]:
        return {"error": f"Table {table} access denied in schema {schema}"}      

  # run query
  engine = get_db_connection()
  if not sql:
      return {"error": "No SQL provided"}

  try:
      with engine.connect() as conn:
          result = conn.execute(text(sql))
          rows = [list(row) for row in result.fetchall()]
      return {"rows": rows}
  except Exception as e:
      return {"error": str(e)}

@mcp.tool(name="sql_query_optimizer")
def sql_query_optimizer(query: str) -> Dict:
  """
  Suggests optimization possibilities for a given SQL query for Redshift database.
  It uses the configured database schema instead of looking into the database directly.
  Args:
    query: The SQL query string to optimize.
  Returns:
    Dictionary containing optimization suggestions.
  """
  suggestions = []

  # Parse the SQL query to extract tables and other components
  parsed_tables = extract_database_schema_and_table(query)
  
  # Example optimization suggestions (can be expanded)
  if "JOIN" in query.upper():
    suggestions.append("Consider optimizing JOIN conditions. Ensure join columns have matching data types and are properly indexed/distributed.")
  if "ORDER BY" in query.upper() and "LIMIT" in query.upper():
    suggestions.append("If using ORDER BY with LIMIT, ensure the ordering columns are part of the sort key for better performance.")
  if "SELECT *" in query.upper():
    suggestions.append("Avoid using SELECT *. Specify only the columns you need to reduce data transfer and processing.")
  
  # Check for large tables and suggest distribution/sort keys
  for db, schema, table in parsed_tables:
      # Normalize table name for schema lookup
      normalized_table_name = table.lower() if table else None
      if normalized_table_name and normalized_table_name in schemas:
          suggestions.append(f"For table '{table}', consider its distribution style and sort keys. Large fact tables should often use DISTKEY and SORTKEY for optimal query performance.")
  
  if not suggestions:
    suggestions.append("No specific optimization suggestions found for the given query based on basic analysis. Consider deeper analysis for complex queries.")

  return {"optimization_suggestions": suggestions}

@mcp.tool(name="redshift_billing_analyzer")
def redshift_billing_analyzer(start_date: str, end_date: str) -> Dict:
  """
  Provides day-wise Redshift billing information (Cost & Usage Analyzer) for a given date range.
  In a real scenario, this would interact with AWS Cost Explorer.
  Args:
    start_date: The start date for the billing report (YYYY-MM-DD).
    end_date: The end date for the billing report (YYYY-MM-DD).
  Returns:
    Dictionary containing a simulated day-wise billing report.
  """
  # This is a placeholder for actual AWS API interaction
  # In a real implementation, you would use boto3 to call AWS Cost Explorer
  # For now, we return sample data
  sample_billing_data = {
      "2023-01-01": {"cost": "$10.50", "usage_hours": "24"},
      "2023-01-02": {"cost": "$12.30", "usage_hours": "24"},
      "2023-01-03": {"cost": "$11.20", "usage_hours": "24"},
  }
  
  # Filter sample data based on date range (basic simulation)
  filtered_data = {date: data for date, data in sample_billing_data.items() if start_date <= date <= end_date}
  
  return {"billing_report": filtered_data, "message": "This is simulated data. Actual implementation would fetch from AWS Cost Explorer."}

@mcp.tool(name="data_dictionary_tool")
def data_dictionary_tool(table_name: str = None) -> Dict:
  """
  Provides data dictionary and metadata for the configured database tables.
  If a table_name is provided, it returns the schema for that specific table.
  If no table_name is provided, it returns a list of all available tables.
  Args:
    table_name: Optional. The name of the table to get the data dictionary for.
  Returns:
    Dictionary containing the data dictionary/metadata.
  """
  if table_name:
    if table_name in schemas:
      return {table_name: schemas[table_name]}
    else:
      return {"error": f"Table '{table_name}' not found in schema."}
  else:
    return {"available_tables": list(schemas.keys()), "message": "Provide a table_name to get detailed schema."}