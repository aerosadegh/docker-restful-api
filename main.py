"""
Main Module for run with uvicorn
"""

from typing import Optional

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from utils import DCli
from utils import logerr
from utils import loginf

##########################
## create Instance objects
app = FastAPI()


class UnicornException(Exception):
    """custom exception class"""

    def __init__(self, name: str, code: int):
        """init class"""
        super().__init__()
        self.name = name
        self.code = code


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    """custom exception handler"""
    loginf(f"{request}")
    return JSONResponse(
        status_code=exc.code,
        content={"message": f"Oops! {exc.name}"},
    )


@app.get("/")
def read_root():
    """root access"""
    try:
        client = DCli()
        res = {
            "images": [
                {"id": image.short_id.split(":")[-1], "tags": image.tags}
                for image in client.images_list()
            ]
        }
    except Exception as docker_exeption:
        logerr(f"{docker_exeption}", exc_info=True)
        raise UnicornException(
            name="Client can't connect to Docker daemon!",
            code=500,
        ) from docker_exeption
    return res


@app.get("/image/{item_id}")
def read_item(item_id: str, query: Optional[str] = None):
    """read item test"""
    return {
        "item_id": item_id,
        "query": query,
    }


@app.get("/run/{item_name}")
def run_item(service_name: str, query: Optional[str] = None):
    """read item test"""
    return {
        "service_name": service_name,
        "query": query,
    }
