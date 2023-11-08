from datetime import time

import pydantic_yaml
from pydantic import BaseModel, ValidationError


class WorkHours(BaseModel):
    start: time
    end: time


class LocationKeywords(BaseModel):
    home: list[str]
    work: list[str]
    meeting: list[str]
    lecture: list[str]
    conference: list[str]
    vacation: list[str]


class UserConfiguration(BaseModel):
    work_hours: WorkHours
    keywords: LocationKeywords

    @classmethod
    def load_configuration(cls, user_num: int):
        """
        Loads a configuration from disk.
        """
        filename = f'{user_num + 1}.yaml'
        try:
            return pydantic_yaml.parse_yaml_file_as(UserConfiguration, filename)
        except FileNotFoundError:
            print(f'Missing configuration file {filename}')
            return None
        except ValidationError:
            print(f'Invalid configuration file {filename}')
            return None
