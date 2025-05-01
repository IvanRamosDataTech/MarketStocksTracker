-- IMPORTANT NOTE: Postgresql automatically generates a transaction block when detects 2 or more statements in a script. You  may face following error
-- ERROR:  CREATE DATABASE cannot run inside a transaction block if you try to run script all at once. 
-- To avoid that error, first copy and paste database creation statement to your SQL Query Tool, execute statement by statement.

-- Stage/Development database
CREATE DATABASE marketstockstracker_dev
    WITH
    OWNER = admin
    ENCODING = 'UTF8'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;


-- Production database
CREATE DATABASE marketstockstracker
    WITH
    OWNER = admin
    ENCODING = 'UTF8'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

-- ... And then copy and paste this one. Execute it.
COMMENT ON DATABASE marketstockstracker_dev
    IS '[DEVELOPMENT SYSTEM] all your coding efforts should point to this environment';

-- And finally this one
COMMENT ON DATABASE marketstockstracker
    IS 'Contains Historical data about of stocks of interest so user can track their portfolio performance over time';