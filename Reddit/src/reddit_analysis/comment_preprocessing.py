"""
@Author Eric Zair
@File comment_preprocessing.py
@Description: Contains an object, RedditPreprocessor, which is used to preprocesses
              comments from reddit submission or just reddit comments given to it
              in general.

@package docstring
"""
# For data preprocessing and frequency analysis.
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer


class RedditPreprocessor():
 """Given a Mongodb database instance we are able to grab the data stored in the
    database and query comments. We can preprocess the queried for comments or just
    preprocess comments given to this object in general."""


    def __init__(self, mongo_reddit_collection, language='english'):
        """ Constructs a RedditPreprocessor object."""
        
        """Since we are analyzing english, we will use a already created (and tested)
        set of stopwords that.
        Every word in here is a word that is not worth analyzing in a given comment.
        These are the kind of words that can make or break your analysis results."""
        self.__stop_words = stopwords.words(language)
        
        """The MongDB collection that we will be pulling our reddit data from.

        The database must have the following fielding fields in it:
            body, created_at, distinguished, edited, id, is_submitter
            link_id, parent_id, replies, score, stickied, submission
            subreddit, sorting_type, sorting_type"""
        self.__reddit_collection = mongo_reddit_collection


    def get_preprocessed_comment(self, comment):
        """Return a list of preprocessed reddit comments. Comments are ready for analysis.

        Arguments:\n
            comment {str} -- The comment that we will preprocess so that it is ready to be
                             used for analysis.

        Returns:\n
            str -- The preprocessed version of the comment. Stripped to lowercase,
                   punctuation removed, each word in the comment is stemmed."""

        filtered_tokens_in_comment = []

        # We don't wanna have any punctuation in our comment.
        tokenizer = RegexpTokenizer(r'\w+')
        tokenized_comment = tokenizer.tokenize(comment)

        # We do not care about words in our stop list, they just cause issues.
        for token in tokenized_comment:
            if token.lower() not in self.__stop_words:
                filtered_tokens_in_comment.append(token)

        # Now we stem each token in the commen that we have.
        # E.g. Words like 'run' or 'running' just become their base form word 'run'
        stemmer = PorterStemmer()
        stemed_tokens = [stemmer.stem(token) for token in filtered_tokens_in_comment]

        # Now, we wanna put these tokens back into string form, so that we can easily
        # feed them into our sentiment analyzer later on.\
        stemed_tokens_to_string_form = ' '.join(stemed_tokens)
        return stemed_tokens_to_string_form


    def __get_comment_objects_for_submission(self, submission_id, number_of_comments_to_get,
                                             sorting_type=None):
        """Return a list of comment objects. The type of sorting_type given will determine the
        type of comments that we are querying for. If no sorting type is None, then we grab any
        comments from the submission.

        Arguments:\n
            submission_id {str} -- The id of the reddit submission that we are pulling comments from.
            number_of_comments_to_get {int} -- The amount of comments we pull from the submission\n

        Keyword Arguments:\n
            sorting_type {str} -- The type of comments that we are querying for.
                                  Either 'hot', 'top', or 'new'. If None is given, then we just pull
                                  any comment without using sorting type. (default: {None})

        Raises:\n
            ValueError: If the user passes something that is not 'hot', 'new', 'top', or 'None'.

        Returns:\n
            Comment -- A reddit comment object from the praw API."""
        
        if sorting_type:
            if sorting_type not in ['hot', 'new', 'top']:
                # The user might not have passed in a valid sorting type.
                raise ValueError(f'Error calling get_preprocessed_comments:, "{sorting_type}"'
                                 'is not a valid option. Valid Options: "hot", "new, and "top"')
            else:
                return self.__reddit_collection.find({'submission': submission_id,
                                                      'sorting_type': sorting_type}
                                                    ).limit(number_of_comments_to_get)

        # No sorting type given, so we can just get the query.
        return self.__reddit_collection.find({'submission': submission_id}
                                            ).limit(number_of_comments_to_get)


    def get_preprocessed_comments(self, submission_id, number_of_comments_to_get,
                                  sorting_type=None):
        """Return a list of preprocessed comments, each comment is a str.

        Arguments:\n
            submission_id {str} -- The id of the submission that we are grabbing comments for.
            number_of_comments_to_get {int} -- The amount of comments that we are going to grab.

        Keyword Arguments:\n
            sorting_type {str} -- The type of comments that we want to grab.
                                Must be 'new', 'top', 'hot'. If None is given, we grab any type
                                of comment. (default: {None})

        Returns:\n
        list -- A list of preprocessed comments. Each comment in the list is a str."""

        # Varying on the sorting type that is passed in, we will query on it.
        # if no sorting type is given, then we just grab all posts for the submission.
        submission_comment_objects =\
            self.__get_comment_objects_for_submission(submission_id, number_of_comments_to_get,
                                                      sorting_type=sorting_type)

        # We need the comments in the form of strings, otherwise we cannot preprocess them/
        # prep them for analysis.
        submission_comments_as_strings =\
            [comment['body'] for comment in submission_comment_objects]

        # We have now cleaned up each individual comment in the given list, now they are ready
        # to be analyzed later.
        preprocessed_comments_for_submission =\
            [self.get_preprocessed_comment(comment) for comment in submission_comments_as_strings]

        return preprocessed_comments_for_submission


    def add_words_to_stop_word_list(self, list_of_words_to_add):
        """Append each element in a given list of words to our list of stop_words.
           Each appended word is AUTOMATICALLY converted to lowercase.

        Arguments:\n
            list_of_words_to_add {list} -- A list of words to append to our stop_words list.

        Raises:\n
            ValueError: An element of the given list is not of type string."""

        # Again... we really wanna make sure we add the correct things to the list.
        for word in list_of_words_to_add:
            if type(word) != str:
                raise ValueError(f"Error in add_words_to_stop_list: {word} is not of type str")
            # Words that we add need to be lowercase, just like our in our stop words list.
            self.__stop_words.append(word.lower())

        # It was a list of strings, we are all good.
        self.__stop_words += list_of_words_to_add
