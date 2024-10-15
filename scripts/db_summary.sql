-- Start writing to db_struct.txt
\o db_struct.txt  

\echo 'Database Summary'
\echo '-----------------'

-- Show schemas
\echo '\nSchemas:'
SELECT nspname AS "Name", pg_catalog.pg_get_userbyid(nspowner) AS "Owner"
FROM pg_catalog.pg_namespace
WHERE nspname !~ '^pg_' AND nspname <> 'information_schema'
ORDER BY 1;

-- Show current schema path
\echo '\nSearch Path:'
SHOW search_path;

-- List all tables
\echo '\nList of Tables:'
SELECT schemaname, tablename, tableowner 
FROM pg_tables 
WHERE schemaname = 'public';

-- Describe the structure of each table

\echo '\n--- Table: attachedfiles ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'attachedfiles';

\echo '\n--- Table: changes ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'changes';

\echo '\n--- Table: deletedfiles ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'deletedfiles';

\echo '\n--- Table: deletedresources ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'deletedresources';

\echo '\n--- Table: dicomidentifiers ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'dicomidentifiers';

\echo '\n--- Table: exportedresources ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'exportedresources';

\echo '\n--- Table: globalintegers ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'globalintegers';

\echo '\n--- Table: globalproperties ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'globalproperties';

\echo '\n--- Table: labels ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'labels';

\echo '\n--- Table: maindicomtags ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'maindicomtags';

\echo '\n--- Table: metadata ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'metadata';

\echo '\n--- Table: patientrecyclingorder ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'patientrecyclingorder';

\echo '\n--- Table: remainingancestor ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'remainingancestor';

\echo '\n--- Table: resources ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'resources';

\echo '\n--- Table: serverproperties ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'serverproperties';

\echo '\n--- Table: storagearea ---'
SELECT 
    column_name, 
    data_type, 
    character_maximum_length,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'storagearea';

-- Stop writing to db_struct.txt
\o

\echo 'Output has been written to db_struct.txt'
