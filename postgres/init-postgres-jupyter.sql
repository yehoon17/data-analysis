-- Create the role 'jupyter_user' only if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_roles WHERE rolname = 'jupyter_user'
    ) THEN
        CREATE ROLE jupyter_user WITH LOGIN PASSWORD 'your_password';
    END IF;
END $$;

-- Create the database 'neo_bank' only if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_database WHERE datname = 'neo_bank'
    ) THEN
        CREATE DATABASE neo_bank
            OWNER jupyter_user
            ENCODING 'UTF8'
            LC_COLLATE='C'
            LC_CTYPE='C'
            TEMPLATE=template0;
    END IF;
END $$;

-- Restrict permissions on the default 'postgres' database
REVOKE CONNECT ON DATABASE postgres FROM PUBLIC;

-- Connect to the 'neo_bank' database
\connect neo_bank;

-- Restrict public schema permissions
REVOKE ALL ON SCHEMA public FROM PUBLIC;
GRANT USAGE ON SCHEMA public TO jupyter_user;
GRANT CREATE ON SCHEMA public TO jupyter_user;

-- Set default privileges for 'jupyter_user' on the 'public' schema
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO jupyter_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT EXECUTE ON FUNCTIONS TO jupyter_user;

-- Optional: Grant full ownership of the schema (if needed)
ALTER SCHEMA public OWNER TO jupyter_user;
