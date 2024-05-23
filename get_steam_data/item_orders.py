#Library Imports
from get_steam_data.core import *
import json








#Main Item Order Querying Logic
def get_item_orders(item_nameid):
    global ITEM_ORDER_URL_CONSTRUCTOR
    global ITEM_ORDER_ARGUMENT_DIVIDER
    item_order_url=""
    item_order_response=""
    buy_orders=[]
    sell_orders=[]



    request_arguments={
                          "norender": 1,
                          "country": "GB",
                          "language": "english",
                          "currency": 2,
                          "item_nameid": item_nameid,
                          "two_factor": 0
                      }
    


    item_order_url=construct_url_arguments(request_arguments,ITEM_ORDER_URL_CONSTRUCTOR,ITEM_ORDER_ARGUMENT_DIVIDER)
    

    item_order_response=get_html(item_order_url)

    if item_order_response is None:
        return(None)


    item_order_response=json.loads(item_order_response)


    buy_orders=construct_item_order_list(item_order_response["buy_order_graph"])
    sell_orders=construct_item_order_list(item_order_response["sell_order_graph"])

    return(buy_orders,sell_orders)




#Item Order Querying Helper Functions
def construct_item_order_list(raw_buy_orders):
    buy_orders=[]

    for current_entry_index in range(0,len(raw_buy_orders)):
        current_entry=raw_buy_orders[current_entry_index]

        if current_entry_index != 0:
            last_entry=raw_buy_orders[current_entry_index-1]
        else:
            last_entry=[0.00,0,""]    #Incase We Are At Start Of The List

        current_buy_order_price=current_entry[0]
        current_buy_order_count=current_entry[1]-last_entry[1]
        
        buy_orders.append([current_buy_order_price,current_buy_order_count])

    return(buy_orders)