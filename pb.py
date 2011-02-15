
DEFAULT_TIMEOUT = 5000

inputs = (
    ('?', 'show current song'),
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
    string = "notify-send "
    if timeout:
       string += "-t %d " % timeout 
    string += "\"pbd: %s\" " % heading
    # Against all reason, & refuses to print, quoted or otherwise.
    # replacing it for now.
    string += "\"%s\"" % str(input.replace('&', 'and'))
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

