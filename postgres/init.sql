-- Create roles
CREATE ROLE airflow_user WITH LOGIN PASSWORD 'airflow_password';
CREATE ROLE task_user WITH LOGIN PASSWORD 'task_password';

-- Create databases
CREATE DATABASE airflow_db
    OWNER airflow_user
    ENCODING 'UTF8'
    LC_COLLATE='C'
    LC_CTYPE='C'
    TEMPLATE=template0;

CREATE DATABASE task_db
    OWNER task_user
    ENCODING 'UTF8'
    LC_COLLATE='C'
    LC_CTYPE='C'
    TEMPLATE=template0;

-- Restrict permissions on the default database (optional)
REVOKE CONNECT ON DATABASE postgres FROM PUBLIC;

-- Set up airflow_db
\connect airflow_db;

-- Restrict public schema permissions
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO airflow_user;
GRANT CREATE ON SCHEMA public TO airflow_user;

-- Default privileges for airflow_user
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO airflow_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT EXECUTE ON FUNCTIONS TO airflow_user;

-- Set up task_db
\connect task_db;

-- Restrict public schema permissions
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO task_user;
GRANT CREATE ON SCHEMA public TO task_user;

-- Default privileges for task_user
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO task_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT EXECUTE ON FUNCTIONS TO task_user;

-- Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
