"""
LATER
"""
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


class SubRedditAnalyzer():
    """
    More on this later.
    """

    def __init__(self, mongo_reddit_collection):
        # This needs to be done, so that we can actually grab data from nltk.

        """ The MongDB collection that we will be pulling our reddit data from."""
        self.__reddit_collection = mongo_reddit_collection

        """
        Since we are analyzing english, we will use a already created (and tested)
        set of stopwords that.
        Every word in here is a word that is not worth analyzing in a given comment.
        These are the kind of words that can make or break your analysis results.
        """
        self.__stop_words = stopwords.words('english')

    def __process_comment(self, list_of_comments):
        useful_tokens = []
        for comment in list_of_comments:
            tokenizer = RegexpTokenizer(r'\w+')
            toks = tokenizer.tokenize(comment)
            toks = [token.lower() for token in toks if token.lower() not in self.__stop_words]
            useful_tokens.extend(toks)
        return useful_tokens

    def analyze_submission(self, submission_id_as_string, show_statistics=False,
                           show_most_frequent_words=False):
        all_submission_comment_objects = \
            self.__reddit_collection.find({'submission': submission_id_as_string})

        # We need to get the actual text from our commend objects, since that is
        # what is going to be analyzed.
        all_comments_on_submission_as_strings = \
            [comment['body'] for comment in all_submission_comment_objects]

        # Okay, we have now cleaned up each individual comment in the given list,
        # so they are ready to be analysed.
        all_processed_comments = self.__process_comment(all_comments_on_submission_as_strings)
        for comment in all_processed_comments:
            print(comment)

        # Now, let's find out what is "positive" and what is "negative".
        # We can get an overall rating of "goodness" and "badness" based off of this.

        if statistics:
            pass

    def analyze_whole_subreddit(self, subreddit_name):
        pass
