"""
@Author Eric Zair
@File collect.py
@Description: This program uses the praw (reddit api) to parse data from
              given sub-reddits. These sub-reddits are located in a file
              called "sub_reddits.txt" and the user can add and remove
              sub_reddits to the program via the program flags.

@package docstring
"""
# Do we wanna add, remove, or collect?
# Also for displaying help text.
import argparse

# These are needed for parsing to figure out if a sub_reddit exists.
import re
import requests
from bs4 import BeautifulSoup

# This is from our credentials lib (not an external lib).
from credentials.reddit_credentials import API_INSTANCE
from credentials.mongo_credentials import DB_COLLECTION


"""
Default location that program searches for our sub reddit list.
Change this variable if you want run program on a different sub_reddit_list.
"""
SUB_REDDIT_LIST = "sub_reddit_list.sub"


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
                                                       'a data range and being '
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


def add_sub_reddit_to_sub_file(parsed_command_line_arguments,
                              path_to_sub_reddit_file=SUB_REDDIT_LIST,
                              reddit=API_INSTANCE):
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
                                         (default: {SUB_REDDIT_LIST})
    """

    try:
        reddit.subreddit(parsed_command_line_arguments.add).hot(limit=1)

        # We only want to add a subreddit to the list one time,
        # so we do not want to allow duplicates. It will ruin our data.
        with open(path_to_sub_reddit_file, 'r') as reddit_file:
            for line in reddit_file:
                if line.strip() == parsed_command_line_arguments.add:
                    return None

        with open(path_to_sub_reddit_file, 'a') as reddit_file:
            reddit_file.write('{}\n'.format(parsed_command_line_arguments.add))

    # The given subreddit does not exist.
    except prawcore.NotFound:
        print('Unable to add sub_reddit: "{}", it does not exist.'
              .format(parsed_command_line_arguments.add))


def remove_sub_reddit_in_db_file(parsed_command_line_arguments,
                                 path_to_sub_reddit_file=SUB_REDDIT_LIST):
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
                                         (default: {SUB_REDDIT_LIST})
    """

    # We need to store the content of the file, so that we can write
    # each line back into it (except the one line we want to remove).
    with open(path_to_sub_reddit_file, 'r') as reddit_file:
        lines_in_reddit_file = reddit_file.readlines()

    # We write every line back into the file except the one we want to
    # remove.
    with open(path_to_sub_reddit_file, 'w') as reddit_file:
        for line in lines_in_reddit_file:
            if line.strip("\n") != parsed_command_line_arguments.remove:
                reddit_file.write(line)


def get_list_of_sub_reddits(path_to_sub_reddit_file=SUB_REDDIT_LIST):
    """
    Returns a list containing the sub_reddits that a user want to analyze
    data off of (given from the path_to_sub_reddit_file)

    Keyword Arguments:
        path_to_sub_reddit_file {str} -- Path to the file that contains
                                         the sub_reddits we want.
                                         (default: {SUB_REDDIT_LIST})

    Returns:
        {list(str)} -- list of sub_reddits that we want to analyze data on.
    """

    return [sub_reddit.strip() for sub_reddit in open(path_to_sub_reddit_file)]


def sub_reddit_exists(sub_reddit_name):
    """
    Determines whether a given subreddit exists.
    
    Arguments:
        sub_reddit_name {str} -- The subreddit that we wanna find out exists or not.
    
    Returns:
        bool -- True if subreddit exists, False otherwise.
    """
    
    # The praw API Has NO way way of knowing if a subreddit exists or not.
    # I have tried insane amount of documentation on this.
    # Long story short, I ended up deciding that parsing subreddit's webpage
    # e.g. "reddit.com/r/<name_of_sub_reddit>/" and looking for the <h3> tag
    # that shows up when no content exists on a reddit page, was the best way
    # to determine that the subreddit does not exist.
    sub_reddit_url = 'https://www.reddit.com/r/{}/'.format(sub_reddit_name)
    sub_reddit_web_page = requests.get(url=sub_reddit_url)
    header_tag_parser = BeautifulSoup(sub_reddit_web_page.text, features="html.parser")
    list_of_h3_tags_in_sub_reddit_page = header_tag_parser.find_all(re.compile('^h[3]$'))

    # This is the message that is displayed when no content is on a reddit page and the
    # community does not exist.
    # I will use this and compare it against each <h3> tag on the webpage that is pulled down.
    # If it is found to be in the list, then we know that the subreddit does not exist.
    string_indicating_sub_reddit_does_not_exist = '<h3 class="_2XKLlvmuqdor3RvVbYZfgz">'\
                                                  'Sorry, there aren’t any communities on '\
                                                  'Reddit with that name.</h3>'
    for bs4_tag_object in list_of_h3_tags_in_sub_reddit_page:
        if str(bs4_tag_object) == string_indicating_sub_reddit_does_not_exist:
            return False
    return True


