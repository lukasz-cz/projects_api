class Config:
    MONGO_URI = "mongodb://mongo:27017/projects_db"
    MONGO_DBNAME = "projects_db"

class DevelopmentConfig(Config):
    DEBUG = True
