#Library Imports
import json
import datetime
import subprocess
from urllib.request import urlopen




#Constants
ITEM_NAMEID_CACHE_DIRECTORY="item_nameid_cache.json"    #Where json Cache For item_nameid Is Located
CALL_LOG_FILE_EXTENSION=".tmp"                          #File Extension For Files Keeping Track Of Rate Limits

DATETIME_STRING_FORMATTING="%Y-%m-%d %H:%M:%S.%f"    #Format Used For Converting A Datetime Object To And From This Library's Standard String

MARKET_URL_CONSTRUCTOR=["https://steamcommunity.com/market/listings/",""]    #["Prefix","Suffix"] , For Scraping item_nameid
URL_DIVIDER="/"                                                              #Just A Forward Slash
HTML_SPACE=["%20"," "]                                                       #Conversion Table For Converting A Regular Space To Its html Equiavalent

JS_FUNCTION_CONSTRUCTOR=["Market_LoadOrderSpread(",");"]    #["Prefix","Suffix"] , For Locating item_nameid In js Function Call
WHITESPACE=" "                                              #Just Whitespace

SCRAPE_LIMIT=[10,60]    #[ScrapeCallCount,GivenSeconds] , Or At Most (ScrapeCallCount) Scrapes Can Be Made In (GivenSeconds) Seconds

ITEM_ORDER_URL_CONSTRUCTOR=["https://steamcommunity.com/market/itemordershistogram?",""]    #["Prefix","Suffix"] , For Obtaining Buy And Sell Order Statistics
ITEM_ORDER_ARGUMENT_DIVIDER="&"                                                             #For Seperating Arguments

PRICE_HISTORY_VARIABLE_CONSTRUCTOR=["var line1=",";"]   #["Prefix","Suffix"] , For Locating The Data For price_history In a js Script




#Globals
scrape_log=[0,None]             #[ScrapesMade,StartTimestamp] , To Ensure Scrape Rate Limit Isn't Exceeded








#Debug Functions
def dump(output):
    print("\n\n"+str(output)+"\n\n")








#Misc Helper Functions
def switch(string,conversion_table):                   #Switches Keys Present In A String Corresponding To conversion_table Contents
    is_key0_in_target=conversion_table[0] in string
    is_key1_in_target=conversion_table[1] in string

    if is_key0_in_target and is_key1_in_target:        #First Failure Case, Cannot Convert String With Both Keys Present
        return(string)
    
    if not(is_key0_in_target or is_key1_in_target):    #Second Failure Case, Neither Key Is Present
        return(string)

    elif is_key0_in_target:
        return(string.replace(conversion_table[0],conversion_table[1]))
    
    elif is_key1_in_target:
        return(string.replace(conversion_table[1],conversion_table[0]))








#Constructor Functions
def extract_constructor_contents(CONSTRUCTOR,string):
        if CONSTRUCTOR[0] == "":    
            start_index=0                          #Incase Prefix Is Omitted
        else:
            start_index=string.find(CONSTRUCTOR[0])

        start_index+=len(CONSTRUCTOR[0])


        if CONSTRUCTOR[1] == "":    
            end_index=len(string[start_index:])    #Incase Suffix Is Omitted
        else:
            end_index=string[start_index:].find(CONSTRUCTOR[1])
        
        end_index+=start_index


        return(string[start_index:end_index])   








#Rate Limit Enforcer Functions
def call_rate_limit_status(CALL_RATE_LIMIT,call_log,identifier,is_verbose=False):
    end_timestamp=call_log[1]
    current_timestamp=datetime.datetime.now()

    call_log=refresh_call_log(CALL_RATE_LIMIT,call_log,identifier)

    if call_log[0] >= CALL_RATE_LIMIT[0]:
        if is_verbose:
            return(call_log,int((end_timestamp-current_timestamp).seconds))   #Gives Seconds Till Calls Can Be Made Again
        
        else:
            return(call_log,False)                                               #Exceeded Call Rate Limit
        
    else:
        return(call_log,True)                                                    #Call Rate Limit Not Exceeded

def increment_calls_made(CALL_RATE_LIMIT,call_log,identifier):
    call_log=refresh_call_log(CALL_RATE_LIMIT,call_log,identifier)

    call_log[0]+=1

    update_call_log(call_log,identifier)

    return(call_log)

