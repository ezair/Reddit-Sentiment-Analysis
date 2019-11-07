"""
@Author Eric Zair
@File collect.py
@Description: This program uses the praw (reddit api) to parse data from
              given sub-reddits. These sub-reddits are located in a file
              called "sub_reddits.txt" and the user can add and remove
              sub_reddits to the program via the program flags.

@package docstring
"""
import argparse
from credentials.reddit_credentials import API_INSTANCE
from credentials.mongo_credentials import db_collection


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

    Arguments:
        parsed_command_line_arguments {namespace} -- Namespace object that
                                                     contains the values of
                                                     each given command line
                                                     argument that is passed
                                                     into the program.

    Keyword Arguments:
        path_to_sub_reddit_file {str} -- Path to a file containing the list of
                                         sub_reddits to add to.
                                         (default: {'sub_reddits.txt'})
    """
    try:
        # Check to make sure that the sub_reddit actually exists.
        reddit.subreddit(parsed_command_line_arguments.add).hot(limit=1)

        # Since it exists, we can add it to our file and parse from it later.
        with open(path_to_sub_reddit_file, 'a') as reddit_file:
            reddit_file.write('{}\n'.format(parsed_command_line_arguments.add))
        print("i am here")
    # In the event that the subreddit does not exist, we land here.
    # We can catch the exception and not print it out.
    except Exception:
        print('Unable to add sub_reddit: "{}", it does not exist.'
              .format(parsed_command_line_arguments.add))


def remove_sub_reddit_in_db_file(parsed_command_line_arguments,
                                 path_to_sub_reddit_file='sub_reddits.txt'):
    """
    Removes a sub_reddit (line in the file) to the end of the file that
    is given by the user.

    Arguments:
        parsed_command_line_arguments {namespace} -- Namespace object that
                                                     contains the values of
                                                     each given command line
                                                     argument that is passed
                                                     into the program.

    Keyword Arguments:
        path_to_sub_reddit_file {str} -- Path to a file containing the list of
                                         sub_reddits to remove from.
                                         (default: {'sub_reddits.txt'})
    """
    # We need to store the content of the file, so that we can write
    # each line back into the it (except the one line we want to remove).
    with open(path_to_sub_reddit_file, 'r') as reddit_file:
        lines_in_reddit_file = reddit_file.readlines()

    # We write every line back into the file except the one we want to
    # remove.
    with open(path_to_sub_reddit_file, 'w') as reddit_file:
        for line in lines_in_reddit_file:
            if line.strip("\n") != parsed_command_line_arguments.remove:
                reddit_file.write(line)


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


def get_collected_data_from_sub_reddits(list_of_sub_reddits,
                                        reddit_api=API_INSTANCE):
    """
    Given a list of sub-reddits from the user, we add all the comments
    made by reddit users to a list and then return it.

    Arguments:
        list_of_sub_reddits {list(str)} -- Contains the names of all the
                                           sub-reddits that a user wants
                                           to parse comments from.

    Keyword Arguments:
        reddit_api {Reddit} -- API_INSTANCE required to use the program
                               (default: {API_INSTANCE})

    Returns:
        [type] -- [description]
    """
    # Cool, we can now load up submissions from the sub-reddits that the
    # wants to collect data from.
    sub_reddit_posts = []
    for sub_reddit in list_of_sub_reddits:
        sub_reddit_posts += reddit_api.subreddit(sub_reddit).hot(limit=5)

    # Awesome, time to grab all of the comments, because we will later
    # want to add them into a mongo db_database.
    reddit_comments_from_given_sub_reddits = []
    for reddit_submission in sub_reddit_posts:
        for comment in reddit_submission.comments:
            reddit_comments_from_given_sub_reddits.append(comment)
    return reddit_comments_from_given_sub_reddits


def add_collected_data_to_database(reddit_post_comments,
                                   ip_address='localhost',
                                   port=27017):
    for post_comment in reddit_post_comments:
        # These are the fields that we want the reddit_comments in the
        # database to have.
        post_comment_data = {
            'author': post_comment.author,
            'body': post_comment.body,
            'created_at': post_comment.created_utc,
            'distinguished': post_comment.distinguished,
            'edited': post_comment.edited,
            'id': post_comment.id,
            'is_submitter': post_comment.is_submitter,
            'link_id': post_comment.link_id,
            'parent_id': post_comment.parent_id,
            'replies': post_comment.replies,
            'score': post_comment.score,
            'stickied': post_comment.stickied,
            'submission': post_comment.submission,
            'subreddit': post_comment.subreddit,
            'subreddit_id': post_comment.subreddit_id
        }
        db_collection.insert_one(dict(post_comment_data))
    # db_collection.close()

def main():
    # Contains the command line arguments that the user passed in.
    # These arguments are stored as namespace objects.
    arg_parser = get_argument_parser_containing_program_flag_information()
    command_line_argument_parser = arg_parser.parse_args()

    # Collecting data.
    if command_line_argument_parser.collect:
        print("Collecting data...")
        add_collected_data_to_database(
            get_collected_data_from_sub_reddits(get_list_of_sub_reddits()))

    # Adding a sub reddit.
    elif command_line_argument_parser.add:
        add_sub_reddit_to_db_file(command_line_argument_parser)

    # Removing a subreddit.
    elif command_line_argument_parser.remove:
        remove_sub_reddit_in_db_file(command_line_argument_parser)

    # When a user doesn't give us anything, we want to display help text.
    else:
        arg_parser.print_help()


if __name__ == '__main__':
    main()
