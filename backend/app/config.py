import os
from pathlib import Path


def _load_dotenv():
    """Nạp biến môi trường từ .env (không ghi đè giá trị đã có)."""
    base = Path(__file__).resolve().parents[2]
    env_path = base / ".env"
    if not env_path.is_file():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key:
            os.environ[key] = value


_load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-rova-host-secret")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(INSTANCE_DIR, 'rova_host.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
    TEMPLATE_FOLDER = os.path.join(FRONTEND_DIR, "templates")
    STATIC_FOLDER = os.path.join(FRONTEND_DIR, "static")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
