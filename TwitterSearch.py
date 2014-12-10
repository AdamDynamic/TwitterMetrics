#!/usr/bin/env python

import twitter
import MySQLdb
import string
import logging

import Reference as r

def TransferResultsTables(db,cur):
    '''Clears the tbl_SearchResults_Old table and transfers the contents of the tbl_SearchResults_New to that table'''
    
    ClearOldTableQuery = "TRUNCATE TABLE " + r.DB_TABLE_SEARCHRESULTS_OLD + ";"
    RepopulateOldTableQuery = "INSERT INTO " + r.DB_TABLE_SEARCHRESULTS_OLD + " (" + r.SR_FIELD_TIMESTAMP + ", " + r.SR_FIELD_SEARCHTERM + ", " + r.SR_FIELD_SEARCHRESULT + ", " + r.SR_FIELD_TWEETID + ") SELECT " + r.SR_FIELD_TIMESTAMP + ", " + r.SR_FIELD_SEARCHTERM + ", " + r.SR_FIELD_SEARCHRESULT + ", " + r.SR_FIELD_TWEETID + " FROM " + r.DB_TABLE_SEARCHRESULTS_NEW + ";" 
    ClearNewTableQuery = "TRUNCATE TABLE " + r.DB_TABLE_SEARCHRESULTS_NEW + ";"
    
    cur.execute(ClearOldTableQuery)
    cur.execute(RepopulateOldTableQuery)
    cur.execute(ClearNewTableQuery)
    
    db.commit
    db.close
    
    return True


def SanitiseTextString(Input):
    '''Removes any characters that will stop the SQL code from working correctly'''
    
    Output = Input.translate(string.maketrans("",""), string.punctuation)
    return Output
    
def CreateListOfTrendsWOEID(api, GeographicCode):
    '''Returns a list of the top 10 current trends based on the WOEID code passed'''
    
    TrendsList = []
    
    Trends = api.GetTrendsWoeid(GeographicCode)
    
    for t in Trends:
        TrendsList.append(t.name)
    
    #l.CreateLogOfList("CreateListOfTrendsWOEID", True, TrendsList)
    logging.info('CreateListOfTrendsWOEID - List Created: %s', TrendsList)
        
    return TrendsList
    

def CreateListOfSearchResults(api, ListOfTerms, TimeStamp, LengthOfSearch=50):
    '''Searches Twitter for the terms passed in the list and returns a time-stamped list of the search terms and returned statuses'''
    
    ResultsList = []
    for i in range(0,len(ListOfTerms)):
        
        SearchResult = api.GetSearch(term=ListOfTerms[i], count=LengthOfSearch)
        
        for s in SearchResult:
            
            # Create a tuple of the date, the search term, the returned text, the tweet ID and the location           
            SearchTerm = SanitiseTextString(str(ListOfTerms[i]))
            
            SearchEntry = SanitiseTextString((s.text).encode('utf-8'))
            
            SearchID = s.id
            
            ResultsList.append((TimeStamp, SearchTerm, SearchEntry, SearchID))
            
    return ResultsList

def WriteTrendingTermsToDatabase(cur, TrendsList, TimeStamp):
    '''Writes the returned trending terms to the database'''
    
    for Trend in TrendsList:
        Query = "INSERT INTO " + r.DB_TABLE_TRENDINGTERMS + " ( " + r.TT_FIELD_TIMESTAMP + ", " + r.TT_FIELD_TERM + ") VALUES ('" + str(TimeStamp) + "', '" + Trend + "');"
        cur.execute(Query)
    
    return True

def ScanTwitter(TimeStamp):
    '''Scans Twitter for trending terms, searches for those terms and populates a database with the results'''
    
    FN_NAME = "ScanTwitter"
    
    ProcessResult = False
    
    # Establish the api connection
    api = twitter.Api(
                      consumer_key = r.CONS_TOKEN,
                      consumer_secret = r.CONS_SECRET,
                      access_token_key = r.ACCESS_TOKEN,
                      access_token_secret = r.ACCESS_SECRET
                      )
    
    # Establish the connection to the database
    db = MySQLdb.connect(
                         host=r.DB_HOST,
                         user=r.DB_USER,
                         passwd=r.DB_PASSWORD,
                         db=r.DB_NAME
                         )
    
    cur = db.cursor()
    
    # Transfer the previous search results to tbl_SearchResults_Old
    if TransferResultsTables(db,cur) == True:
    
        # Get the current trends
        TrendsList = CreateListOfTrendsWOEID(api, r.WOEID_UK)
        
        if TrendsList: # Checks whether the list is empty
            
            # Save the list of trends to the database
            WriteTrendingTermsToDatabase(cur, TrendsList, TimeStamp)
            
            # Return 100 most recent tweents for each trending item
            SearchResultsList =  CreateListOfSearchResults(api, TrendsList, TimeStamp, 100)
            
            if SearchResultsList: # Checks whether the list is empty
            
                # Insert into the database
                for tweet in SearchResultsList:
                    SearchQuery = "INSERT INTO " + r.DB_TABLE_SEARCHRESULTS_NEW + " ( " + r.SR_FIELD_TIMESTAMP + ", "  + r.SR_FIELD_SEARCHTERM + ", " + r.SR_FIELD_SEARCHRESULT + ", " + r.SR_FIELD_TWEETID + ") VALUES ('" + tweet[0] + "', '" + tweet[1] + "', '" + tweet[2] + "', '" + str(tweet[3]) + "');"
                    cur.execute(SearchQuery)
                
                db.commit()
                db.close
                
                ProcessResult = True

    logging.info('%s - Twitter scanned for trending terms with result %s', FN_NAME, ProcessResult)
                
    return ProcessResult
