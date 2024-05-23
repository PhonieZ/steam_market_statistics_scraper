#Library Imports
from get_steam_data.core import *
import json
import datetime
import copy








#Main Price History Scraping Logic
def get_price_history(market_url):    #Important Note, Prices Here Are In USD And Not GDP (Due To Limitation) 
    price_history=[]



    price_history=scrape_price_history(market_url)

    if price_history is None:
        return(None)
    
    price_history=filter_price_history_data(price_history)

    return(price_history)


#Price History Scraping Helper Functions
def scrape_price_history(market_url):
    global PRICE_HISTORY_VARIABLE_CONSTRUCTOR
    url_html=""
    price_history=[]



    url_html=get_html(market_url)

    if url_html is None:
        return(None)
    

    url_html=extract_constructor_contents(PRICE_HISTORY_VARIABLE_CONSTRUCTOR,url_html)

    price_history=json.loads(url_html)



    return(price_history)








#Main Price History Data Filtering Logic
def filter_price_history_data(price_history):#TBD
    global DATETIME_STRING_FORMATTING
    filtered_data={}

    for current_entry in price_history:
        current_entry_date_object=extract_price_history_date_object(current_entry[0])


        current_entry_price=float(current_entry[1])

        current_entry_sale_volume=int(current_entry[2])


        if not(current_entry_price in filtered_data):    #Initalise Price Entry In Dict If It Doesn't Exist
            filtered_data[current_entry_price]=[]



        filtered_data[current_entry_price].append({
                                                        "date": current_entry_date_object,
                                                        "volume": current_entry_sale_volume
                                                  })



    return(filtered_data)


#Price History Data Filtering Helper Functions
def extract_price_history_date_object(raw_date):
    month, day, year, *_=raw_date.split(" ")    #*_ Ignores The Rest of The Values

    month=datetime.datetime.strptime(month,"%b").month

    date_object=datetime.datetime(int(year),int(month),int(day))

    return(date_object)