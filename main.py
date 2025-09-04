import warnings
warnings.filterwarnings("ignore", message=".*pkg_resources is deprecated.*")
warnings.filterwarnings("ignore", message=".*ssl.SSLContext() without protocol.*")

from server import mcp
from settings import ServerConfig

# Import tools,resources and prompts so they get registered via decorators
from tools import run_sql_query, get_tables_schema, sql_query_optimizer, redshift_billing_analyzer, data_dictionary_tool
from resources import database_permitted_tables
from prompt import get_data

# Entry point to run the server
if __name__ == "__main__":
    mcp.run(transport = ServerConfig().mcp_transport)