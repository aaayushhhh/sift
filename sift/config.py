from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    mode: str = "offline"
    model: str = "gpt-4.1-mini"
    knowledge_dir: Path = ROOT / "data" / "knowledge"
    top_k: int = 4

    model_config = SettingsConfigDict(env_file=".env", env_prefix="SIFT_", extra="ignore")


settings = Settings()
