# ID Block

- @Author Eric Zair
- @Course Machine Learning
- @Instructor Dr. Gurajala
- @Project Reddit Analysis
- @Assignment Report 1

## MongoDB Records

We are using MongoDB as our DBMS. Inside of this DBMS we have a Database called `Reddit` which has only one instance/record inside of it called `submission_comment`.

### submission_comment Fields

The following are all of the fields that are stored in a document/table for a `submission_comment`:

```python
submission_comment_record = {
    'author': author_id,
    'body': submission_comment.body,
    'created_at': submission_comment.created_utc,
    'distinguished': submission_comment.distinguished,
    'edited': submission_comment.edited,
    '_id': submission_comment.id,
    'is_submitter': submission_comment.is_submitter,
    'link_id': submission_comment.link_id,
    'parent_id': submission_comment.parent_id,
    'replies': replies,
    'score': submission_comment.score,
    'stickied': submission_comment.stickied,
    'submission': submission_comment.submission.id,
    'subreddit_name': submission_comment.subreddit.display_name,
    'subreddit_id': submission_comment.subreddit_id,
    'sorting_type': sorting_type
}
```

This is an exact example of how the records are being created in our python code.

Rather than storing the actual reddit objects themselves, we store references to them that can be looked up by accessing the `praw` API, being that we do no actually add any other reddit instances aside from `post_comment` in our database and thus cannot query them directly.

## Features

Since we are going to be preforming Sentiment Analysis on a collection of reddit comments, the main feature that we really care about is the text body of a comment. In the case of the above this would be `submission_comment_record['body']`.

The other useful field is the `sorting_type` field. Playing around with this field, we can determine if a comment is "hot", "new", or "top".

### Data Parsed From Features

There is a lot of distinct things that you can do with the `body` of a comment. Especially when we have a huge amount of them. The main thing we are going to do with this data (in the `reddit_analyze_sub_reddits.py` program specifically, is take the sentiment results from each individual comment and then average up their positivity, their negativity, and their neutrality together. We can then figure out an average rating for a given submission or a given subreddit, depending on what we decided to do when we run the program.

```txt
Subreddit Name: dankmemes
Comment: downvot bot best
Positivity Rating: 0.677
Negativity Results: 0.0
Neutral results: 0.323

Subreddit Name: dankmemes
Comment: appar someon alreadi call repostsleuthbot
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: shitload someth
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: Da boi meme tight
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: Oh thank updat
Positivity Rating: 0.556
Negativity Results: 0.0
Neutral results: 0.444

Subreddit Name: dankmemes
Comment: suppos releas summer
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: thank kind fellow
Positivity Rating: 0.855
Negativity Results: 0.0
Neutral results: 0.145

Subreddit Name: dankmemes
Comment: nah guy post two subreddit
Positivity Rating: 0.0
Negativity Results: 0.259
Neutral results: 0.741

Subreddit Name: dankmemes
Comment: best guess mod decid need
Positivity Rating: 0.512
Negativity Results: 0.0
Neutral results: 0.488

Subreddit Name: dankmemes
Comment: would kill like alreadi dead
Positivity Rating: 0.185
Negativity Results: 0.667
Neutral results: 0.148

Subreddit Name: dankmemes
Comment: holi shit dude kill
Positivity Rating: 0.0
Negativity Results: 0.806
Neutral results: 0.194

Subreddit Name: dankmemes
Comment: peopl hate prove wrong
Positivity Rating: 0.0
Negativity Results: 0.773
Neutral results: 0.227

Subreddit Name: dankmemes
Comment: think bot work 100 time
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: Da boi meme tight
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: problem man
Positivity Rating: 0.0
Negativity Results: 0.73
Neutral results: 0.27

Subreddit Name: dankmemes
Comment: someon alreadi post way least meme idea differ pictur
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: burn corps dead burn afterlif
Positivity Rating: 0.0
Negativity Results: 0.518
Neutral results: 0.482

Subreddit Name: dankmemes
Comment: prove wrong wrong rememb see meme back
Positivity Rating: 0.0
Negativity Results: 0.554
Neutral results: 0.446

Subreddit Name: dankmemes
Comment: liter made
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: Da boi meme tight
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: well shit differ pictur everi meme templat use differ pictur somewher everi popular templat would repost dont get wrong im justifi make small chang meme call origin dont think fall repost yet howev might call borderlin repost someth
Positivity Rating: 0.165
Negativity Results: 0.08
Neutral results: 0.755

Subreddit Name: dankmemes
Comment: OP made half commun burn repost witch
Positivity Rating: 0.0
Negativity Results: 0.294
Neutral results: 0.706

Subreddit Name: dankmemes
Comment: Da boi meme tight
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: yeah know cours bot recogn pictur said guy said like super origin meme sure pictur
Positivity Rating: 0.498
Negativity Results: 0.0
Neutral results: 0.502

Subreddit Name: dankmemes
Comment: true
Positivity Rating: 1.0
Negativity Results: 0.0
Neutral results: 0.0

Subreddit Name: dankmemes
Comment: Da boi meme tight
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: get link
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: Da boi meme tight
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: w month ago point even tri
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: Da boi meme tight
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: Da boi meme tight
Positivity Rating: 0.0
Negativity Results: 0.0
Neutral results: 1.0

Subreddit Name: dankmemes
Comment: well prove
Positivity Rating: 0.677
Negativity Results: 0.0
Neutral results: 0.323

Results of all comments:
Average positivity: 0.14238059701492536
Average negativity: 0.121634328358209
Average neutrality: 0.7210298507462682
```
