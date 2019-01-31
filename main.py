import time
import praw
from pprint import pprint
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentiText
from nltk import tokenize
import ssl
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('googlesheets.json', scope)

gc = gspread.authorize(credentials)

posSheet = gc.open("Reddit Randoms").worksheet('Positives')
negSheet = gc.open("Reddit Randoms").worksheet('Negatives')

r = praw.Reddit(client_id='',
                     client_secret="", password='',
                     user_agent='USERAGENT', username='h3xadecimal138')


def generatesentiment(k, text):
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(text)
    sentiment = {
        k: text,
        "sentiment": score,
        "v_neg": [],
        "s_neg": [],
        "v_pos": [],
        "s_pos": []
    }

    sentitext = SentiText(text).words_and_emoticons

    for i, w in enumerate(sentitext):
        w_lower = w.lower()
        if w_lower in sid.lexicon:
            score = sid.lexicon[w_lower]
            word_obj = {"word": w, "score": score}
            if score <= -2.4:
                sentiment["v_neg"].append(word_obj)
            elif score <= -0.8:
                sentiment["s_neg"].append(word_obj)
            elif score >= 2.4:
                sentiment["v_pos"].append(word_obj)
            elif score >= 0.8:
                sentiment["s_pos"].append(word_obj)

    return sentiment 
positives = []
negatives = []
subreddit = r.subreddit('bitcoin')
for submission in subreddit.hot(limit=1000):
	text = (vars(submission)['selftext'])
	splits = text.split('\n')
	splits = list(filter(None, splits))
	sentiments = [generatesentiment("split", split) for split in splits]
	for sentiment in sentiments:
		compound = (sentiment['sentiment']['compound'])
		if compound > 0.6:
			lower = sentiment['split'].lower().replace('bitcoin', '[[our coin]]').replace('btc', '[[our ticker]]')
			if not lower.startswith('>') and not lower.startswith('**') and not lower.startswith('##')and not lower.startswith('[http'):
				positives.append(lower)
		if compound < -0.6:
			lower = sentiment['split'].lower().replace('bitcoin', '[[our coin]]').replace('btc', '[[our ticker]]')
			if not lower.startswith('>') and not lower.startswith('**') and not lower.startswith('##')and not lower.startswith('[http'):
				negatives.append(lower)
print('positive sentences last 100 posts in /r/bitcoin: ' + str(len(positives)))
print('negative sentences last 100 posts in /r/bitcoin: ' + str(len(negatives)))
posChoices = []
negChoices = []
def posF(n: int, C: list) -> list:
	choice = random.choice (positives)
	print(n)
	if choice not in posChoices:
		posChoices.append(choice)
		C.append(choice)
		n = n - 1
	if n >= 0:
		return posF(n, C)
	else:
		return C
def negF(n: int, C: list) -> list:
	choice = random.choice (negatives)
	if choice not in negChoices:
		negChoices.append(choice)
		C.append(choice)
		n = n - 1
	if n >= 0:
		return posF(n, C)
	else:
		return C
for n in range(10):
	empty = []
	poses = int(len(positives) / 10)
	if poses > 6:
		poses = 6
	posC = posF(poses, empty)
	print('individual random positive sentences from /r/bitcoin with the word bitcoin replaced with [[our coin]], and btc with [[our ticker]]:')
	for choice in posC:
		print(' ')
		print(choice)
	print(' ')
	print('and combined, as if we are posting:')
	posPara = ""
	print(' ')
	for choice in posC:
		posPara = posPara + choice + " "
	print(posPara)
	posArray = []
	posArray.append(posPara)
	posSheet.append_row(posArray)
	
	neges = int(len(negatives) / 10)
	if neges > 6:
		neges = 6
	empty = []
	negC = negF(neges, empty)
	print(' ')
	print('individual random negative sentences from /r/bitcoin with the word bitcoin replaced with [[our coin]], and btc with [[our ticker]]:')
	for choice in negC:
		print(' ')
		print(choice)
	print(' ')
	print('and combined, as if we are posting:')
	print(' ')
	negPara = ""
	for choice in negC:
		negPara = negPara + choice + " "
	print(negPara)
	negArray = []
	negArray.append(negPara)
	negSheet.append_row(negArray)