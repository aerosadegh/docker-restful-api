"""
Main Module for run with uvicorn
"""

import subprocess
from typing import Optional

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from utils import DCli, ps
from utils import logerr
from setting import write_compose, read_compose, PATH

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


@app.get("/ps/")
def ps_item(
    all: Optional[bool] = False,
    limit: Optional[int] = -1,
):
    """read containers info"""
    try:
        res = ps(all=all, limit=limit)
    except Exception as docker_exeption:
        logerr(f"{docker_exeption}", exc_info=True)
        raise UnicornException(
            name="Client can't connect to Docker daemon!",
            code=500,
        ) from docker_exeption
    return res


@app.get("/image/{image_id}")
def read_item(image_id: str, query: Optional[str] = None):
    """return full image info with id"""
    try:
        client = DCli()
        res = {
            "image": [
                {"id": image.short_id.split(":")[-1], "tags": image.tags, "attrs": image.attrs}
                for image in client.images_list()
                if image.short_id.split(":")[-1] == image_id
            ]
        }
    except Exception as docker_exeption:
        logerr(f"{docker_exeption}", exc_info=True)
        raise UnicornException(
            name="Client can't connect to Docker daemon!",
            code=500,
        ) from docker_exeption
    return res


@app.get("/run/{service_name}")
def run_item(service_name: str, image: Optional[str] = None):
    """run service_name with specific image"""
    conf, file = read_compose(verbose=True)

    if service_name not in conf["services"].keys():
        return {"service_name": service_name, "msg": "Not Found!"}

    conf["services"][service_name]["image"] = image
    write_compose(conf)

    stat = subprocess.run(
        ["docker-compose", "-f", f"{PATH}/{file}", "up", "-d"], capture_output=True
    )

    return {
        "service_name": service_name,
        "image": image,
        "stat": stat,
    }
