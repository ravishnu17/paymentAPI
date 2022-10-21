from pydantic import BaseSettings

class Secrets(BaseSettings):
    client_id:str
    secret_key:str
    dbname:str
    dbuser:str
    dbpassword:str
    host:str
    port:int
    
    class Config:
        env_file='.env'
        
secret = Secrets()