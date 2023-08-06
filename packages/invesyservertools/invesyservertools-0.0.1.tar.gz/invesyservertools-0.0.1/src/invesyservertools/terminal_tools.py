# -*- coding: utf-8 -*-
import sys
import os
import textwrap
from colorama import Fore, Style

LIST_BULLET = '-'
COLOR_RESET = getattr(Style, 'RESET_ALL')

INDENT_MULT = 4
INDENT_BASE = 4 * ' '


def indent(level=1, raw=False, base=INDENT_MULT, base_str=' '):
    base = base * base_str
    if raw:
        return base * level
    else:
        return (base * level)[:-1]


##  Enhanced print function
#
#   @param texts: all the texts as a list
#   @param logging: you have to provide the logging object
#   @param indent: set the indentation level
#   @param list_bullet: True or provide a string
#   @param color: can be a string or a dictionary: {index: color}.
#                 Example: {1: 'red', 4: 'blue'}. index begins with 1
#   @param style
#   @param sep: as in print function
#   @param end: as in print function
#   @param ignore: don't print (but possibly log)
#   @param flush: as in print function
#   @param nowrapper: don't use textwrap
def print_(
    *texts: list,
    logging: bool = False,
    indent: int = 0,
    list_bullet: (bool, str) = '',
    color: (str, dict) = '',
    style: str = '',
    sep: str = ' ',
    end: str = '\n',
    ignore: bool = False,
    flush: bool = False,
    nowrapper: bool = False
) -> None:
    """Enhanced print function"""

    texts = [str(t) for t in texts]

    if logging:
        logging.info(sep.join(texts))

    if ignore:
        return

    colors = None
    if isinstance(color, dict):
        colors = color
        color = None

    if len(texts):
        try:
            prefix = ' ' * indent
        except TypeError:
            prefix = indent or ''

        suffix = ''
        prefix_len_subtract = 0
        if color or style:
            prefix += getattr(
                Fore,
                color.upper(), ''
            ) + getattr(
                Style, style.upper(),
                ''
            )
            prefix_len_subtract = len(prefix) - 2
            suffix = COLOR_RESET

        if colors:
            texts_colored = []
            for i, t in enumerate(texts, start=1):
                p = s = ''
                if i in colors:
                    p = getattr(Fore, colors[i].upper())
                    s = COLOR_RESET

                texts_colored.append(p + t + s)

            texts = texts_colored

        if isinstance(list_bullet, bool):
            if list_bullet:
                list_bullet = LIST_BULLET
            else:
                list_bullet = ''

        bullet_sep = ' '
        prefix += list_bullet + bullet_sep if list_bullet else ''

        try:  # when there is no terminal, i.e. cron-job
            term_rows, term_columns = map(
                int,
                os.popen('stty size', 'r').read().split()
            )
            wrapper = textwrap.TextWrapper(
                initial_indent=prefix,
                width=term_columns,
                subsequent_indent=' ' * (len(prefix) - prefix_len_subtract)
            )
        except ValueError:
            nowrapper = True

        if flush or nowrapper:
            print(
                prefix + texts[0],
                *texts[1:],
                suffix,
                sep=sep,
                end=end,
                flush=flush
            )
        else:
            msg = sep.join(
                [t for t in texts]
            ) + suffix + end
            print(wrapper.fill(msg))

    else:
        print()


## Wait for a key press on the console and return it
def wait_for_key(
    text: str = 'continue: press any button',
    color: str = 'black',
    list_bullet: (bool, str) = False
) -> 'None or str':
    ''' Wait for a key press on the console and return it.'''

    if text:
        print_(
            text,
            color=color,
            list_bullet=list_bullet
        )

    result = None

    import termios
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    try:
        result = sys.stdin.read(1)
    except IOError:
        pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result
