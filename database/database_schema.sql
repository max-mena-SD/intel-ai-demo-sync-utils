
CREATE TABLE IF NOT EXISTS metadata_premap (
            id_name TEXT PRIMARY KEY,
            name TEXT,
            link TEXT,
            description TEXT, 
            platform TEXT,
            summary TEXT,
            update_date TEXT
        );
        
-- Main metadata table
CREATE TABLE IF NOT EXISTS metadata_map (
    id_name TEXT PRIMARY KEY,        -- Unique identifier for each metadata record
    title TEXT,
    path TEXT,
    imageUrl TEXT,
    createDate TEXT,
    modifiedDate TEXT,
    link TEXT
);

-- Tag categories table
CREATE TABLE IF NOT EXISTS tag_categories (
    category_id INTEGER PRIMARY KEY,  -- Unique identifier for each category
    category_name TEXT                -- E.g., 'categories', 'tasks', 'libraries', 'other'
);

-- Tags table
CREATE TABLE IF NOT EXISTS tags (
    tag_id INTEGER PRIMARY KEY,       -- Unique identifier for each tag
    category_id INTEGER,              -- Foreign key linking to tag_categories
    tag_name TEXT,                    -- Name of the tag, e.g., 'Keras', 'Retail', etc.
    FOREIGN KEY (category_id) REFERENCES tag_categories(category_id)
);

-- Mapping table between metadata_map and tags
CREATE TABLE IF NOT EXISTS metadata_tags_map (
    id INTEGER PRIMARY KEY,           -- Unique identifier for this mapping
    metadata_id TEXT,                 -- Foreign key linking to metadata_map.id_name
    tag_id INTEGER,                   -- Foreign key linking to tags.tag_id
    FOREIGN KEY (metadata_id) REFERENCES metadata_map(id_name),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
);
