from typing import Optional, Literal
from dotenv import load_dotenv
import os

load_dotenv()

class ServerConfig:
    db_url: str = ""
    db_user: str = ""
    db_password: str = ""
    mcp_transport: Literal["stdio", "streamable-http"] = "streamable-http"
    schema_file:str = "_api__analytics__models.yml"