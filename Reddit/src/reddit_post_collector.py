"""
Author:	eric zair
File: collect.py
Description: TBA

@doxyfile
"""
import praw
import argparse
from credentials.reddit_credentials import API_INSTANCE


# Handle argparsing.
def get_argument_parser_containing_program_flag_information():
    """
    Returns Loads up an argument_parser object with the value that the
    command line argument that the user gave to the program.

    NOTE: There is only ONE command line argument that has been passed by the
    user contained in here!

    Returns:
        parser {argparse.ArgumentParser} -- Contains the single command line
                                            argument that the user passed into
                                            the program.
    """
    parser = argparse.ArgumentParser()
#    parser = argparse.ArgumentParser(add_help=False)

    # This line makes it so that the user can only choose one option of the
    # rather than being able to call both add and remove for example.
    argument_to_execute = parser.add_mutually_exclusive_group()

    argument_to_execute.add_argument('--collect', help='Prompt the user for '
                                                       'a datarange and being '
                                                       'collecting the data. '
                                                       'When we are done with '
                                                       'collecting, we add '
                                                       'the data to the '
                                                       'database. ')

    argument_to_execute.add_argument('--add', help='Add the sub-reddit passed '
                                                   'in by the user '
                                                   'to the list of '
                                                   'sub-reddits '
                                                   'that we will collect '
                                                   'data from.')

    argument_to_execute.add_argument('--remove', help='Remove the subreddit '
                                                      'passed in by the user.')
    return parser


def add_sub_reddit_to_db_file(path_to_sub_reddit_file='../sub_reddits.txt'):
    """
    Appends a sub_reddit to the end of the file that is given by the user.

    Keyword Arguments:
        path_to_sub_reddit_file {str} -- Path to a file containing the list of
                                         sub_reddits to add to.
                                         (default: {'../sub_reddits.txt'})
    """
    print("func 1")


def remove_sub_reddit_in_db_file(path_to_sub_reddit_fil='../sub_reddits.txt'):
    """
    Removes a sub_reddit (line in the file) to the end of the file that
    is given by the user.

    Keyword Arguments:
        path_to_sub_reddit_file {str} -- Path to a file containing the list of
                                         sub_reddits to remove from.
                                         (default: {'../sub_reddits.txt'})
    """
    print("func 2")


# collect tweets.

# load sub-reddits.

# get subreddit from user.


def main():
    # Allows us to use the praw (reddit) api. (REQUIRED).
    reddit = API_INSTANCE

    # Contains the command line arguments that the user passed in.
    # These arguments are stored as namespace objects.
    arg_parser = get_argument_parser_containing_program_flag_information()
    command_line_argument_parser = arg_parser.parse_args()

    if command_line_argument_parser.collect:
        print("collecting...")
    elif command_line_argument_parser.add:
        add_sub_reddit_to_db_file()
    elif command_line_argument_parser.remove:
        remove_sub_reddit_in_db_file()
    else:
        arg_parser.print_help()


if __name__ == '__main__':
    main()
