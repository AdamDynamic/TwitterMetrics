#!/usr/bin/env python

# Creates and saves a JSON file to update the D3.js graphs

import MySQLdb
import MySQLdb.cursors 
import json

import Reference as r
import logging

def CreateSentimentIndex(NegativeWords, PositiveWords, TotalWords):
    ''' Creates a sentiment value for the word counts'''
    
    if TotalWords != 0:
        Sentiment = ((PositiveWords - NegativeWords)/float(TotalWords))
    
    return Sentiment

def CreateJsonData(QueryResults):
    ''' Creates a list of dictionaries containing the dates and sentiment indexes'''
    
    Output = []
    
    for Row in QueryResults:
        RowDate = Row['DateTime'].strftime('%Y-%m-%d %H:%M:%S')
        RowSentiment = CreateSentimentIndex(Row['Negative'], Row['Positive'], Row['TotalWords'])
        Output.append({"date" : RowDate, "index" : RowSentiment})
    
    return Output
        
def OutputJsonFile(InputDictionary):
    '''Saves a dictionary to an output file in a JSON format'''
    
    JsonOutput = json.dumps(InputDictionary)
    OutputFileName = 'json/twittermetrics_sentiment.js'
    FileOutput = open(OutputFileName,'w')
    print >> FileOutput, JsonOutput 
    
    return True   
    
def CreateJsonFile():
    '''Extracts data from the database and saves a JSON file to the server'''
    
    FN_NAME = "CreateJsonFile"
    
    dbDict = MySQLdb.connect(
                         host=r.DB_HOST,
                         user=r.DB_USER,
                         passwd=r.DB_PASSWORD,
                         db=r.DB_NAME,
                         cursorclass=MySQLdb.cursors.DictCursor
                         )
    curDict = dbDict.cursor()
    
    Query = "SELECT " + r.KR_FIELD_TOTALWORDS + ", " + r.KR_FIELD_POSITIVE + ", " + r.KR_FIELD_NEGATIVE + ", " + r.KR_FIELD_DATETIME + " FROM " + r.DB_TABLE_KEYWORDSRESULTS + ";"
    
    logging.debug(FN_NAME, Query)
    
    curDict.execute(Query)
    
    QueryResults = curDict.fetchall()
    
    Output = CreateJsonData(QueryResults)
    
    ProcessResult = OutputJsonFile(Output)
    
    logging.info('%s - JSON file created and saved to server with result %s', FN_NAME, ProcessResult)
    
    dbDict.close
    
    return ProcessResult

    