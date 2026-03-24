-- Set password for postgres user
ALTER USER postgres WITH PASSWORD 'postgres';

-- Create jobportal user
CREATE USER jobportal WITH PASSWORD 'jobportal123';

-- Grant privileges
ALTER DATABASE job_portal OWNER TO jobportal;
GRANT ALL PRIVILEGES ON DATABASE job_portal TO jobportal;
