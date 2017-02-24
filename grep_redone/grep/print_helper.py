"""Print matched items for grep_redone."""

import os
from clint.textui import colored

def print_matched_files_full_path(matched_lines, search_term):

    output = []
    for file, lines in matched_lines.iteritems():
        output = [(colored.magenta(file + ':', True, False) +
                  str(line_num) + ':' + line) for line_num, line in lines.iteritems()
                 ]

    # Remove last occurrence of new line
    output = [rreplace(f, '\n', '', 1) for f in output]

    # Color search term yellow.
    if search_term:
        output = [f.replace(search_term, colored.green(search_term, True, False).__str__()) for f in output]

    for f in output:
        print f

    return output

def print_matched_files_relative_path(matched_lines, search_term):

    output = []
    for file, lines in matched_lines.iteritems():
            output = [(colored.magenta("./" + os.path.relpath(file) + ':', True, False) +
                      str(line_num) + ':' + line) for line_num, line in lines.iteritems()
                     ]

    # Remove last occurrence of new line
    output = [rreplace(f, '\n', '', 1) for f in output]

    # Color search term yellow.
    if search_term:
        output = [f.replace(search_term, colored.green(search_term, True, False).__str__()) for f in output]

    for f in output:
        print f

    return output

def rreplace(string, old, new, num_occurrences):
    li = string.rsplit(old, num_occurrences)
    return new.join(li)