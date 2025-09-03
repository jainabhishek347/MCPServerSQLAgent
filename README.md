# AI Database Agent

A natural language interface for database interactions using AI. This project enables users to query databases using natural language through an AI agent that translates requests into optimized SQL queries.

## Overview

This project implements an AI-powered database agent that allows users to interact with databases using natural language. It leverages MCP (Machine Conversation Protocol) to handle natural language processing and generates optimized SQL queries for database operations.

## Architecture

```plaintext
┌─────────────────┐         ┌──────────────┐         ┌─────────────┐
│  Natural Lang.  │         │   AI Agent   │         │  Database   │
│    Interface    ├────────►│   (MCP)      ├────────►│  (Redshift)│
└─────────────────┘         └──────────────┘         └─────────────┘
                                  │
                                  │
                          ┌───────▼───────┐
                          │  Schema Files │
                          │    & Config   │
                          └───────────────┘
```

### Components

1. **MCP Server**: Core component handling natural language processing and query generation
2. **Database Connector**: Handles database connections and query execution
3. **Schema Manager**: Manages database schema information and permissions
4. **Query Validator**: Ensures generated queries are safe and permitted
5. **Response Formatter**: Formats database responses for user consumption

## Features

- Natural language to SQL query conversion
- Support for AWS Redshift database
- Schema-aware query generation
- Query safety validation
- Multilingual support (English/Arabic) for certain fields
- Comprehensive analytics data model support

## Installation

```bash
# Install UV first
# Then clone and set up the project
git clone <repository-url>
cd <project-directory>
```

## Configuration

### Environment Variables Setup

#### Windows
1. Using Command Prompt:
```cmd
setx DB_URL "your_database_url"
setx DB_USER "your_database_user"
setx DB_PASSWORD "your_database_password"
```
Or create a `.env` file in the project root:
```plaintext
DB_URL=your_database_url
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

#### macOS/Linux
1. Using terminal (temporary):
```bash
export DB_URL="your_database_url"
export DB_USER="your_database_user"
export DB_PASSWORD="your_database_password"
```

2. For permanent setup (bash):
```bash
echo 'export DB_URL="your_database_url"' >> ~/.bashrc
echo 'export DB_USER="your_database_user"' >> ~/.bashrc
echo 'export DB_PASSWORD="your_database_password"' >> ~/.bashrc
source ~/.bashrc
```

For zsh (macOS default):
```bash
echo 'export DB_URL="your_database_url"' >> ~/.zshrc
echo 'export DB_USER="your_database_user"' >> ~/.zshrc
echo 'export DB_PASSWORD="your_database_password"' >> ~/.zshrc
source ~/.zshrc
```

Or create a `.env` file in the project root (recommended for all platforms):
```plaintext
DB_URL=your_database_url
DB_USER=your_database_user
DB_PASSWORD=your_database_password
```

### Running the Application

#### Windows
```cmd
# Using Command Prompt
python main.py

# Using PowerShell
python main.py
```

#### macOS/Linux
```bash
# Make sure environment variables are set
python3 main.py
```

### Database Settings
The application uses environment variables for database configuration. These are loaded in `settings.py`:
```python
class ServerConfig:
    db_url: str = os.getenv('DB_URL', '')
    db_user: str = os.getenv('DB_USER', '')
    db_password: str = os.getenv('DB_PASSWORD', '')
    schema_file: str = "_api__analytics__models.yml"
```

## Using with Claude

1. **Setup Claude**:
   - Open Claude at https://claude.ai
   - Add project files as resources
   - Initialize with base prompt

2. **Send Queries**:
   ```plaintext
   "Show me total orders from last week"
   "What are the top selling products?"
   "Get customer analytics for active users"
   ```

## Project Structure

```plaintext
├── main.py              # Application entry point
├── server.py            # MCP server setup
├── tools.py            # MCP tools implementation
├── resources.py        # MCP resources
├── prompt.py          # MCP prompt handling
├── settings.py        # Configuration settings
├── helper.py          # Helper functions
└── sql_permitted_tables.json  # Database access configuration
```

## Security Features

- Query blacklist for dangerous operations
- Schema-level access control
- Database and schema validation
- Permitted tables verification
- SQL injection prevention

## Dependencies

- fastmcp
- sqlalchemy
- psycopg2-binary
- sqlalchemy-redshift
- redshift_connector
- sqlparse
- python-dotenv
- pyyaml

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

[Add License Information]

## Support

For support, please [create an issue](https://github.com/yourusername/repository/issues) on GitHub.
