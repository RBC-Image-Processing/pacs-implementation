-- Drop the public schema and all contents, and recreate it
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

-- Set default permissions for your user and the public role
GRANT ALL ON SCHEMA public TO midap_pacs_db_user;
GRANT ALL ON SCHEMA public TO public;


VACUUM FULL;
