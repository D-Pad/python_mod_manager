import crayons
from os import system


###########################################
#               FUNCTIONS                 #
###########################################
def colorize(text):
    """Pass a block of ascii art here to color them by rows."""

    lines = text.split('\n')
    del lines[0]
    string = ''
    count = 0
    maximum = 5
    for i in range(len(lines)):
        if count == 0:
            string += crayons.red(lines[i] + '\n')
        elif count == 1:
            string += crayons.magenta(lines[i] + '\n')
        elif count == 2:
            string += crayons.blue(lines[i] + '\n')
        elif count == 3:
            string += crayons.cyan(lines[i] + '\n')
        elif count == 4:
            string += crayons.green(lines[i] + '\n')
        elif count == maximum:
            string += crayons.yellow(lines[i] + '\n')
        count = count + 1 if count < maximum else 0

    return string


def dye(txt, col):
    """Colors text"""
    if isinstance(col, str):
        col = col.lower()

    if col == 'red':
        txt = crayons.red(txt)
    elif col == 'blue':
        txt = crayons.blue(txt)
    elif col == 'green':
        txt = crayons.green(txt)
    elif col == 'yellow':
        txt = crayons.yellow(txt)
    elif col == 'magenta':
        txt = crayons.magenta(txt)
    elif col == 'cyan':
        txt = crayons.cyan(txt)
    return txt

