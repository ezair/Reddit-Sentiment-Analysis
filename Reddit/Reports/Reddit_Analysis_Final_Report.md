# ID Block

- @author Eric Zair
- @project Reddit Analysis (<https://github.com/ezair/Reddit)>

## Project Description

There are two main goals for this project.

The first part is the `reddit_collector.py` program which is used to grab data from given subreddits using the `praw` API, which is used for mining reddit data. I will then add that collected data into a Mongodb database, using the `pymongo` API.

The second part of the project is the `SubredditAnalyzer` object that I will create. This object takes the data that was collected and put into the mongodb database and run sentiments analysis on it using the vader `SentimentIntensityAnalyzer`, which is an already created sentiment analyzer in the vader library. The `SentimentIntensityAnalyzer` will spit out a score of positivity and negativity for each comment that is fed to it. From there I will decide what is classified as positive and what is classified as negative.

**Note**: I have also created a preprocessing object called `RedditPreprocessor`, which is used to...preprocess each reddit comment by stemming the words, removing punctuation, ignoring stop words, and things of that sort.

## Approach

### reddit_collector.py

The first thing that I had to deal with was creating my own dataset (database) for reddit comments. This is the where I would pull the comments that will be analyzed out.

#### The functionality of this program is simple

We have a file called `sub_reddit_list.sub` which the user can add subreddits to, remove subreddits from, and collect data from every subreddit in the list.

```ignore
usage: reddit_post_collector.py [-h] [--collect | --add ADD | --remove REMOVE]

optional arguments:
  -h, --help       show this help message and exit
  --collect        Prompt the user for a data range and being collecting the
                   data. When we are done with collecting, we add the data to
                   the database.
  --add ADD        Add the sub-reddit passed in by the user to the list of
                   subreddits that we will collect data from.
  --remove REMOVE  Remove the subreddit passed in by the user.
```

##### Collecting

When a user choose to collect data from a subreddit, we grab *N* amount of comments on *K* amount of posts. The default amount of comments grabbed is 20 for testing reasons, however, the user can easily change this amount to what ever they would like. The *K* comments at this particular moment is actually every comment. In other words, currently we grab *N* amount of subreddits and from each of those subreddits, we grab **every** comment.

#### Error handling

Just as a note, the program already accounts for the problem of adding a subreddit that is already in our list of subreddits, as well as formatting of the file, and even checking to see if a subreddit exists.

### SubredditAnalyzer

This is the object that actually handles analyzing subreddits. The object is rather straight forward to use, but I will show a simple example of using it as well as the documentation on it.

#### Documentation

##### Class and constructor

```python
class SubredditAnalyzer():
    """Given a Mongodb database instance we are able to run sentiment analysis
    to analyzing given reddit submissions and subreddits as well.

    Using this object we can get the results for the positivity and negativity
    of a given subreddit or submission."""


    def __init__(self, mongo_reddit_collection, language='english'):
        """Constructs a SubRedditAnalyzer object."""

        """MongDB collection that we will be pulling our reddit data from.

        The database must have the following fielding fields in it:
            body, created_at, distinguished, edited, id, is_submitter
            link_id, parent_id, replies, score, stickied, submission
            subreddit, sorting_type."""
        self.__reddit_collection = mongo_reddit_collection
```

##### Method used to analyze a single submission

```python
def analyze_submission(self, submission_id, sorting_type=None,
                           display_all_comment_results=False,
                           max_number_of_comments_to_analyze=0):
        """Returns a dictionary containing the positivity and negativity of a submission.

        Arguments:\n
            submission_id {str} -- The reddit submission id of the submission you want to analyze.

        Keyword Arguments:\n
            sorting_type {str} -- Determines the type of comments you want to parse.
                                  Must be one of the following: 'hot', 'top', or 'new'
                                  (None is valid as well) (default: {None})\n
            display_all_comment_results {bool} -- True if user wants to seethe analysis results of each
                                                  comment; False otherwise. (default: {False})\n
            max_number_of_comments_to_analyze {int} -- This is the max amount of comments that we want to
                                                       analyze for a given submission.
                                                       A value of 0 means that we will collect all comments.
                                                       (default: {0})

        Returns:\n
            dict -- A dictionary in the form of {'positive': int_value, 'negative', int value}"""

```

##### Method used to analyze an entire subreddit

```python
def analyze_subreddit(self, subreddit_name, sorting_type=None,
                          display_all_comment_results=False,
                          display_all_submission_results=False,
                          max_number_of_comments_to_analyze=0,
                          max_number_of_submissions_to_analyze=0):
        """Return a dictionary containing the positive and negative results of a given subreddit.

        Arguments:\n
            subreddit_name {str} -- The subreddit that we want to analyze.

        Keyword Arguments:\n
            sorting_type {str} -- The type of posts that we will grab. either 'hot', 'top', 'new'.
                                  (default: {None})\n
            display_all_comment_results {bool} -- True if user wants to display analysis results of
                                                  comments. (default: {False})\n
            display_all_submission_results {bool} -- True if user wants to display all analysis results
                                                     of each submission in the subreddit.
                                                     (default: {False})\n
            max_number_of_comments_to_analyze {int} -- The max number of comments that we will analyze
                                                       for positivity and negativity. (default: {0})\n
            max_number_of_submissions_to_analyze {int} -- The max number of submissions that we are
                                                          going to analyze for positivity and
                                                          negativity. (default: {0})\n

        Returns:\n
            dict -- Dictionary containing the positivity and negativity of a given subreddit.
                    {'positive': int, 'negative': int}"""

```

#### Examples

The file `src/analyze_subreddits.py` is a script I wrote that can demonstrate the use of how the `SubredditAnalyzer` object is used. Feel free to check that out, it is quite helpful for seeing how you can make calls and do interesting things using the object.

##### Here is a simple example of how the object

```python
# Simple example of how to use the SubredditAnalyzer object for a subreddit.
def test_subreddit_call(analyzer):
   anylsis_results = analyzer.analyze_subreddit('battlestations', sorting_type='top',
                                                display_all_submission_results=True,
                                                display_all_comment_results=True,
                                                max_number_of_comments_to_analyze=10,
                                                max_number_of_submissions_to_analyze=10)
```

Running this method will analyze the subreddit "battlestations", only analyzing "top" comments from our mongo database. It will also display the results of each incoming submission (increasing our overall score for each submission that comes in). This method will also output the results of each individual comment that comes in. We have also assigned the amount of comments to grab from each submission to be 10, and the amount of submissions to analyze on to be 10 as well.

##### This method only needs to be called with subreddit

```python
def test_subreddit_call(analyzer):
   anylsis_results = analyzer.analyze_subreddit('battlestations')
```

This will analyze on **ALL** of the submissions and **ALL** of the comments in each submission. Sorting types do not matter here, we take **every** most. Also note, we do not print out the results of our analysis.

#### Output

The `analyze_subreddit` method returns a dict with a positivity and negativity score assosciated.

##### Example

A call like this:

```python
results_dict = reddit_analyzer.analyze_subreddit('battlestations',
                                                     max_number_of_comments_to_analyze=10,
                                                     max_number_of_submissions_to_analyze=5)
    print(results_dict)
```

Will return a dictionary like this:

```python
{'positive': 0.9208031230489626, 'negative': 0.07919687695103743}
```

This means that the subreddit was 92.08% positive and 0.079% negative.

**Note**: If you are interested in seeing what comment and submission results look like, check out the other to reports that I created in the `Reports/` folder. They have a lot of detail about what results look like and some mathematics behind them.

### RedditPreprocessor

The `RedditPreprocessor` is an object I created for specifically preprocessing a reddit comment.

I find that there is not much need to go into detail about this object, since its main purpose is to be used inside of the `SubredditAnalyzer`, however, is worth talking about how I preprocessed the data.

The data is preprocessed by taking each individual reddit comment (as a str of course) and using some nice tools contained in the Natural Language Processing Toolkit library in python (or `NLTK` for short).

Given a single string, we remove any punctuation from it, tokenize the string (into single words), remove any stop words, so that we do not analyze them, and then we stem the word (set the word to its base form). This stemming allows for words to not be analyzed differently simply because of the tense that the word is in. E.g. "run" and "running" should not be looked at differently.

Though the comment looks a little bit odd because of the way it is preprocessed, it make for much better results.

## Results & Testing

Due to the nature of the `SentimentIntensityAnalyzer` already being a built and trained model, it was a bit hard to test my results to confirm that they are accurate.

### Determining what subreddits to test with

My main method of doing this was by finding subreddits that were deemed as "toxic" or "bad" and similarly, finding subreddits that were deemed as "good" or "positive". To no surprise, this method was actually incredibly helpful for discovering issues with my code and things of that sort.

The main "negative" subreddit I used for testing was `holdmyfeedingtube` and the main positive subreddit I used was `battlestations`.

`holdmyfeedingtube` is a subreddit that is deemed incredibly negative, because of the nature of the submissions on it. Most of the submissions are about people doing dumb things and getting hurt badly as a result of those things. Thus most of the comments on these submissions tend to be really bad. (Feel free to look at the subreddit to see for yourself: <https://reddit.com/r/holdmyfeedingtube>).

'battlestations' is a subreddit deemed really positive because each submission is a forum about a really nice looking computer setup. People tend to upload beautiful looking computers, which results in people leaving really nice comments about how great a computer setup looks.(Link to subreddit if you are interested: <https://www.reddit.com/r/battlestations/>).

### Classifying positive and negative comments

The `SentimentIntensityAnalyzer` is great at calculating the positive level, and negative level, and neutral level of a subreddit, as well as the general `polarity` score, which is an extremely useful score.

When I started out the project, I decided that if a analysis result had a higher positive score than negative, then it should be classified as positive, and vice versa for negative results. But then I realized something really important! If something had a small score for positive and negative, but a high score for neutral, then it is just to close to call positive or negative. In other words, I found that results will high neutral scores to be bad for analysis, so I ignored them.

The only exception to the above was if I would find a result that was highly neutral and did not have a positivity score, or highly neutral and did not have a negativity score. In this specific case I decided to take that result and classify it. This was actually a good decision because, I started noticing that the overall results began to actually lean more to a certain direction. There were a lot of comments that were not being analyzed simply because they were too neutral, but a lot of these comments had a high neutral score and a score of zero for positive. In this case it was negative. Similarly if the score was high for neutral and had a score for positive, but no score for negative, then the comment is classified as positive. This allowed me to have a larger pool of data to compare. With more comments in the dataset, a single result becomes less meaningful, which is good, because then our results are not as heavily affected by one single comment.

Using the polarity score of a given comment, I was able to make the decision that if the comment had a polarity >= 0.5, then it was positive, and if it was < -0.5, then it was negative. If either of the cases was not true, we ignore the comment, unless it has no score for positive and has a score for negative, or vice versa.

#### Code for classification decision of a single comment

```python
analysis_results_of_comment = \
                self.__comment_sentiment_analyzer.polarity_scores(comment)

            # Comment might not be positive or negative, so by default it is ignored.
            # It will be set later if we find the comment to be positive or negative.
            classification_to_print_out = "Ignored"

            if(
                # Concluded comment is positive.
                analysis_results_of_comment['compound'] >= 0.05 or \
                analysis_results_of_comment['neg'] == 0 and analysis_results_of_comment['pos'] > 0
            ):
                positive_comment_results.append(analysis_results_of_comment['compound'])
                classification_to_print_out = "Positive"
            elif(
                # Concluded comment is negative.
                analysis_results_of_comment['compound'] <= -0.05 or \
                analysis_results_of_comment['pos'] == 0 and analysis_results_of_comment['neg'] > 0
            ):
                negative_comment_results.append(abs(analysis_results_of_comment['compound']))
                classification_to_print_out = "Negative"
```

### Submission Analysis

The previous demonstrates how I classify a single comment. In order to get the overall results of a single subreddit submission, I would run every comment through that process. If it was classified as positive, I add its compound score to a list of positive comments. If it is classified as negative, then I add its compound score to a list of negative comments. Otherwise the comment is completely ignored and does not at all weigh in on the overall scores for the submission.

After the analysis of each comment in the subreddit is done, I take the two populated lists (one for negative comments, one for positive), combine them together and sum their scores.

To find the positive score for the submission I divide the sum of positive scores and divide it by the sum of all scores.

To find the negative score for the submission I divide the sum of negative scores by the sum of all scores.

#### Code to demonstrate what was done

```python
 # Need this to later get percentages of negativity and positivity (math stuffs).
        total_sum_of_result_scores = sum(positive_comment_results + negative_comment_results)

        # This implies we have not analyzed anthing.
        if total_sum_of_result_scores == 0:
            return {'positive': 0, 'negative': 0}

        average_positivity = sum(positive_comment_results) / total_sum_of_result_scores
        average_negativity = sum(negative_comment_results) / total_sum_of_result_scores

        ... (In between code that does not matter)...

        return {'positive': average_positivity, 'negative': average_negativity}
```

### Subreddit Analysis

Analyzing an entire subreddit is extremely easy, most of the hard work is already done. We can just call the code that analyzes a single submission and run it on all *N* amount of submissions that we are trying to analyze for a given subreddit.

To figure out the positivity of the subreddit, we simply take the sum of the positive scores from each submission that was analyzed and then divide it by the sum of all scores (positive and negative scores).

To figure out the negativity of the subreddit, we simply take the sum of the negative scores from each submission that was analyzed and then divide it by the sum of all scores (positive and negative scores).

#### Code to demonstrate

```python
for submission_id in subreddit_submission_ids:
    # Dict with all averages of a submission in given subreddit.
    analysis_results_of_submission = \
        self.analyze_submission(submission_id, sorting_type=sorting_type,
                                display_all_comment_results=display_all_comment_results,
                                max_number_of_comments_to_analyze=\
                                    max_number_of_comments_to_analyze)

    average_results_for_subreddit['positive'] += analysis_results_of_submission['positive']
    average_results_for_subreddit['negative'] += analysis_results_of_submission['negative']

    ... (In between code that does not matter)...

    # We can use this as our divisor in following calculations, so that we can
    # get average score for positivity and the average score for negativity.
    total_sum_of_all_submission_scores = average_results_for_subreddit['positive'] +\
                                            average_results_for_subreddit['negative']

    # We don't want to divide by zero.
    # We would get to this point if all results were evaluated as neutral in an odd case.
    if total_sum_of_all_submission_scores != 0:
        average_results_for_subreddit['positive'] /= total_sum_of_all_submission_scores
        average_results_for_subreddit['negative'] /= total_sum_of_all_submission_scores

    return average_results_for_subreddit
```

### Model Accuracy

Overall, I find my results to be very accurate. To demonstrate how accurate my results appear to be, I wrote the following method (which can be found in at `src/analyze_subreddit.py`):

```python
# Simple method to show how the analyzer method can be used in different ways.
def compare_subreddit_sorting_type_results(subreddit, number_of_comments=0,
                                           number_of_submissions=0):
    analyzer = SubredditAnalyzer(DB_COLLECTION)

    top_analysis_results = analyzer.analyze_subreddit(subreddit, sorting_type='top',
                                                      max_number_of_comments_to_analyze=\
                                                          number_of_comments,
                                                      max_number_of_submissions_to_analyze=\
                                                          number_of_submissions)
    top_analysis_results['sorting_type'] = 'top'

    new_analysis_results = analyzer.analyze_subreddit(subreddit, sorting_type='new',
                                                      max_number_of_comments_to_analyze=\
                                                          number_of_comments,
                                                      max_number_of_submissions_to_analyze=\
                                                          number_of_submissions)
    new_analysis_results['sorting_type'] = 'new'

    hot_analysis_results = analyzer.analyze_subreddit(subreddit, sorting_type='hot',
                                                      max_number_of_comments_to_analyze=\
                                                          number_of_comments,
                                                      max_number_of_submissions_to_analyze=\
                                                          number_of_submissions)
    hot_analysis_results['sorting_type'] = 'hot'

    all_results = [top_analysis_results, new_analysis_results, hot_analysis_results]

    most_positive_result = sorted(all_results, key=lambda k: k['positive'], reverse=True)[0]
    most_negative_result = sorted(all_results, key=lambda k: k['negative'], reverse=True)[0]

    print(f"\nTop analysis results: {top_analysis_results}")
    print(f"New analysis results: {new_analysis_results}")
    print(f"Hot analysis results: {hot_analysis_results}\n")

    print(f"The most positive result is \"{most_positive_result['sorting_type']}\" "
          f"with a score of {most_positive_result['positive']}")

    print(f"The most negative result is \"{most_negative_result['sorting_type']}\" "
          f"with a score of {most_negative_result['negative']}")
```

Basically what this method does is analyze a subreddit for every single sorting type and then chooses the highest positivity level and the highest negativity level and prints them out.

I used this method to test against the `holdmyfeedingtube` subreddit (as an example of a negative subreddit) and the `battlestations` subreddit (as an example of a positive subreddit).

#### Running the method with r/battlestations

The function call:

```python
# Now, let's comare results on a much more negative subreddit.
# NOTICE: The results are MUCH higher for negativity and MUCH lower for positivity.
compare_subreddit_sorting_type_results('battlestations', number_of_comments=10,
                                        number_of_submissions=10)
```

The results:

```ignore
Top analysis results: {'positive': 0.9176357100895001, 'negative': 0.08236428991049997, 'sorting_type': 'top'}
New analysis results: {'positive': 0.9844417512498106, 'negative': 0.015558248750189366, 'sorting_type': 'new'}
Hot analysis results: {'positive': 0.9008543010876545, 'negative': 0.09914569891234548, 'sorting_type': 'hot'}

The most positive result is "new" with a score of 0.9844417512498106
The most negative result is "hot" with a score of 0.09914569891234548
```

#### Running the method with r/holdmyfeedingtube

The function call:

```python
compare_subreddit_sorting_type_results('holdmyfeedingtube', number_of_comments=10,
                                        number_of_submissions=10)
```

The results:

```ignore
Top analysis results: {'positive': 0.5779936093194682, 'negative': 0.4220063906805317, 'sorting_type': 'top'}
New analysis results: {'positive': 0.4714669086576282, 'negative': 0.5285330913423718, 'sorting_type': 'new'}
Hot analysis results: {'positive': 0.6917565559444011, 'negative': 0.3082434440555989, 'sorting_type': 'hot'}

The most positive result is "hot" with a score of 0.6917565559444011
The most negative result is "new" with a score of 0.5285330913423718
```

#### Comparison between holdmyfeedingtube and battlestations

So we can see that the highest negativity reported for battlestations is only 9.9% , which is not all that high. That means 1/10th of the time you will see a negative comment.

Now comparing that to holdmyfeedingtube, for which the highest negativity is 52.8%, that means that more than 1/2 of the time we are going to see a negative or toxic comment. I find this to be extremely interesting, because it certainly proves that our model is on the correct track.

## Challenges

There were certainly a lot of challenges in building this project.

I found one of the largest ones to be general error handling. Accounting for things like duplicate keys in a database, making sure queries exist, making sure the database exists, accounting for if fields in records retrieved from praw actually existed (some times they did not), making sure things do not get analyzed more than once, making sure the user gives us the correct fields in our analysis object, checking to see if a subreddit actually exists (which was more annoying than you would thinK), and much much more.

Another challenge was just structuring the project in general. Knowing what code to split up, when to split things into a distinct object, finding a good way to use credential files, but still git ignoring the file.

There were also certainly a lot of challenges with respect to deciding what the best way to classify a comment was. When was it positive, negative, and when should I ignore it.

Finally, deciding when to declare a subreddit as positive or negative and when to decide a submission is positive or negative.

## Moving Forward

As it stands, my model seems to be extremely accurate, but to dive even deeper in experimenting with it, I want to use LDA (Linear Discriminant Analysis) in order to implement topic modeling. Topic modeling will essentially display to me the most common talked about topics over all. More specifically, I am interested in topic modeling for nouns, mainly because I want to see what the most talked about "things" are for this model. I think seeing the most discussed things will help me to determine the overall score of a subreddit to the most talked about things. I would then be able to compare and see if those talked about things are positive from my own understanding, and compare that to what my model is saying.

...Honestly, this sounds super interesting and I look forward to working on it rather shortly!
