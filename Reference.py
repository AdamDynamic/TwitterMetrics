# Define the database access details
DB_HOST = "localhost"
DB_USER = "TwitterDB1"
DB_PASSWORD = "password"
DB_NAME = "databasename"

# Define the names of table in the database
DB_TABLE_SEARCHRESULTS_NEW = "tbl_SearchResults_New"
DB_TABLE_SEARCHRESULTS_OLD = "tbl_SearchResults_Old"
DB_TABLE_KEYWORDSRESULTS = "tbl_DATA_KeywordResults"
DB_TABLE_TRENDINGTERMS = "tbl_DATA_TrendingTerms"
DB_TABLE_WORDLISTS = "tbl_DATA_WordList"
DB_TABLE_LOG = "tbl_LOG"

# Column names from the wordlist tables
WL_FIELD_TIMESTAMP = "`DateTime`"
WL_FIELD_POSITIVE = "`Positive`"
WL_FIELD_NEGATIVE = "`Negative`"
WL_FIELD_STRONG = "`Strong`"
WL_FIELD_HOSTILE = "`Hostile`"
WL_FIELD_POWER = "`Power`"
WL_FIELD_WEAK = "`Weak`"
WL_FIELD_ACTIVE = "`Active`"
WL_FIELD_PASSIVE = "`Passive`"
WL_FIELD_PAIN = "`Pain`"
WL_FIELD_PLEASURE = "`Pleasure`"
WL_FIELD_TWEETSTOTAL = "`TotalTweets`"
WL_FIELD_WORDSTOTAL = "`TotalWords`"

# Column names from the SearchResults tables
SR_FIELD_TIMESTAMP = "`TimeStamp`"
SR_FIELD_SEARCHTERM = "`SearchTerm`"
SR_FIELD_SEARCHRESULT = "`SearchResult`"
SR_FIELD_TWEETID = "`TweetID`"

# Column names from the Trending Terms table
TT_FIELD_TIMESTAMP = "`TimeStamp`"
TT_FIELD_TERM = "`Term`"

# Column names from the KeywordResults table
KR_FIELD_TOTALWORDS = "`TotalWords`"
KR_FIELD_POSITIVE = "`Positive`"
KR_FIELD_NEGATIVE = "`Negative`"
KR_FIELD_DATETIME = "`DateTime`"

# Column names from the Log table
LOG_FIELD_DATETIME = "`DateTime`"
LOG_FIELD_PROCESS = "`Process`"
LOG_FIELD_STATUS = "`Status`"
LOG_FIELD_DESCRIPTION = "`Description`"

# Define the keys used by the Twitter API to authenticate
CONS_SECRET = "G7zzH7QXIXm6zXIyAJdxKqSWcnLd32TIT2nWN5Gi3I"
CONS_TOKEN = "lLEqtOfuNZRGTstXWz2TCQ"
ACCESS_SECRET = "XxPU6m6XfhGz7m0zOA7lWbqb14KrsMy1BoCFTsyo4ek"
ACCESS_TOKEN = "285675393-yJQcZlFPKWvbK3Eh4Xo6y4MacsVYk6tz2WQ8qHoE"

# WOEID IDs provide geographical information
WOEID_USA = 23424977
WOEID_LONDON = 44418
WOEID_UK = 23424975
