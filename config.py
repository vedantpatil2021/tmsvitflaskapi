from dotenv import load_dotenv
import os
import redis

load_dotenv()
class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]
    TT_PUBLIC_KEY = os.environ["TT_PUBLIC_KEY"]

    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
