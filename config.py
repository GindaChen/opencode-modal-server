# Modal Configuration
# This file contains configuration settings for the Modal deployment

# App settings
APP_NAME = "opencode-server"
VOLUME_NAME = "opencode-storage"
STORAGE_PATH = "/storage"

# Container settings
CONTAINER_IDLE_TIMEOUT = 300  # seconds (5 minutes)
JOB_TIMEOUT = 3600  # seconds (1 hour)
MAX_CONCURRENT_INPUTS = 100

# Python version
PYTHON_VERSION = "3.11"
