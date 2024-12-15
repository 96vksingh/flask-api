import os

# Service id
SERVICE_ID                                    = os.getenv("id", "codingspheres-api")
APP_ENVIRONMENT                               = os.getenv("APP_ENVIRONMENT", "dev1")  
# API URI Prefix      
BASE_PATH                                     = "/v1"

DB_USER = "96vksingh"
DB_PASSWORD = "wcfyLqyKyqDsPj4u"
DB_HOST = "cluster0.ksemp.mongodb.net"
DB_NAME = "codingsphers"
WHITE_LISTED_CORS_ORIGINS                     = os.getenv("WHITE_LISTED_CORS_ORIGINS", ["http://localhost:4000","https://codingsphere-811368486283.us-central1.run.app"])

DB                                            = "mongodb+srv://{}:{}@{}/codingsphers?retryWrites=true&w=majority&appName=Cluster0".format(DB_USER,DB_PASSWORD,DB_HOST,DB_NAME)
SECRET_KEY      = "96vksingh"
LOG_LEVEL       = "INFO"