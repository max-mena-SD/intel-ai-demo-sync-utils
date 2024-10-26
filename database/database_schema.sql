
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
    status TEXT DEFAULT 'active'
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

CREATE TABLE IF NOT EXISTS ai_demo_dashboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prim TEXT,
    demo_type TEXT,
    demo_description TEXT,
    demo_link TEXT,
    demo_team TEXT,
    usage_requirements TEXT,
    tech TEXT,
    start_date TEXT,
    status TEXT-- Table to track processed demos
);

CREATE TABLE IF NOT EXISTS processed_demos_control (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    demo_id TEXT,                    -- Reference to the demo being processed
    source_table TEXT,               -- Which table the demo came from (metadata_map or ai_demo_dashboard)
    processing_status TEXT,          -- Status of the processing (pending, completed, failed)
    processing_date TIMESTAMP,       -- When the processing occurred
    json_file_path TEXT,            -- Where the JSON file was saved
    error_message TEXT,             -- Any error messages during processing
    last_modified_date TIMESTAMP,    -- Last time this record was updated
    created_date TIMESTAMP,          -- When this record was created
    processed_by TEXT,              -- Who or what process handled this
    version TEXT,                   -- Version of the processing script
    
    -- Add foreign key constraints as needed
    FOREIGN KEY (demo_id) REFERENCES metadata_map(id_name),
    
    -- Add indexes for frequently queried columns
    CREATE INDEX idx_demo_id ON processed_demos_control(demo_id),
    CREATE INDEX idx_processing_status ON processed_demos_control(processing_status),
    CREATE INDEX idx_processing_date ON processed_demos_control(processing_date)
);

-- View to get processing statistics
CREATE VIEW IF NOT EXISTS processing_stats AS (
    SELECT 
        source_table,
        processing_status,
        COUNT(*) as count,
        MIN(processing_date) as earliest_process,
        MAX(processing_date) as latest_process
    FROM processed_demos_control
    GROUP BY source_table, processing_status);

CREATE INDEX IF NOT EXISTS idx_metadata_map_status ON metadata_map(status);
CREATE INDEX IF NOT EXISTS idx_metadata_map_createDate ON metadata_map(createDate);
CREATE INDEX IF NOT EXISTS idx_metadata_map_modifiedDate ON metadata_map(modifiedDate);
CREATE INDEX IF NOT EXISTS idx_demo_links_metadata_id ON demo_links(metadata_id);
CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(tag_name);
