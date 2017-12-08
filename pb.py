## This file is part of pbd.
##
## Copyright (c) 2011 Dustan Bower.
##
## pbd is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 2 of the License, or
## (at your option) any later version.
##
## pbd is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with pbd.  If not, see <http://www.gnu.org/licenses/>.

DEFAULT_TIMEOUT = 5000

inputs = (
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

def display(input, heading="", timeout=DEFAULT_TIMEOUT):
    import os
    import textwrap

    max_line_length = int(os.environ.get('PBD_MAX_LINE_LEN', 0))

    if max_line_length:
        lines = textwrap.wrap(input, max_line_length)
    else:
        lines = [input]

    for line in lines:
        string = "notify-send "
        if timeout:
            string += "-t %d " % timeout 
        string += "\"pbd: %s\" " % heading
        # Against all reason, & refuses to print, quoted or otherwise.
        # replacing it for now.
        string += "\"%s\"" % str(line.replace('&', 'and'))
        os.system(string)

def prompt(known_inputs, prompt="", delay=0.5):
    import subprocess
    import time
    time.sleep(delay)
    # triple quotes won't work here.  If the quotes aren't escaped, they
    # don't function properly.
    (BLACK, GREEN) = ("#000000", "#00EE00")
    string = "dmenu -b "
    string += "-nb \"%s\" -nf \"%s\" " % (BLACK, GREEN)
    string += "-sb \"%s\" -sf \"%s\" " % (GREEN, BLACK)
    string += "-p \"pbd: %s\" <<< \"%s\"" % (prompt, known_inputs)
    input = subprocess.check_output(string, shell=True).strip()
    return input

