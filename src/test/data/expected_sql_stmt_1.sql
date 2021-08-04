CREATE TABLE IF NOT EXISTS test_db_schema_name.schema_version (
    version TEXT NOT NULL,
    created_on TIMESTAMP DEFAULT current_timestamp
)