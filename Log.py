#!/usr/bin/env python

# Contains the tools needed to input log entriess into the Log table

import MySQLdb
import time
import datetime
import logging

import Reference as r

def CreateTimeStamp():
    '''Create a timestamp with which to mark the log entry'''
        
    ts = time.time()
    TimeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    return TimeStamp

def CreateLogOfList(ProcessName, Status, InputList):
    '''Creates a log entry based on a list of items'''
    
    LogDescription = ""
    
    for Entry in InputList:
        LogDescription = LogDescription + Entry + ", "
        
        CreateLogEntry(ProcessName, Status, LogDescription)
        
def CreateLogEntry(ProcessName, Status, Description):
    '''Inputs a log entry into the Log table of the database'''
    
    db = MySQLdb.connect(
                         host=r.DB_HOST,
                         user=r.DB_USER,
                         passwd=r.DB_PASSWORD,
                         db=r.DB_NAME
                         )
    cur = db.cursor()
    
    TimeStamp = CreateTimeStamp()
    
    LogQuery = "INSERT INTO " + r.DB_TABLE_LOG + " ( " + r.LOG_FIELD_DATETIME + ", "  + r.LOG_FIELD_PROCESS + ", " + r.LOG_FIELD_STATUS + ", \
     " + r.LOG_FIELD_DESCRIPTION + ") VALUES ('" + str(TimeStamp) + "', '" + str(ProcessName) + "', " + str(Status) + ", '" + Description + "');"
      
    cur.execute(LogQuery)
     
    print ProcessName + ", " + str(Status) + ", " + Description
     
    db.commit()
    db.close