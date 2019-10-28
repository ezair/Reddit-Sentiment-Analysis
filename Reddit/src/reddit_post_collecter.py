"""
Author:	eric zair
File: collect.py
Description: TBA
"""
import argparse
import praw
from credentials.reddit_credentials import API_INSTANCE


# Handle argparsing.
def get_argument_parser_containing_program_flag_information():
    parser = argparse.ArgumentParser()

    # Simply displays the program useage :)
    parser.add_argument('--help', help='Display program usage.',
                        action='store_true')

    # When called, it executes a function that allows the user to
    # enter the sub_reddit that they want to pull data off of and
    # store into the database.
    parser.add_argument('--add', help='Prompt the user to enter a '
                                      ' sub_reddit that they would '
                                      'like to grab data from.',
                        action='store_true',
                        func=prompt_user_for_sub_reddit_to_enter)


# add to database.

# prompt user for subreddit to enter.
def prompt_user_for_sub_reddit_to_enter():
    pass

# collect tweets.

# load sub-reddits.

# get subreddit from user.


def main():
    # Allows us to use the praw (reddit) api. (REQUIRED)
    reddit = API_INSTANCE

    # First this is first, we wanna find out if:
    #   1. The user wants to add more sub-reddits to the list of sub-reddits
    #       to parse and grab data from
    #   or
    #   2.  The user wants to continue mining/collecting the data and adding it to the database.


if __name__ == '__main__':
    main()
