# Settings file
    # Server
host_name = "localhost"
server_port = 8080
# Index for serving requests
index_filename = "index/indices/index.pickle"

    # Indexer
scraped_files_dir = "../crawler/spiders/uc_data/" # obligatory trailing '/'!
# Index for building offline
dev_index_obj = "index/indices/dev_index.pickle"