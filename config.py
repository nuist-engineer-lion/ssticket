from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Ssticket"
    lark_id: str = ""
    lark_secret: str = ""
    lark_chat: str = ""
    domain: str = ""
    host: str = ""
    port: str = ""
    lark_card: str = ""
    lark_card_v: str = ""
    table_token: str = ""
    table_id: str = ""

    model_config = SettingsConfigDict(env_file=".env")