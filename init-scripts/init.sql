/*Here are some database initialization procedures for testing*/
CREATE TABLE IF NOT EXISTS data_table (
    id serial PRIMARY KEY,
    data JSONB
);

/*
INSERT INTO data_table (id, data)
VALUES
    (1, '{"text": "Sample text 1", "author": "Author 1", "tags": "tag1, tag2"}'),
    (2, '{"text": "Sample text 2", "author": "Author 2", "tags": "tag2, tag3"}'),
    (3, '{"text": "Sample text 3", "author": "Author 3", "tags": "tag3, tag4"}'),
    (4, '{"text": "Sample text 4", "author": "Author 4", "tags": "tag4, tag5"}'),
    (5, '{"text": "Sample text 5", "author": "Author 5", "tags": "tag5, tag1"}');
*/