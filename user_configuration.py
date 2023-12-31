# Copyright 2023 Max Rumpf
#
# This file is part of Weasley Clock.
#
# Weasley Clock is free software: you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this software.
# If not, see <https://www.gnu.org/licenses/>.

from datetime import time

from pydantic import BaseModel, ValidationError
from pydantic_yaml import parse_yaml_file_as

from calendar_helper import Event, get_time


class WorkHours(BaseModel):
    start: time
    end: time


class LocationKeywords(BaseModel):
    home: list[str]
    work: list[str]
    lecture: list[str]
    meeting: list[str]
    conference: list[str]
    vacation: list[str]

    @staticmethod
    def priority(location: str) -> int:
        """
        Returns the priority of a location.
        """
        return {
            'home': 0,
            'work': 1,
            'lecture': 2,
            'meeting': 3,
            'conference': 4,
            'vacation': 5,
        }[location]


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
            return parse_yaml_file_as(UserConfiguration, filename)
        except FileNotFoundError:
            print(f'Missing configuration file {filename}')
            return None
        except ValidationError:
            print(f'Invalid configuration file {filename}')
            return None

    def map_location(self, event: Event) -> str | None:
        """
        Maps an event to a location via keywords.
        """
        for location, keywords in self.keywords.model_dump().items():
            for keyword in keywords:
                summary = event.summary.lower()
                # Location or keywords matches summary
                if location.lower() in summary or keyword.lower() in summary:
                    return location

        return None

    def calculate_fallback_location(self) -> str:
        """
        Calculates the fallback location based on the current time and day.
        """
        now = get_time()
        working_day = now.weekday() < 5
        if working_day and self.work_hours.start <= now.time() <= self.work_hours.end:
            return 'work'
        else:
            return 'home'
