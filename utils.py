"""
some utils to use in API
"""
import logging
import logging.config
from time import sleep

import docker

logging.config.fileConfig("logging.conf", disable_existing_loggers=False)

logger = logging.getLogger("myApp")
log = logger.info
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
        log(f"Connected: {self.connected}")

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


if __name__ == "__main__":
    DCli()
