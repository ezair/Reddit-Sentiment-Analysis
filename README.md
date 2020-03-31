# PROJECT INFORMATION

- @author Eric Zair
- @updated 03/17/2020
- @brief Program that uses the `praw` API and `mongod` API in order to grab information from reddit and add it to a mongodb database. From there the user can then create any models or programs they want that are built around the `reddit_collector.py` program.

## Project Goal

There are two different goals for this project.

The first part is the `reddit_collector.py` program which is used to grab data from given subreddits and add the data to a mongodb database.

The second part of the project is to take the data that is in the mongodb database and analyze it via natural language processing.

I will be creating my own NLP "model" for analyzing reddit data from the database, however, the beauty of this project is that users can create their own models and use the `reddit_collector.py` script to grab the data that they wanna find. All they have to do is slightly tweak. The program is setup so that you can use your own database with it, so it is quite easy, just swap your database and auth keys and you should have no problems.

## reddit_collector

This is program is used to grab data off of reddit.

More specifically, given a `.sub` file containing multiple different subreddits, we grab N amount of comments on K amount of posts.

This program has a flag for adding a subreddit to the `.sub` file, removing a flag from the `.sub` file, and also collecting the data based of the subreddits in the `.sub` file.

*Program Usage Information:*

```ignore
usage: reddit_post_collector.py [-h] [--collect | --add ADD | --remove REMOVE]

optional arguments:
  -h, --help       show this help message and exit
  --collect        Prompt the user for a data range and being collecting the
                   data. When we are done with collecting, we add the data to
                   the database.
  --add ADD        Add the sub-reddit passed in by the user to the list of
                   sub-reddits that we will collect data from.
  --remove REMOVE  Remove the subreddit passed in by the user.
```

The best way to run the `reddit_post_collector.py` program is actually through the `reddit_post_collector.sh` bash script, as all the paths are accurate and such.

*Example run of the program for collecting data:*
`./reddit_collector.sh --collect`

*Example run of the program for adding a subreddit to the `.sub` list:*
`./reddit_collector.sh --add <name_of_subreddit_to_add>`

*Example run of the program for removing a subreddit from the `.sub` list:*
`./reddit_collector.sh --remove <name_of_subreddit_to_remove>`

## Models

More on this later.

## Credentials

*IMPORTANT:* There are *TWO* different `python3` files that are required in order for this project to work. These files *MUST* be created by the user. These two files are in the `.gitignore` file because they contain information that you don not want to be publicly known to anyone but you, the user.

The code for both files is available below, all you have to do is copy the content and make the files in the `src/credentials/` folder.

These files contains required global variables that will be imported directly into our `python3` files e.g. in `collector.py`.I figured that this is the neatest way to handle secret credentials while still being able to have a lot of flexibility in these programs.

## mongo_credentials.py

The first file that we need to make is called `mongo_credentials.py` and must be created in the `src/credentials/` folder.

The only things that need to be changed in this file is the `client_id` and the `client_secret`. Everything else in the entire file can remain exactly as is.

```python
API_INSTANCE = get_api_instance(client_id='YOUR CLIENT ID',
                                client_secret='YOUR SECRET KEY',
                                user_agent='my user agent')
```

```python
"""
Author: Eric Zair
File: reddit_credentials.py
Description: This file contains the api_instance needed to use
             the reddit api(praw). This will be imported in by
             the user.
"""
import praw


def get_api_instance(client_id, client_secret, user_agent):
    """
    :Desc:  Method sets up connecting to the reddit api for the user.
            The purpose of this method is to be called into the main program,
            so that the praw instance will have been connected.
    :param client_id: This is the user's praw client ID.
    :type: str
    :param client_secret: User's client secret for the praw API.
    :type: str
    :param user_agent: This is the user's praw user_agent. (This can be what ever).
    :return: praw.Reddit
    """
    return praw.Reddit(client_id=client_id,
                       client_secret=client_secret,
                       user_agent=user_agent)


def test(api_instance):
    """
    :Desc: Very simple test to see that the reddit api is working normally.
    :param: api_instance: Instance that you are returning.
    :type: praw.Reddit()
    :return:    None
    """
    for submission in api_instance.subreddit("soccer").hot(limit=11):
        print(submission.title)
        print("IT WORKS, The test works.")


# Variable that the user must import into their program,
# in order for the reddit
# api to work correctly. This is an api instance.

# Change the client_id field and the cliend_secret.
API_INSTANCE = get_api_instance(client_id='YOUR CLIENT ID',
                                client_secret='YOUR SECRET KEY',
                                user_agent='my user agent')

"""
Variable in the reddit_crenentials.py, If run_test == True, the test runs, False.
"""
RUN_TEST = False
if RUN_TEST:
    test(API_INSTANCE)
```

### reddit_credentials.py

The next file that we must have created is called `reddit_credentials.py` and must be created in the `src/credentials/` folder.

All you have to do is change the variable `mongo_auth_token` to your mongodb authorization token for your database.

If you would like to (but this is more up to how you wanna customize your database) you can change the name of your database for `DB_COLLECTION`.

*Content of reddit_credentials.py*:

```python
"""
Author: Eric Zair
File: mongo_credentials.py
Description: This file all of the setup done for the user's database.
             We set it up completely, and then just return the instance
             of the database to our collector program when it is needed.

            NOTE:
                (This is done so that we KNOW the user's database will work
                fluently within out reddit_collector.py file.)
"""
from pymongo import MongoClient


# We setup the database so that it can be directly imported into the programs
# that it will be needed in.
# This is very nice because no matter how the user sets up their program,
# our main program (reddit_post_collector) can handle it all the same.
try:
    # My current auth token is python3.4 or higher.
    mongo_auth_token = 'YOUR MONGO AUTH TOKEN GOES HERE!'
    client = MongoClient(mongo_auth_token)
    db = client.get_database('reddit')

    # This collection is what will be imported directly into the
    # reddit_post_collector.py file.
    DB_COLLECTION = db['post_comment']

except Exception:
    print('Error, either you database:\n'
          '\t1. Does not exist\n'
          '\t2. Has not properly been setup or\n'
          '\t3. The incorrect token has been given.')
```
