#!/usr/bin/env python

# Scans twitter for trending terms, populates a database with the results and
# then creates a json file showing trends based on the data

import CreateJson as j
import TwitterSearch as t
import KeywordSearch as k
import Log as l
import logging

ProcessResult = False
FN_NAME = "TrendingTermsSentiment"

logging.basicConfig(filename='TwitterMetrics_Sentiment.log', format='%(asctime)s %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)

logging.info('%s - Process Start', FN_NAME)


TimeStamp = l.CreateTimeStamp()

if t.ScanTwitter(TimeStamp) == True:
    if k.SearchTweetsForKeywords(TimeStamp) == True:
        ProcessResult = True
    else:
        logging.warning('%s - Function SearchTweetsForKeywords in KeywordSearch module failed to run correctly', FN_NAME)
else:
    logging.warning('%s - Function ScanTwitter in TwitterSearch module failed to run correctly', FN_NAME)

logging.info('%s - Process complete with status %s', FN_NAME, ProcessResult)






        
