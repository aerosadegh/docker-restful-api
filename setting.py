"""
  some setting for project
"""


from os import listdir
from os.path import isfile
from os.path import join

import yaml

DEBUG = True
PATH = "compose"


def read_compose(path=PATH, verbose=False):
    """read docker-compose.yaml file from PATH"""
    files = filter(lambda items: isfile(join(path, items)), listdir(path))
    for file in files:
        if verbose:
            print("Load file:>", file)
        with open(join(path, file), "r", encoding="utf-8") as fin:
            conf = yaml.safe_load(fin)
        break
    else:
        raise FileNotFoundError(f"No any file exist in {path!r} directory!")
    return conf


def write_compose(conf, path=PATH, filename="docker-compose.yaml"):
    """write yaml conf in docker-compose file in path"""
    with open(join(path, filename), "w", encoding="utf-8") as fout:
        yaml.dump(conf, fout)


print(read_compose())
## select service to compose up
### docker-compose  -f "compose/docker-compose.yml" up -d --build rdb grf
