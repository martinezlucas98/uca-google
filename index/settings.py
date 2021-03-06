# Settings file
    # Server
host_name = "localhost"
server_port = 8080
# Index for serving requests
index_filename = "index/indices/index.pickle"
indexed_pages_filename = "index/indices/indexed_pages.pickle"

    # Indexer
scraped_files_dir = "offline_backend/crawler/spiders/uc_data/" # obligatory trailing '/'!
# Index for building offline
dev_index_obj = "index/indices/dev_index.pickle"
# Description length shown in search results
description_len = 100