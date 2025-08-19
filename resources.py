from server import mcp, schemas 
from typing import Any
import json

@mcp.resource("file://database_permitted_tables")
def database_permitted_tables() -> Any:
  '''
  Returns information about database, schema and tables which are allowed to acces  or execute sql query against.
  '''
  with open("sql_permitted_tables.json") as f:
    data = json.load(f)
  data['tables'] = list(schemas.keys())
  return data
  