If you found this repo useful, consider clicking the sponsor button near the top :) Sponsoring via GitHub is as little as $1/month and if you do not use banks or credit cards, there are crypto links included :)<br /><br />
# redditSentimentCombiner

1. Connect to gsheets for later: https://docs.google.com/spreadsheets/d/1rX4mniePZLIUCIFd7H2EdMioR_ip3LhtAjxJ2VclvXg/edit?usp=sharing

2. Connect to Reddit

3. Load top 1000 /r/bitcoin hot posts

4. Take the raw text, split it into an array on newline chars, filter out empty strings

5. Create an array of judged sentiments from the Natural Language Toolkkit's Vader function for each string in array from step 4

6. For each of the sentiments from step 5, grab the compound (overall) sentiment rating (which is based on values attributed to keywords and etc., wort a search on your favorite engine) and check if it's above or below a threshold value, then make them lowercase and replace 'bitcoin' with 'our coin' and 'btc' with 'our ticker' and ensure the string doesn't start with a shady substring then append the results to our positives && negatives arrays

7. Loop 10 times

8. For a range of maximum 6 strings, for first positive strings then negative strings take a random choice (so long as it's not already taken) and add it to a series of final sets of superpowerful strings

9. Print a bunch of useful information to terminal in the process of steps 7-8

10. Finally add a row to Positives and Negatives gsheet for each of the 10 superstrings

In an ideal world, people wouold use a variation of this script to load and replace keyword strings from many crypto-based subreddits, then push the final superstrings through a (good) word spinner, then post the resulting strings to create FOMO or FUD for a given perp.