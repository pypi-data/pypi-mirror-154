from pydantic import BaseModel
import yaml
from typing import Literal
from pathlib import Path


BASE_CONFIF_FILE = Path(__file__).parent / 'config.yaml'

class Config(BaseModel):
    registerName: Literal['pandas', 'dict']


def load_config(path: str) -> Config:
    with open(path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
        return Config(**data)


