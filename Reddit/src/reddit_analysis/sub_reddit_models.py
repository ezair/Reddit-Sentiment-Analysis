"""
LATER
"""
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA


class SubRedditAnalyzer():
    """
    More on this later.
    """

    def __init__(self, mongo_reddit_collection):
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
            toks = [token.lower() for token in toks if token.lower() not in self.stop_words]
            useful_tokens.extend(toks)
        return useful_tokens

    def analyze_submission(self, submission_id):
        all_submission_comments = self.__reddit_collection.find({'submission_id': submission_id})
        print(type(all_submission_comments))
        return all_submission_comments

    def analyze_whole_subreddit(self, subreddit_name):
        pass
