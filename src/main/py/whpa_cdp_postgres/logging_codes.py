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
ERROR_EXECUTING_SQL = (
    "PGLIBERR002",
    "Caught exception '%s' when running SQL statement '%s'",
)

# Warnings
TABLE_NOT_FOUND = (
    "PGLIBWARN002",
    "Table '%s' not found. Assuming schema is not installed and version is 0",
)

# Info
DATABASE_EXISTS = ("PGLIBLOG002", "Database already exists, not creating.")
CREATING_SCHEMA_VERSION_TABLE = (
    "PGLIBLOG003",
    "Creating schema_version table in schema '%s'",
)