def get_collected_data_from_sub_reddits(list_of_sub_reddits, sorted_by,
                                        reddit_api=API_INSTANCE, number_of_posts=5):
    """
    Given a list of sub-reddits from the user, we add all the comments
    made by reddit users to a list and then return it.

    Arguments:
        list_of_sub_reddits {list(str)} -- Contains the names of all the
                                           sub-reddits that a user wants
                                           to parse comments from.

        sorted_by {str} -- String that is either 'hot', 'new', or 'top'.
                           Varying on which one is passed in, we will
                           grab data from it's category.
                           E.g. if the string is 'hot', then we will
                           grab post data from the hot category.

    Keyword Arguments:
        reddit_api {Reddit} -- API_INSTANCE required to use the program
                               (default: {API_INSTANCE})

    Returns:
        {list(str)} -- List containing all comments from our the subreddits
                       that the user has in their sub reddit file.
    """

    # Cool, we can now load up submissions from the sub-reddits that the
    # wants to collect data from.
    sub_reddit_submissions = []
    for sub_reddit in list_of_sub_reddits:
        if sub_reddit_exists(sub_reddit):
            if sorted_by == 'hot': 
                sub_reddit_submissions += reddit_api.subreddit(sub_reddit).hot(limit=number_of_posts)
            elif sorted_by == 'top':
                sub_reddit_submissions += reddit_api.subreddit(sub_reddit).top(limit=number_of_posts)
            elif sorted_by == 'new':
                sub_reddit_submissions += reddit_api.subreddit(sub_reddit).new(limit=number_of_posts)
        else:
            print('Error: The subreddit "{}" does not exist. Skipping over it...\n'
                  .format(sub_reddit))

    # Awesome, time to grab all of the comment objects, because we will later
    # want to add them into a mongo db_database.
    reddit_comments_from_given_sub_reddits = [
        comment
        for reddit_submission in sub_reddit_submissions
        for comment in reddit_submission.comments
    ]
    return reddit_comments_from_given_sub_reddits


def add_collected_data_to_database(reddit_submission_comments,
                                   db_collection=DB_COLLECTION):
    """
    Put every reddit comment contained in "reddit_submission_comments" into
    the given mongo db database collection.

    Arguments:
        reddit_submission_comments {list} -- Contains reddit_comments for a
                                            particular post stored in strings.

    Keyword Arguments:
        db_collection {mongoDB Database} -- The database that we are putting
                                            all of the reddit comments in.
                                            (default: {DB_COLLECTION})
    """

    for submission_comment in reddit_submission_comments:
        # These are the fields that we want the reddit_comments in the
        # database to have.
        print("POST__________________________________________________\n")
        print("Author:", submission_comment.author)
        print("Comment Body:", submission_comment.body)
        print("Created at:", submission_comment.created_utc)
        # print(submission_comment.distinguished)
        print("Edited:", submission_comment.edited)
        print("Comment id:", submission_comment.id)
        print(submission_comment.is_submitter)
        print("Link ID:", submission_comment.link_id)
        print("Comments from previous submission:",
              submission_comment.parent_id)
        for x in submission_comment.replies:
            print(x)
        print("Rating:", submission_comment.score)
        print(submission_comment.stickied)
        print("submission:", submission_comment.submission)
        print("Subreddit:", submission_comment.subreddit)
        print(submission_comment.subreddit_id)
        print("\n")
        exit()
    #     submission_comment_data = {
    #         'author': submission_comment.author,
    #         'body': submission_comment.body,
    #         'created_at': submission_comment.created_utc,
    #         'distinguished': submission_comment.distinguished,
    #         'edited': str(submission_comment.edited),
    #         '_id': str(submission_comment.id),
    #         'is_submitter': submission_comment.is_submitter,
    #         'link_id': str(submission_comment.link_id),
    #         'parent_id': str(submission_comment.parent_id),
    #         # 'replies': submission_comment.replies,
    #         'score': submission_comment.score,
    #         'stickied': submission_comment.stickied,
    #         'submission': str(submission_comment.submission),
    #         'subreddit': str(submission_comment.subreddit),
    #         'subreddit_id': str(submission_comment.subreddit_id)
    #     }
    #     db_collection.insert_one(submission_comment_data)

    db_collection.close()


def get_post_sorting_type_from_user():
    """
    Prompt the user to decide the sorting method that they will want to use to collect posts
    The options are Hot posts, New posts, and Top posts
    
    Returns:
        str -- string containing either 'hot', 'new', or 'top'
    """

    # post_sort_option will contain an integer value that we will use to figure out
    # how the user wants to sort their posts.
    # Varying on this integer value, we will pass in a different string to the
    # get_collected_data_from_sub_reddits() method for the sorted_by parameter.
    post_sort_option = 0
    while post_sort_option < 1 or post_sort_option > 3:
        try:
            post_sort_option = int(input("What type of posts would you like to grab?\n"
                                         "(1) Hot posts\n"
                                         "(2) New posts\n"
                                         "(3) Top posts\n"
                                         "Enter: "))
        except ValueError:
            print("\nError, that is not an integer, please try again!\n")

    if post_sort_option == 1:
        return 'hot'
    elif post_sort_option == 2:
        return 'new'
    else:
        return 'top'


def main():
    # Argparse is used to grab the command line arguments that the user passed in.
    # Now that we have them, we can determine what they actually wanted to do
    # and if something invalid is given, we can throw a help message for it :)
    arg_parser = get_argument_parser_containing_program_flag_information()
    command_line_argument_parser = arg_parser.parse_args()

    # Collect data.
    if command_line_argument_parser.collect:
        # This is either 'new', 'hot', or 'top'.
        post_sorting_type = get_post_sorting_type_from_user()
        
        print("Collecting data...")
        collected_data_from_sub_reddits = get_collected_data_from_sub_reddits(
                                                     get_list_of_sub_reddits(),
                                                     post_sorting_type)
        # And now it's in MongoDB :)
        add_collected_data_to_database(collected_data_from_sub_reddits)

    # Add a subreddit to our subreddit (.sub) file.
    elif command_line_argument_parser.add:
        print('"{}" has been added to list of sub_reddits'
              .format(command_line_argument_parser.add))
        
        add_sub_reddit_to_sub_file(command_line_argument_parser)

    # Remove a subreddit from our subreddit (.sub) file.
    elif command_line_argument_parser.remove:
        remove_sub_reddit_in_db_file(command_line_argument_parser)

    else:
        arg_parser.print_help()


if __name__ == '__main__':
    main()
