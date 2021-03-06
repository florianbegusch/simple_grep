import os
import sys
import tempfile
import select
import platform

import getopt
from . import grep as grep_


empty_string = ''

args_key                 = 'args'
search_recursively_key   = 'search_recursively'
full_paths_key           = 'full_paths'
do_regex_search_key      = 'do_regex_search'
display_line_numbers_key = 'display_line_numbers'

def usage():
    import subprocess

    # version_string = subprocess.Popen(
        # ("grep", "version", "setup.py"), stdout=subprocess.PIPE)
    # version = subprocess.check_output(
        # (["grep", "-Eo", "[0-9].[0-9]{1,}"]), stdin=version_string.stdout)
    # version_string.wait()

    print('simple_grep')
    # print('simple_grep, version ' + version.decode('utf-8'))
    print('')
    print('usage: simple_grep [-rnpe] [SEARCH_TERM] [FILE_TO_SEARCH]')
    print('')
    print('Arguments:')
    print('  SEARCH_TERM')
    print('  FILE_TO_SEARCH')
    print('')
    print('Options:')
    print('  -h --help         ')
    print('  -r                Search directory recursively.')
    print('  --full            Display full/absolute paths for matches.')
    print('  -e                Use the search term as a regex pattern.')
    print('  -n                Display line numbers for matches.')


def parse_command_line_options():
    search_recursively   = False
    full_paths           = False
    do_regex_search      = False
    display_line_numbers = False
    
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'hren',
                                      ['help', 'full'])

    except getopt.GetoptError as err:
        print(str(err))
        usage()
        raise KeyboardInterrupt

    if len(args) < 1:
        args = [empty_string, empty_string]
    elif len(args) == 1:
        args.insert(1, empty_string)

    for o, a in optlist:
        if o in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif o in ('-r'):
            search_recursively = True
        elif o in ('--full'):
            full_paths = True
        elif o in ('-e'):
            do_regex_search = True
        elif o in ('-n'):
            display_line_numbers = True
    
    return  { args_key: args,
              search_recursively_key: search_recursively,
              full_paths_key: full_paths,
              do_regex_search_key: do_regex_search,
              display_line_numbers_key: display_line_numbers
            }


def main():
    """Entry point for simple_grep."""

    parsed_values = parse_command_line_options()
    
    args                 = parsed_values[args_key]
    search_recursively   = parsed_values[search_recursively_key]
    full_paths           = parsed_values[full_paths_key]
    do_regex_search      = parsed_values[do_regex_search_key]
    display_line_numbers = parsed_values[display_line_numbers_key]
    
    temp_dir      = tempfile.mkdtemp()
    fd, temp_f    = tempfile.mkstemp(dir=temp_dir, suffix='.tmp', text=True)
    directory     = 1
    is_from_stdin = False
    try:

        # no stdin support for windows
        if platform.system() != 'Windows':
            # check for input - non-blocking
            is_from_stdin = (sys.stdin in 
                select.select( [sys.stdin], [], [], 0 ) [0])
            
        if is_from_stdin:
            f = open(temp_f, 'w')
            try:
                f.write(sys.stdin.read())
                directory = os.path.dirname(f.name)

            finally:
                f.close()
                assert type(directory) == str

        else:
            f = args[1]
            if f:  # verify that the specified path is a directory
                if os.path.isdir(os.path.abspath(f)):
                    directory = f
                    args[1] = empty_string

                else:
                    directory = empty_string

            else:
                directory = os.path.abspath(os.path.curdir)

        search_term = args[0] if args[0] else empty_string
        specific_file = args[1]

        searcher = grep_.Searcher(
            caller_dir=directory,
            search_term=search_term,
            specific_file=specific_file,
            is_recursive=search_recursively,
            is_abs_path=full_paths,
            is_regex_pattern=do_regex_search,
            is_search_line_by_line=display_line_numbers,
            is_from_stdin=is_from_stdin)

        searcher.run()

    except KeyboardInterrupt:
        pass

    finally:
        os.close(fd)
        os.remove(temp_f)
        os.removedirs(temp_dir)


if __name__ == "__main__":
    main()

