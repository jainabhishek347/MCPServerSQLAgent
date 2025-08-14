from typing import Optional, Literal
class ServerConfig():
  db_url:str = 'localhost:5439/dev?sslmode=allow'
  db_user:str = 'analytics_api' # 'analytics_api_dev'
  db_password:str = '2WTdwC0LyMTr76d6jP' # 'xiZ8nQ90l4EKRtMWA1'
  mcp_transport: Literal["stdio", "streamable-http"] = "streamable-http"