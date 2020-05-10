"""
LATER
"""
import datetime

# Catching possible mongo errors.
from pymongo.errors import CursorNotFound

# My comment preprocessor object, specifically used for reddit comments.
from .comment_preprocessing import RedditPreprocessor

# For analysis/gathering sentiment analysis results.
# https://www.kaggle.com/kamote/exploring-toxic-comments-by-sentiment-analysis
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SubRedditAnalyzer():
    """
    More on this later.
    """

    def __init__(self, mongo_reddit_collection):
        """
        The MongDB collection that we will be pulling our reddit data from.

        The database must have the following fielding fields in it:
            body, created_at, distinguished, edited, id, is_submitter
            link_id, parent_id, replies, score, stickied, submission
            subreddit, sorting_type': sorting_type
        """
        self.__reddit_collection = mongo_reddit_collection

        """
        This is an out of the box Sentiment Analyzer model that is exceptionally good
        at analyzing social media data. We will feed individual comments to it and it will
        give us a score of polarity (positivity, negativity, neutral, and Compound). 
        """
        self.__comment_sentiment_analyzer = SentimentIntensityAnalyzer()

        # Make sure that the passed in database has all of the following fields.
        # It NEEDS to fit the form of our comment model, or we cannot analyze it.
        # TODO
        
        """
        RedditPreprocessor that is used for preprocessing all of the comments that we will be
        analyzing. This object can later be configured by the user, in the event that they want
        edit their stop_word list, or change it's language.
        """
        self.__comment_preprocessor = RedditPreprocessor(self.__reddit_collection)


    def analyze_submission(self, submission_id, sorting_type=None,
                           display_all_comment_results=False,
                           max_number_of_comments_to_analyze=0):
        
        preprocessed_submission_comments =\
            self.__comment_preprocessor.get_preprocessed_comments(submission_id,
                                                                  max_number_of_comments_to_analyze,
                                                                  sorting_type=sorting_type)

        # Used to sum up and get averages for positive and negative comments.
        positive_comment_results = []
        negative_comment_results = []

        for comment in preprocessed_submission_comments:
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

                # Now we can actually...show the results the user wants to see.
                print("\nSubreddit Name:", subreddit_name)
                print("Comment:", comment)
                print(f"Positivity Rating: {analysis_results_of_comment['pos']}")
                print(f"Negativity Results: {analysis_results_of_comment['neg']}")
                print(f"Neutral results: {analysis_results_of_comment['neu']}")
                print("Classification:", classification_to_print_out)

        # Need this to later get percentages of negativity and positivity (math stuffs).
        total_sum_of_result_scores = sum(positive_comment_results + negative_comment_results)

        # This implies we have not analyzed anthing.
        if total_sum_of_result_scores == 0:
            return {'positive': 0, 'negative': 0}

        average_positivity = sum(positive_comment_results) / total_sum_of_result_scores
        average_negativity = sum(negative_comment_results) / total_sum_of_result_scores

        # They also wanna see the final results of scoring (even tho they are returned).
        if display_all_comment_results:
            print(f'\nResults of all comments for submission: "{submission_id}"')
            print("Average Positivity: {:.2f}%".format(average_positivity * 100))
            print("Average Negativity: {:.2f}%".format(average_negativity * 100))

        return {'positive': average_positivity, 'negative': average_negativity}


    def analyze_subreddit(self, subreddit_name, sorting_type=None,
                          display_all_comment_results=False,
                          display_all_submission_results=False,
                          max_number_of_comments_to_analyze=0,
                          max_number_of_submissions_to_analyze=0):
        start_time = datetime.datetime.now()
        
        # This gives us a list of strings, with each str being a distinct subreddit_id.
        subreddit_submission_ids =\
            self.__reddit_collection.find(
                {'subreddit_name': subreddit_name}
                ).distinct('submission')

        # There are no posts from the subreddits.
        if len(subreddit_submission_ids) == 0:
           # We should let the user know.
            if display_all_comment_results or display_all_submission_results:
                print(f'No posts were found for the subreddit {subreddit_name}')
            # Since there are no submissions our scores are both going to be zero.
            return {'positive': 0, 'negative': 0}
        
        # We only want to grab the amount of submissions that the user wants us to.
        # We take the first n amount.
        if len(subreddit_submission_ids) > max_number_of_submissions_to_analyze and \
           max_number_of_submissions_to_analyze !=0:
            # It is not zero, so we know that the user wants to get a subset of comments,
            # we just needed to make sure that we had enough in the first place.
            # Now that we know we do, let's subset out comment list.
            subreddit_submission_ids = subreddit_submission_ids[: max_number_of_submissions_to_analyze]

        # This will have records appended to it to keep track of positive and negative results.
        # later we will divide it by the amount of submissions we have. It will hold mean averages.
        average_results_for_subreddit = {'positive': 0, 'negative': 0}

        for submission_id in subreddit_submission_ids:
            # Dict with all averages of a submission in given subreddit.
            analysis_results_of_submission = \
                self.analyze_submission(submission_id, sorting_type=sorting_type,
                                        display_all_comment_results=display_all_comment_results,
                                        max_number_of_comments_to_analyze=\
                                            max_number_of_comments_to_analyze)

            average_results_for_subreddit['positive'] += \
                analysis_results_of_submission['positive']

            # These values are negative, need to take abs.
            average_results_for_subreddit['negative'] += \
                analysis_results_of_submission['negative']

            # They want to see the rating for each submission post.
            if display_all_submission_results:
                print(f'Subreddit: {subreddit_name}:')
                print(f'Submission_id: {submission_id}:')
                print(f"Positivity Rating: {average_results_for_subreddit['positive']}")
                print(f"Negativity Rating: {average_results_for_subreddit['negative']}\n")

        # We can use this as our divisor in following calculations, so that we can
        # get average score for positivity and the average score for negativity.
        total_sum_of_all_submission_scores = average_results_for_subreddit['positive'] + \
                                             average_results_for_subreddit['negative']

        # We don't want to divide by zero.
        if total_sum_of_all_submission_scores != 0:
            average_results_for_subreddit['positive'] /= total_sum_of_all_submission_scores
            average_results_for_subreddit['negative'] /= total_sum_of_all_submission_scores

        # They wanna show the averages in the method.
        if display_all_submission_results:
            print(f'\nResults of all comments for : "{subreddit_name}"')
            print("Average positivity: {:2f}%".format(average_results_for_subreddit['positive'] * 100))
            print("Average negativity: {:2f}%".format(average_results_for_subreddit['negative'] * 100))
            print(f"Total time: {datetime.datetime.now() - start_time}")

        return average_results_for_subreddit


    # Later, once I implement word bubble and freq analysis.
    def show_hotest_submission_topics(self, submission_id):
        pass


    # Later, once I implement word bubble and freq analysis.
    def show_hotest_subreddit_topics(self, subreddit_id):
        pass
