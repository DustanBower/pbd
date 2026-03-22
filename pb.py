# This file is part of pbd.
#
# Copyright (c) 2011 Dustan Bower.
#
# pbd is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# pbd is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pbd.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import textwrap
import time
import yaml

import dmenu
from platformdirs import PlatformDirs


dirs = PlatformDirs("pbd", "pbd", ensure_exists=True)
# load config
dirs.user_config_path
config_path = os.path.join(dirs.user_config_path, 'config.yml')
with open(config_path, 'r', encoding="utf-8") as file:
    config_file = yaml.safe_load(file)

    DEBUG = config_file.get("debug")

# SET UP LOGGING
logger = logging.getLogger(__name__)
log_path = os.path.join(dirs.user_log_dir, 'pb.log')
logging.basicConfig(filename=log_path, encoding='utf-8', level=logging.DEBUG)


DEFAULT_TIMEOUT = 5000
UNIMPLEMENTED_COMMANDS: list[str] = [
    'b',
    'c',
    'd',
    'g',
    'h',
    'j',
    'm',
    'r',
    'u',
    'x'
]

INPUTS = (
    ('?', 'show current song'),
    ('e', 'explain why this song is playing'),
    ('n', 'next song'),
    ('s', 'change station'),
    ('p', 'pause'),
    ('+', 'love song'),
    ('-', 'ban song'),
    ('t', 'tired of this song'),
    ('q', 'quit'),
    (':help', 'Show help message')
)


def display(text, heading="", timeout=DEFAULT_TIMEOUT):
    """
    display information to users via notifications

    :param text: text to display
    :param heading: additional information to show the user (e.g., station)
    :param timeout: time in ms that notification should be visible for
    :return: None

    """

    # word wrap if necessary by splitting into multiple lines
    max_line_length = int(os.environ.get('PBD_MAX_LINE_LEN', 0))

    if max_line_length:
        lines = textwrap.wrap(text, max_line_length)
    else:
        lines = [text]

    # display however many notifications we have left to show
    for line in lines:
        string = "notify-send "
        if timeout:
            string += f"-t {timeout} "
        string += f"\"pbd: {heading}\" "
        # Against all reason, & refuses to print, quoted or otherwise.
        # replacing it for now.
        string += f"\"{str(line.replace('&', 'and'))}\""
        os.system(string)


def get_song_title_display(data):
    """
    Get the display form of the song title.

    """
    return f"{data['artist']} - {data['title']}"


def get_station_display(data):
    """
    Get the display form of the station.

    """
    return f"[{data['stationName']}]"


def prompt(
    known_inputs: list[str],
    display_prompt: str = "",
    delay: float = 0.5
) -> str:
    """
    prompt user for input by loading dmenu

    :param known_inputs: input choices we allow
           ["0) Example Station", "2) Second Station"]
    :param display_prompt: any additional information to pass
    :param delay: how long to wait before showing prompt (default 0.5 seconds)
           a delay that is too low will react poorly with hotkeys

    :return: user selection

    """

    time.sleep(delay)
    (BLACK, GREEN) = ("#000000", "#00EE00")
    selection = dmenu.show(known_inputs, bottom=True,
                           prompt=f"pbd: {display_prompt}",
                           foreground=GREEN, background=BLACK,
                           background_selected=BLACK,
                           foreground_selected=GREEN,
                           case_insensitive=True)

    if isinstance(selection, str):
        return selection

    return ""


def datadict(data):
    """
    convert data to dictionary

    :param data: data from pianobar as \n separated strings
                    (e.g., "blah=1\nblah=2")
    :return: dictionary using each variable as a key for the data
                    (e.g., {'blah': 1, 'blah': 2})

    """

    # This function should be able to handle whatever text is in
    # /tmp/pbd.tmp. Verify that is the case if DEBUG is true.

    if DEBUG:
        data_split = data.split('\n')
        logger.debug("pb datadict> split: %s\n", data_split)
        logger.debug("datadict:")
        for i in range(len(data_split)):
            logger.debug("#%s: %s", i, data_split[i])
            try:
                dict([data_split[i].split('=', 1)])
            except Exception:
                logger.debug("LINE %s FAILED: %s", i, data_split[i])

    dict([line.split('=', 1) for line in data.split('\n') if line])
    return dict([line.split('=', 1) for line in data.split('\n') if line])