def init_call_log(CALL_RATE_LIMIT,call_log,identifier):
    end_timestamp=datetime.datetime.now()+datetime.timedelta(seconds=CALL_RATE_LIMIT[1])

    call_log=[]
    call_log.append(0)
    call_log.append(end_timestamp)

    update_call_log(call_log,identifier)

    return(call_log)

def refresh_call_log(CALL_RATE_LIMIT,call_log,identifier):
    end_timestamp=call_log[1]
    current_timestamp=datetime.datetime.now()

    if end_timestamp == None:    
        call_log=init_call_log(CALL_RATE_LIMIT,call_log,identifier)

    elif current_timestamp > end_timestamp:   
        call_log=init_call_log(CALL_RATE_LIMIT,call_log,identifier)

    return(call_log)








#URL Handling Functions
def get_html(url):
    global SCRAPE_LIMIT
    global scrape_log
    url_html=""

    scrape_log,can_scrape=call_rate_limit_status(SCRAPE_LIMIT,scrape_log,"scrape_log")



    if can_scrape:
        url_html=urlopen(url).read().decode("utf-8")

        scrape_log=increment_calls_made(SCRAPE_LIMIT,scrape_log,"scrape_log")

        return(url_html)
        
    else:
        return(None)
    
def construct_url_arguments(arguments,URL_CONSTRUCTOR,ARGUMENT_DIVIDER):
    url=""



    url=URL_CONSTRUCTOR[0]

    for current_argument in arguments:
        url+="{argument}={value}".format(argument=current_argument,value=arguments[current_argument])
        url+=ARGUMENT_DIVIDER

    url=url[:-1]

    url+=URL_CONSTRUCTOR[1]


    return(url)








#JSON Caching Functions
def get_cache_data(is_raw=False):
    global ITEM_NAMEID_CACHE_DIRECTORY
    cache_data=open(ITEM_NAMEID_CACHE_DIRECTORY,"r")

    if is_raw:
        return(cache_data)
    
    else:
        return(cache_data.read())
    
def update_cache_data(steam_app_id,listing_name,item_nameid):
    try:
        cache_data=json.load(get_cache_data(is_raw=True))

    except:
        cache_data=json.loads("{}")
        


    new_listing={
                    "listing_name": str(listing_name),
                    "item_nameid": item_nameid
                }



    if not(str(steam_app_id) in cache_data.keys()):
        cache_data[str(steam_app_id)]=[]

        

    cache_data[str(steam_app_id)].append(new_listing)



    cache_data_pointer=open(ITEM_NAMEID_CACHE_DIRECTORY,"w")

    json.dump(cache_data,cache_data_pointer,indent=4)

    cache_data_pointer.close()

def update_call_log(call_log,identifier):
    global CALL_LOG_FILE_EXTENSION
    global DATETIME_STRING_FORMATTING
    call_log_file_name=identifier+CALL_LOG_FILE_EXTENSION
    call_log_data_to_write=[]

    call_log_data_to_write.append(str(call_log[0]))
    call_log_data_to_write.append(call_log[1].strftime(DATETIME_STRING_FORMATTING))

    subprocess.check_call(["attrib","-H",call_log_file_name])

    call_log_pointer=open(call_log_file_name,"w")
    call_log_pointer.write(call_log_data_to_write[0]+"\n"+call_log_data_to_write[1])
    call_log_pointer.close()

    subprocess.check_call(["attrib","+H",call_log_file_name])

def retrieve_call_log(identifier):
    global CALL_LOG_FILE_EXTENSION
    global DATETIME_STRING_FORMATTING
    call_log_file_name=identifier+CALL_LOG_FILE_EXTENSION
    call_log=[]

    try:
        call_log_pointer=open(call_log_file_name,"r")
        call_log_data=call_log_pointer.readlines()

        call_log.append(int(call_log_data[0].strip("\n")))
        call_log.append(datetime.datetime.strptime(call_log_data[1].strip("\n"),DATETIME_STRING_FORMATTING))

        call_log_pointer.close()
        return(call_log)

    except:
        return(None)











#Initialization Code
scrape_log=retrieve_call_log("scrape_log")
scrape_log=refresh_call_log(SCRAPE_LIMIT,scrape_log,"scrape_log")