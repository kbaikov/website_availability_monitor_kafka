CREATE TABLE IF NOT EXISTS monitor
(
    id              SERIAL  PRIMARY KEY,
    site                VARCHAR,
    status_code         VARCHAR,
    reason              VARCHAR,
    response_time       FLOAT,
    expected_contents   VARCHAR
);
