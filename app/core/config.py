# Configurações principais, como database, CORS, etc.
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv("app/.env") # D:\PythonMeusProjetos\Brasileirao\app\.env 

class Settings:
    ALGORITHM = os.getenv("ALGORITHM")
    minutes = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(minutes) if minutes is not None else 15
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")    
    # Database settings
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    # CORS settings
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    # Other settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()