"""
LATER
"""
import datetime

# For data preprocessing and frequency analysis.
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer

# Catching possible mongo errors.
from pymongo.errors import CursorNotFound

# For analysis/gathering sentiment analysis results.
# https://www.kaggle.com/kamote/exploring-toxic-comments-by-sentiment-analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SubRedditAnalyzer():
    """
    More on this later.
    """

    def __init__(self, mongo_reddit_collection):
        """
        The MongDB collection that we will be pulling our reddit data Inside of.

        The database must have the following fielding fields in it:
            body, created_at, distinguished, edited, id, is_submitter
            link_id, parent_id, replies, score, stickied, submission
            subreddit, sorting_type': sorting_type
        """
        self.__reddit_collection = mongo_reddit_collection

        """
        Since we are analyzing english, we will use a already created (and tested)
        set of stopwords that.
        Every word in here is a word that is not worth analyzing in a given comment.
        These are the kind of words that can make or break your analysis results.
        """
        self.__stop_words = stopwords.words('english')

        """
        This is an out of the box Sentiment Analyzer model that is exceptionally good
        at analyzing social media data. We will feed individual comments to it and it will
        give us a score of polarity (positivity, negativity, neutral, and Compound). 
        """
        self.__comment_sentiment_analyzer = SentimentIntensityAnalyzer()

        # Make sure that the passed in database has all of the following fields.
        # It NEEDS to fit the form of our comment model, or we cannot analyze it.
        # TODO

    def __preprocess_comment(self, comment):
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


    def __get_comment_objects_for_submission(self, submission_id, sorting_type=None,
                                             number_of_comments_to_get=0):
        if sorting_type:
            if sorting_type not in ['hot', 'new', 'top']:
                # The user might not have passed in a valid sorting type.
                raise ValueError('Error calling analyze_submission:, "{}" is not a valid option.'
                                 'Valid Options: "hot", "new, and "top"'.format(sorting_type))
            else:
                return self.__reddit_collection.find({'submission': submission_id,
                                                      'sorting_type': sorting_type},
                                                     limit=number_of_comments_to_get)

        # No sorting type given, so we can just get the query.
        return self.__reddit_collection.find({'submission': submission_id})


    def __get_preprocessed_comments_as_strings(self, submission_id, sorting_type=None,
                                               max_number_of_comments_to_analyze=0):
         # Varying on the sorting type that is passed in, we will query on it.
        # if no sorting type is given, then we just grab all posts for the submission.
        submission_comment_objects =\
            self.__get_comment_objects_for_submission(submission_id,
                                                      sorting_type,
                                                      max_number_of_comments_to_analyze)

        # We need the comments in the form of strings, otherwise we cannot preprocess them/
        # prep them for analysis.
        submission_comments_as_strings =\
            [comment['body'] for comment in submission_comment_objects]

        # We have now cleaned up each individual comment in the given list, now they are ready
        # to be analyzed later.
        preprocessed_comments_for_submission =\
            [self.__preprocess_comment(comment) for comment in submission_comments_as_strings]

        return preprocessed_comments_for_submission


    def analyze_submission(self, submission_id, sorting_type=None,
                           display_all_comment_results=False,
                           max_number_of_comments_to_analyze=0):

        # We have now cleaned up each individual comment in the given list, ready to analyze them.
        list_of_preprocessed_comments_for_submission =\
            self.__get_preprocessed_comments_as_strings(submission_id,
                                                        sorting_type=sorting_type,
                                                        max_number_of_comments_to_analyze=\
                                                            max_number_of_comments_to_analyze)

        # Used to sum up and get averages for positive and negative comments.
        positive_comment_results = []
        negative_comment_results = []

        for comment in list_of_preprocessed_comments_for_submission:
            analysis_results_of_comment = \
                self.__comment_sentiment_analyzer.polarity_scores(comment)

            # Comment might not be positive or negative, so by default it is ignored.
            # It will be set later.
            classification_to_print_out = "Ignored"

            # Concluded comment is positive.
            if(
                analysis_results_of_comment['compound'] >= 0.05 or \
                analysis_results_of_comment['neg'] == 0 and analysis_results_of_comment['pos'] > 0
            ):
                positive_comment_results.append(analysis_results_of_comment['compound'])
                classification_to_print_out = "Positive"

            # Concluded comment is negative.
            elif(
                analysis_results_of_comment['compound'] <= -0.05 or \
                analysis_results_of_comment['pos'] == 0 and analysis_results_of_comment['neg'] > 0
            ):
                # We have a negative comment.
                negative_comment_results.append(abs(analysis_results_of_comment['compound']))
                classification_to_print_out = "Negative"

            # The user wants us to show the scoring for all comments that we are analyzing.
            if display_all_comment_results:
                try:
                    subreddit_name =\
                        self.__reddit_collection.find_one(
                            {'submission': submission_id})['subreddit_name']
                except CursorNotFound:
                    # Might not have a subreddit_name as a field for this one, so
                    # we default it if not found.
                    subreddit_name = "NONE"

                print("\nSubreddit Name:", subreddit_name)
                print("Comment:", comment)
                print("Positivity Rating:", analysis_results_of_comment['pos'])
                print("Negativity Results:", analysis_results_of_comment['neg'])
                print("Neutral results: {}\n".format(analysis_results_of_comment['neu']))
                print("Classification: {}".format(classification_to_print_out))

        number_of_results = len(negative_comment_results) + len(positive_comment_results)

        if number_of_results == 0:
            return {'positive': 0, 'negative': 0}

        average_positivity = sum(positive_comment_results) / number_of_results
        average_negativity = sum(negative_comment_results) / number_of_results

        # They also wanna see the final results of scoring (even tho they are returned).
        if display_all_comment_results:
            print('\nResults of all comments for submission: "{}"'.format(submission_id))
            print("Average positivity: {}".format(average_positivity))
            print("Average negativity: {}\n".format(average_negativity))

        return {'positive': average_positivity, 'negative': average_negativity}


    def analyze_subreddit(self, subreddit_name, sorting_type=None,
                          display_all_comment_results=False,
                          display_all_submission_results=False,
                          max_number_of_comments_to_analyze=None,
                          max_number_of_submissions_to_analyze=0):
        start_time = datetime.datetime.now()

        # Every single subreddit submission record (with given sorting type).
        all_sub_reddit_submissions =\
            self.__reddit_collection.find({'subreddit_name': subreddit_name})

        average_results_for_sub_reddit = {'positive': 0, 'negative': 0}

        # We need to keep track of this
        number_of_submissions_in_sub_reddit = 0
        for submission in all_sub_reddit_submissions:
            # Dict with all averages of a submission in given subreddit.
            analysis_results_of_submission = \
                self.analyze_submission(submission['submission'], sorting_type=sorting_type,
                                        display_all_comment_results=display_all_comment_results)
            
            # TODO
            # Do same thing that was done with submission analysis where we only
            # except certain scores. Some submissions are not positive and sum are not negative.
            # Make a private method that is general and takes 2 lists and appends to the one that
            # fits.
            average_results_for_sub_reddit['positive'] += \
                analysis_results_of_submission['positive']

            # These values are negative, need to take abs.
            average_results_for_sub_reddit['negative'] += \
                analysis_results_of_submission['negative']

            # They want to see the rating for each submission post.
            if display_all_submission_results:
                print("{}: ".format(subreddit_name))
                print('Positivity Rating: {}'.format(average_results_for_sub_reddit['positive']))
                print('Negativity Rating: {}\n'.format(average_results_for_sub_reddit['negative']))

        # There might be zero submissions; avoid dividing by zero :)
        if all_sub_reddit_submissions.retrieved > 0:
            average_results_for_sub_reddit['positive'] /= all_sub_reddit_submissions.retrieved
            average_results_for_sub_reddit['negative'] /= all_sub_reddit_submissions.retrieved

        # They wanna show the averages in the method.
        if display_all_submission_results:
            print('\nResults of all comments for submission: "{}"'.format(subreddit_name))
            print("Average positivity: {}".format(average_results_for_sub_reddit['positive']))
            print("Average negativity: {}".format(average_results_for_sub_reddit['negative']))
            print("Total time:", str(datetime.datetime.now() - start_time))

        return average_results_for_sub_reddit


    # Later, once I implement word bubble and freq analysis.
    def show_hotest_submission_topics(self, submission_id):
        pass


    # Later, once I implement word bubble and freq analysis.
    def show_hotest_sub_reddit_topics(self, subreddit_id):
        pass
