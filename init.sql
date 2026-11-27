CREATE USER challenge_test
    WITH PASSWORD 'test_password';

CREATE DATABASE challenge_test
    OWNER challenge_test;

REVOKE CONNECT ON DATABASE challenge_db FROM PUBLIC;