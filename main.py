"""
Main Module for run with uvicorn
"""

from typing import Optional

import docker
from fastapi import FastAPI


app = FastAPI()

client = docker.from_env()


@app.get("/")
def read_root():
    """root access"""
    return {
        "images": {image.short_id.split(":")[-1]: image.tags for image in client.images.list()}
    }


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
