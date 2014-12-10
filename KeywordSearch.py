#!/usr/bin/env python

import MySQLdb
import string
import logging

import Reference as r

def CalculateWordCount(InputList,MatchList):
    '''Counts the instance of MatchList values in the InputList'''
    
    NumberOfMatches = 0
    for w in InputList:
        NumberOfMatches += MatchList.count(w)
        
    return NumberOfMatches

def ReturnQueryAsList(cur, Query):
    '''Runs a query on the database and returns the results as a list'''
    
    cur.execute(Query)
    ResultsTuple = cur.fetchall()
    ResultsList = [row[0] for row in ResultsTuple]
    
    return ResultsList

def SentenceToList(sentence):
    '''Strips out punctuation and returns a list of words in the sentence'''
    
    exclude = set(string.punctuation)
    
    return (''.join(ch for ch in sentence if ch not in exclude)).split()

def GetSearchResults(cur):
    '''Returns from the database the list of most recently searched tweets'''
    
    # Select only those search terms that are new since the last search was performed
    QUERY_SEARCHRESULTS_TEXT = "SELECT new." + r.SR_FIELD_SEARCHRESULT + " \
    FROM " + r.DB_TABLE_SEARCHRESULTS_NEW + " AS new \
    WHERE new." + r.SR_FIELD_TWEETID + " NOT IN( \
    SELECT old." + r.SR_FIELD_TWEETID + " \
    FROM " + r.DB_TABLE_SEARCHRESULTS_OLD + " AS old \
    WHERE new." + r.SR_FIELD_TWEETID + " = old." + r.SR_FIELD_TWEETID + ");"
    
    SearchResultsList = ReturnQueryAsList(cur, QUERY_SEARCHRESULTS_TEXT)
    
    logging.debug(QUERY_SEARCHRESULTS_TEXT)  
    
    return SearchResultsList

def InsertResultsIntoDatabase(cur, TimeStamp, ResultsDict, TotalTweets, TotalWords):
    '''Inserts the results of the keyword search back into the database'''
    
    # Define the columns the values will be entered into
    InsertResultsQuery = "INSERT INTO " + r.DB_TABLE_KEYWORDSRESULTS + " ( " + r.WL_FIELD_TIMESTAMP + ", " + r.WL_FIELD_POSITIVE + "\
    , " + r.WL_FIELD_NEGATIVE + ", " + r.WL_FIELD_STRONG + ", " + r.WL_FIELD_HOSTILE + "\
    , " + r.WL_FIELD_POWER + ", " + r.WL_FIELD_WEAK + ", " + r.WL_FIELD_ACTIVE + "\
    , " + r.WL_FIELD_PASSIVE + ", " + r.WL_FIELD_PAIN + ", " + r.WL_FIELD_PLEASURE + "\
    , " + r.WL_FIELD_TWEETSTOTAL + ", " + r.WL_FIELD_WORDSTOTAL + ") VALUES ('" + TimeStamp + "', " + str(ResultsDict['positive']) + "\
    , " + str(ResultsDict['negative']) + ", " + str(ResultsDict['strong']) + ", " + str(ResultsDict['hostile']) + ", " + str(ResultsDict['power']) + "\
    , " + str(ResultsDict['weak']) + ", " + str(ResultsDict['active']) + ", " + str(ResultsDict['passive']) + ", " + str(ResultsDict['pain']) + "\
    , " + str(ResultsDict['pleasure']) + ", " + str(TotalTweets) + ", " + str(TotalWords)+ ");" 
    
    logging.debug(InsertResultsQuery)
    
    cur.execute (InsertResultsQuery)
    
    return True

