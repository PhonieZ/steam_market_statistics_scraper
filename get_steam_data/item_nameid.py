#Library Imports
import json
from get_steam_data.core import *








#Main Scraping Logic
def get_item_nameid(market_url):
    global MARKET_URL_CONSTRUCTOR
    steam_app_id=0
    listing_name=""
    item_nameid=0



    steam_app_id,listing_name=deconstruct_market_url(MARKET_URL_CONSTRUCTOR,market_url)

    item_nameid=item_nameid_cache_lookup(steam_app_id,listing_name)


    if item_nameid == -1:   #TBD, Making Error Codes Less Stoopid
        item_nameid=scrape_item_nameid(market_url)

        if item_nameid is None:
            return(None)

        update_cache_data(steam_app_id,listing_name,item_nameid)


    return(item_nameid)




#Scraping Helper Functions
def deconstruct_market_url(MARKET_URL_CONSTRUCTOR,market_url):
    global URL_DIVIDER
    global HTML_SPACE
    market_url_properties=""



    market_url_properties=extract_constructor_contents(MARKET_URL_CONSTRUCTOR,market_url)

    market_url_properties=market_url_properties.split(URL_DIVIDER)
    market_url_properties[0]=int(market_url_properties[0])
    market_url_properties[1]=switch(market_url_properties[1],HTML_SPACE)

    return(market_url_properties)

def item_nameid_cache_lookup(steam_app_id,listing_name):
    try:
        cache=json.load(get_cache_data(is_raw=True))

    except:
        return(-1)    #Third Failure Case, json Is Empty



    try:
        steam_app_listings=cache[str(steam_app_id)]

    except:
        return(-1)    #First Failure Case, Listings For This App Id Cannot Be Found



    for current_listing_index in range(0,len(steam_app_listings)):
        if steam_app_listings[current_listing_index]["listing_name"] == listing_name:
            return(steam_app_listings[current_listing_index]["item_nameid"])
    
    else:
        return(-1)    #Second Failure Case, Cached Listing Not Found


def scrape_item_nameid(market_url):
    global JS_FUNCTION_CONSTRUCTOR
    global WHITESPACE
    url_html=""
    item_nameid=0



    url_html=get_html(market_url)

    if url_html is not None:
        url_html=extract_constructor_contents(JS_FUNCTION_CONSTRUCTOR,url_html).strip(WHITESPACE)
        item_nameid=int(url_html)


        return(item_nameid)        
    
    else:
        return(None)