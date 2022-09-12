from dotenv import load_dotenv
from pydantic import BaseSettings, Field

load_dotenv()


class DevSettings(BaseSettings):
    host: str = Field(..., env='DEV_HOST')
    port: int = Field(22, env='DEV_PORT')
    username: str = Field(..., env='DEV_USER')
    password: str = Field(..., env='DEV_PASSWORD')
    secret: str = Field(..., env='DEV_SECRET')

    class Config:
        env_file = '.env'


class ServiceSettings(BaseSettings):
    start_cfg_file: str = Field('start_conf.cfg', env='START_CFG_FILE')
    run_cfg_file: str = Field('run_conf.cfg', env='RUN_CFG_FILE')

    class Config:
        env_file = '.env'


dev_settings = DevSettings()
srv_settings = ServiceSettings()