def SearchTweetsForKeywords(TimeStamp):
    '''Retrieves a twitter results from the database and scans them for keywords'''
    
    FN_NAME = "SearchTweetsForKeywords"
    ProcessResult = False
    
    # Establish the connection to the database
    db = MySQLdb.connect(
                         host=r.DB_HOST,
                         user=r.DB_USER,
                         passwd=r.DB_PASSWORD,
                         db=r.DB_NAME
                         )
    cur = db.cursor()

    QUERY_WORDLIST_POSITIVE = "SELECT Word FROM " + r.DB_TABLE_WORDLISTS + " WHERE Category = 'positive'"
    QUERY_WORDLIST_NEGATIVE = "SELECT Word FROM " + r.DB_TABLE_WORDLISTS + " WHERE Category = 'negative'"
    QUERY_WORDLIST_STRONG = "SELECT Word FROM " + r.DB_TABLE_WORDLISTS + " WHERE Category = 'strong'"
    QUERY_WORDLIST_HOSTILE = "SELECT Word FROM " + r.DB_TABLE_WORDLISTS + " WHERE Category = 'hostile'"
    QUERY_WORDLIST_POWER = "SELECT Word FROM " + r.DB_TABLE_WORDLISTS + " WHERE Category = 'power'"
    QUERY_WORDLIST_WEAK = "SELECT Word FROM " + r.DB_TABLE_WORDLISTS + " WHERE Category = 'weak'"
    QUERY_WORDLIST_ACTIVE = "SELECT Word FROM " + r.DB_TABLE_WORDLISTS + " WHERE Category = 'active'"
    QUERY_WORDLIST_PASSIVE = "SELECT Word FROM " + r.DB_TABLE_WORDLISTS + " WHERE Category = 'passive'"
    QUERY_WORDLIST_PAIN = "SELECT Word FROM " + r.DB_TABLE_WORDLISTS + " WHERE Category = 'pain'"
    QUERY_WORDLIST_PLEASURE = "SELECT Word FROM " + r.DB_TABLE_WORDLISTS + " WHERE Category = 'pleasure'"
    
    # Create lists of keywords to match against the search results
    WordListNegative = ReturnQueryAsList(cur, QUERY_WORDLIST_NEGATIVE)
    WordListPositive = ReturnQueryAsList(cur, QUERY_WORDLIST_POSITIVE)
    WordListStrong = ReturnQueryAsList(cur, QUERY_WORDLIST_STRONG)
    WordListHostile = ReturnQueryAsList(cur, QUERY_WORDLIST_HOSTILE)
    WordListPower = ReturnQueryAsList(cur, QUERY_WORDLIST_POWER)
    WordListWeak = ReturnQueryAsList(cur, QUERY_WORDLIST_WEAK)
    WordListActive = ReturnQueryAsList(cur, QUERY_WORDLIST_ACTIVE)
    WordListPassive = ReturnQueryAsList(cur, QUERY_WORDLIST_PASSIVE)
    WordListPain = ReturnQueryAsList(cur, QUERY_WORDLIST_PAIN)
    WordListPleasure = ReturnQueryAsList(cur, QUERY_WORDLIST_PLEASURE)
    
    # Retrieve the contents of the tbl_SearchResults table
    SearchResults = GetSearchResults(cur)
    
    TotalTweets = 0
    TotalWords = 0
    
    ResultsDict = {
                            'timestamp': 0,
                            'positive': 0,
                            'negative': 0,
                            'strong': 0,
                            'hostile': 0,
                            'power': 0,
                            'weak': 0,
                            'active': 0,
                            'passive': 0,
                            'pain': 0,
                            'pleasure': 0
                            }
    
    # Calculate the wordcounts for each search result against each of the keyword lists
    for Result in SearchResults:
        
        ResultAsList = SentenceToList(Result)
        
        TotalTweets = TotalTweets + 1
        TotalWords = TotalWords + len(ResultAsList)
        
        ResultsDict['negative'] = ResultsDict['negative'] + CalculateWordCount(ResultAsList, WordListNegative)
        ResultsDict['positive'] = ResultsDict['positive'] + CalculateWordCount(ResultAsList, WordListPositive)
        ResultsDict['strong'] = ResultsDict['strong'] + CalculateWordCount(ResultAsList, WordListStrong)
        ResultsDict['hostile'] = ResultsDict['hostile'] + CalculateWordCount(ResultAsList, WordListHostile)
        ResultsDict['power'] = ResultsDict['power'] + CalculateWordCount(ResultAsList, WordListPower)
        ResultsDict['weak'] = ResultsDict['weak'] + CalculateWordCount(ResultAsList, WordListWeak)
        ResultsDict['active'] = ResultsDict['active'] + CalculateWordCount(ResultAsList, WordListActive)
        ResultsDict['passive'] = ResultsDict['passive'] + CalculateWordCount(ResultAsList, WordListPassive)
        ResultsDict['pain'] = ResultsDict['pain'] + CalculateWordCount(ResultAsList, WordListPain)
        ResultsDict['pleasure'] = ResultsDict['pleasure'] + CalculateWordCount(ResultAsList, WordListPleasure)
    
    if InsertResultsIntoDatabase(cur, TimeStamp, ResultsDict, TotalTweets, TotalWords) == True:
        db.commit()
        ProcessResult = True
    
    db.close

    logging.info('%s - Retrieved %s tweets containing %s words with result %s', FN_NAME, TotalTweets, TotalWords, ProcessResult)
    
    
    return ProcessResult


