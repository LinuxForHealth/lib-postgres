# *******************************************************************************
# IBM Watson Imaging Common Application Framework 3.0                         *
#                                                                             *
# IBM Confidential                                                            *
#                                                                             *
# OCO Source Materials                                                        *
#                                                                             *
# (C) Copyright IBM Corp. 2019                                                *
#                                                                             *
# The source code for this program is not published or otherwise              *
# divested of its trade secrets, irrespective of what has been                *
# deposited with the U.S. Copyright Office.                                   *
# ******************************************************************************/

# Errors
CONFIG_ACCESSED_BEFORE_LOADING = (
    "PGLIBERR001",
    "attempted to access configurations before loading them",
)
ERROR_EXECUTING_SQL = (
    "PGLIBERR002",
    "Caught exception '%s' when running SQL statement '%s'",
)

# Warnings
MISSING_CONFIG_ENV = (
    "PGLIBWARN001",
    "'%s' environment variables not defined. Loading default config...",
)
MISSING_CONFIG_FILE = (
    "PGLIBWARN002",
    "Config file '%s' not found. Please check config file path and name...",
)
TABLE_NOT_FOUND = (
    "PGLIBWARN002",
    "Table '%s' not found. Assuming schema is not installed and version is 0",
)

# Info
LOADING_CONFIG = ("PGLIBLOG001", "Loading postgres config and secrets from: '%s' and '%s'")
DATABASE_EXISTS = ("PGLIBLOG002", "Database already exists, not creating.")
CREATING_SCHEMA_VERSION_TABLE = (
    "PGLIBLOG003",
    "Creating schema_version table in schema '%s'",
)
