#! python3

import sys
import os
import argparse
import pickle
import time
import markov
import twitter

parser = argparse.ArgumentParser(description='Markov chain text generator written in Python.')
parser.add_argument('step', metavar='N', type=int, nargs=1,
                    help='Determines length of keys in the program\'s dictionary.')
parser.add_argument('twitter_handles', type=str, nargs='+',
                    help='List of twitter handles to use.')
args = parser.parse_args()

pickle_file = 'entries.pickle'
consumer_key = os.environ.get("TWEETUSER")
consumer_secret = os.environ.get("TWEETPASS")
access_token_key = os.environ.get("TWEETACCESS")
access_token_secret = os.environ.get("TWEETACCSECRET")


def dict_save(data, pickle_file):
    with open(pickle_file, 'ab') as f:
        pickle.dump(data, f)

def dict_load(data, pickle_file):
    try:
        f = open(pickle_file, 'rb')
    except:
        print("No pickle file detected, creating new one...")
        dict_save(data, pickle_file)
    else:
        data = pickle.load(f)
        f.close()

def train(api, data, person):
    markov_prefix_length = int(args.step[0])
    tweet_since_count = None
    test = 1

    while(tweet_since_count != test):
        test = tweet_since_count
        try:
            tweets_list = api.GetUserTimeline(screen_name=person, 
                                        count=200, 
                                        include_rts=False, 
                                        max_id=tweet_since_count)
        except:
            print('Something went wrong getting {person}\'s tweets. Going to next person.'.format(person=person))
            dict_save(data, pickle_file)
            break
        else:
            tweet_since_count = tweets_list[-1].id

        tweet_text = [status.text for status in tweets_list]

        # Pass text from status update to markov chain dictionary
        for text in tweet_text:
            for key, value in markov.parse_input(text, markov_prefix_length):

                if isinstance(key, markov.ParseLengthError):
                    pass
                else:
                    markov.build_dict(data, key, value)

        # Save dictionary to pickle
        dict_save(data, pickle_file)


if __name__ == '__main__':
    data_table = {}
    dict_load(data_table, pickle_file)
    print("Dictionary loaded! Continuing...")
    print("Length of data table: ", len(data_table))

    # Authentication using OAuth
    twitter_api = twitter.Api(consumer_key, 
                            consumer_secret, 
                            access_token_key, 
                            access_token_secret, 
                            sleep_on_rate_limit=True)

    print("Authenticated. Continuing, grasping tweets...")

    for celebrity in args.twitter_handles:
        train(twitter_api, data_table, celebrity)
    
    print("Tweets from list of accounts processed. Moving to sentence generation.")

    while(True):
        # Generates a sentence, tweets it, then sleeps.
        text = markov.generate_sentence(data_table)
        twitter_api.PostUpdate(text)
        time.sleep(120)