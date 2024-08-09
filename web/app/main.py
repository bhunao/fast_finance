import logging
from fastapi import FastAPI


log_format = (
    "[%(asctime)s | %(name)s | %(levelname)s | "
    "%(filename)s:%(lineno)d | %(funcName)s]: %(message)s"
)
logging.basicConfig(format=log_format, level=logging.INFO)

app = FastAPI()


@app.get("/check_health")
def check_health():
    """Endpoint for testing if the web server is online."""
    return True
