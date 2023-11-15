# Weasley Clock - Software

Python software for the Weasley Clock project.

## Setup and configuration

Install the required dependencies with [poetry](https://python-poetry.org/):

```bash
poetry install
```

To fully set up the clock, you must provide a configuration and calendar file for each of the three users.
The calendar file has to be in the iCalendar format (`.ics`),
the configuration can be adapted from the example file `sample_user.yaml`.  
A JSON-schema for the configuration file is available in `user_config.schema.json`.  
The filenames have to be the number of the user followed by extension, for example `1.yaml` and `1.ics` for user 1.

The configuration file specifies the user's work hours (don't forget to include leading zeros!) and,
for each available location, a set of keywords to match against the calendar events.

## Usage

To run the software, simply execute the `main.py` script:

```bash
poetry run python main.py
```

## License

```
Copyright 2023 Max Rumpf

This program is free software: you can redistribute it and/or modify it under the terms
of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This software is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.
```
