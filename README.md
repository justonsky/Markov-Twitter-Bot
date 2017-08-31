# Markov Chain Twitter Bot

Small, simple project, implementing a Markov Chain text generator bot in Python 3. Uses the MIT License.

## Prerequisites

This project uses the **python-twitter** library to access Twitter's API. You can install this using `pip3 install -r requirements.txt`, or simply `pip3 install python-twitter`.

Additionally, to run this project *you will need application tokens from Twitter itself*, which you can do by [signing up](https://twitter.com/signup) for the service and creating a new application [on this link](https://apps.twitter.com/).  For reference you will need these four tokens:

- Consumer Key (API Key)
- Consumer Secret (API Secret)
- Access Token
- Access Token Secret

## Getting Started

To get immediate use out of this project, replicate the repository to your local machine. Ensure the dependencies have been installed and you have obtained the requisite application tokens from Twitter.

You will need to set the generated tokens as environment variables on your machine, which you can do on Linux and macOS with the following:

```
export TWEETUSER=consumer_key
export TWEETPASS=consumer_secret
export TWEETACCESS=access_key
export TWEETACCSECRET=access_secret
```

From there, you can simply run `twitter-markov.py` followed by a list of twitter handles you want to use to train it. For example: `python3 twitter-markov.py twitter_handle1 twitter_handle2`. It will build a dictionary using their tweets and then issue tweets every 2 minutes.
