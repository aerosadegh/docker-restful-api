"""
some utils to use in API
"""
import logging
import logging.config
from time import sleep

import docker

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger("myApp")

loginf = logger.info
logdbg = logger.debug
logwrn = logger.warning
logerr = logger.error


class DCli:
    """Docker client class"""

    def __init__(self):
        """init class"""
        self._connected = None
        self.connect_to_cli()

    @property
    def connected(self) -> bool:
        """get connected state in bool (read-only property)"""
        return self._connected

    def status(self):
        """log connection status"""
        loginf(f"Connected: {self.connected}")

    def connect_to_cli(self, retry_times=3, retry_interval=2):
        """try to connect to docker sock"""
        for i in range(retry_times, 0, -1):
            try:
                client = docker.from_env()
            except docker.errors.DockerException:
                logwrn(
                    f"cannot connect to the Docker daemon; retry {i} times. "
                    f"sleep {retry_interval} (sec) ..."
                )
                sleep(2)
            except Exception as _:
                logerr("Error:>", exc_info=True)
                logwrn(f"retry {i} times. " f"sleep {retry_interval} (sec) ...")
                sleep(2)
            else:
                break
        else:
            self._connected = False
            raise ConnectionError("cannot connect to the Docker daemon!")
        self.cli = client
        self._connected = True

    def images_list(self):
        """return images list"""
        self.connect_to_cli()
        return self.cli.images.list()

    def containers_list(self, **kwargs):
        """return containers list
        kwargs:
            all=False
            limit=-1
            # before=None
            # filters=None
            # since=None
            # sparse=False
            # ignore_removed=False
        """
        self.connect_to_cli()
        return self.cli.containers.list(**kwargs)


def get_cli():
    client = DCli()
    return client


def ps(all=False, limit=-1):
    client = get_cli()

    res = {
        "containers": [
            {
                "id": container.short_id.split(":")[-1],
                "tags": container.name,
                "status": (
                    f"{container.status}"
                    if container.status == "running"
                    else f"{container.status}" f' ({container.attrs.get("State").get("ExitCode")})'
                ),
                "image": {
                    "id": container.image.short_id.split(":")[-1],
                    "tags": container.image.tags,
                },
                "ports": container.attrs.get("NetworkSettings").get("Ports"),
            }
            for container in client.containers_list(all=all, limit=limit)
        ]
    }
    return res


if __name__ == "__main__":
    DCli()
