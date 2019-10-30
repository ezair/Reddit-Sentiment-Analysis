"""
Author:	eric zair
File: collect.py
Description: TBA

@doxyfile
"""
import praw
import argparse
from pymongo import MongoClient
from prawcore import PrawcoreException
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
                                                       'database. ',
                                                       action='store_true')

    argument_to_execute.add_argument('--add', help='Add the sub-reddit passed '
                                                   'in by the user '
                                                   'to the list of '
                                                   'sub-reddits '
                                                   'that we will collect '
                                                   'data from.')

    argument_to_execute.add_argument('--remove', help='Remove the subreddit '
                                                      'passed in by the user.')
    return parser


def add_sub_reddit_to_db_file(parsed_command_line_arguments,
                              path_to_sub_reddit_file='sub_reddits.txt',
                              reddit=API_INSTANCE,):
    """
    Appends a sub_reddit to the end of the file that is given by the user.

    Keyword Arguments:
        path_to_sub_reddit_file {str} -- Path to a file containing the list of
                                         sub_reddits to add to.
                                         (default: {'sub_reddits.txt'})
    """
    try:
        # Check to make sure that the sub_reddit actually exists.
        reddit.subreddit(parsed_command_line_arguments.add).hot(limit=1)

        # Since it exists, we can add it to our file and parse from it later on.
        with open(path_to_sub_reddit_file, 'a') as reddit_file:
            reddit_file.write('{}\n'.format(parsed_command_line_arguments.add))
        print("i am here")
    # In the event that the subreddit does not exist, we land here.
    # We can catch the exception and not print it out (this looks better than not).
    except Exception:
        print('Unable to add sub_reddit: "{}", it does not exist.'
              .format(parsed_command_line_arguments.add))


def remove_sub_reddit_in_db_file(parsed_command_line_arguments,
                                 path_to_sub_reddit_file='sub_reddits.txt'):
    """
    Removes a sub_reddit (line in the file) to the end of the file that
    is given by the user.

    Keyword Arguments:
        path_to_sub_reddit_file {str} -- Path to a file containing the list of
                                         sub_reddits to remove from.
                                         (default: {'sub_reddits.txt'})
    """
    # We need to store the content of the file, so that we can write
    # each line back into the it (except the one line we want to remove).
    with open(path_to_sub_reddit_file, 'r') as f:
        lines_in_reddit_file = f.readlines()

    # We write every line back into the file except the one we want to
    # remove.
    with open(path_to_sub_reddit_file, 'w') as f:
        for line in lines_in_reddit_file:
            if line.strip("\n") != parsed_command_line_arguments.remove:
                f.write(line)


def get_list_of_sub_reddits(path_to_sub_reddit_file='sub_reddits.txt'):
    """
    Returns a list containing the sub_reddits that a user want to analyze
    data off of (given from the path_to_sub_reddit_file)

    Keyword Arguments:
        path_to_sub_reddit_file {str} -- Path to the file that contains
                                         the sub_reddits we want.
                                         (default: {'sub_reddits.txt'})

    Returns:
        list(str) -- list of sub_reddits that we want to analyze data on.
    """
    return [sub_reddit.strip() for sub_reddit in open(path_to_sub_reddit_file)]


def collect_data_from_sub_reddits(reddit, list_of_sub_reddits):
    sub_reddit_posts = []
    for sub_reddit in list_of_sub_reddits:
        sub_reddit_posts += reddit.subreddit(sub_reddit).hot(limit=10)
    print(sub_reddit_posts)
    ##submissions = r.get_subreddit('opensource').get_hot(limit=5)
#  >>> [str(x) for x in submissions]


def add_collected_data_to_database(data, ip_address='localhost', port=27017):
    client = MongoClient(ip_address, port)
    database = client.reddit
    subreddits = database.subreddits
    print(subreddits)


def main():
    # Contains the command line arguments that the user passed in.
    # These arguments are stored as namespace objects.
    arg_parser = get_argument_parser_containing_program_flag_information()
    command_line_argument_parser = arg_parser.parse_args()

    # Allows us to use the praw (reddit) api. (REQUIRED).
    reddit = API_INSTANCE

    # Collecting data.
    if command_line_argument_parser.collect:
        print("Collecting...")
        add_collected_data_to_database(
            collect_data_from_sub_reddits(reddit, get_list_of_sub_reddits()))

    # Adding a sub reddit.
    elif command_line_argument_parser.add:
        add_sub_reddit_to_db_file(command_line_argument_parser)

    # Remvoing a subreddit.
    elif command_line_argument_parser.remove:
        remove_sub_reddit_in_db_file(command_line_argument_parser)

    # When a user doesn't give us anything, we want to display help text.
    else:
        arg_parser.print_help()


if __name__ == '__main__':
    main()
