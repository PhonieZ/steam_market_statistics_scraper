# from get_steam_data import item_orders
# from get_steam_data import item_nameid
# from get_steam_data.core import *

# market_url="https://steamcommunity.com/market/listings/244850/Emissive%20Stripes%20Welder"
# item_gameid=item_nameid.get_item_nameid(market_url)
# buy_orders,sell_orders=item_orders.get_item_orders(item_gameid)
# item_name=item_nameid.deconstruct_market_url(MARKET_URL_CONSTRUCTOR,market_url)[1]

# print("\n"*4)
# print(item_name+":\n")
# print("Buy Orders:")
# for i in buy_orders:
#     entry="£{buy_order_price:.2f}: {buy_order_quantity}".format(buy_order_price=i[0],buy_order_quantity=i[1])
#     print(entry)
# print("\nSell Orders:")
# for i in sell_orders:
#     entry="£{sell_order_price:.2f}: {sell_order_quantity}".format(sell_order_price=i[0],sell_order_quantity=i[1])
#     print(entry)
# print("\n"*4)




from get_steam_data.core import *
from get_steam_data import price_history
from get_steam_data import item_orders
from get_steam_data import item_nameid

market_url="https://steamcommunity.com/market/listings/244850/Hazmat%20Helmet"
sales_history=price_history.get_price_history(market_url)
buy_orders, sell_orders=item_orders.get_item_orders(item_nameid.get_item_nameid(market_url))



# sales_metric={}    #In Sales Per Day
# date_range={
#                 "start": datetime.datetime(2023,11,28,0,0),
#                 "end": datetime.datetime.now()
#            }
# days_elapsed=date_range["end"] - date_range["start"]
# days_elapsed=days_elapsed.days


# for current_price, current_price_data in sales_history.items():
#     total_sales=0

#     for current_price_entry in current_price_data:
#         if not((current_price_entry["date"] >= date_range["start"]) and (current_price_entry["date"] <= date_range["end"])):
#             continue

#         total_sales+=current_price_entry["volume"]

#     sales_metric[current_price]=total_sales / days_elapsed


# for current_price, current_sales_metric in sales_metric.items():
#     print("${current_price}: {current_sales_metric} Sales Per Day".format(current_price=current_price,current_sales_metric=current_sales_metric))



# output_file=open("sus.json","w")
# output_file.write(str(sales_history))
# output_file.close()


# price_list=[*sales_history.keys()]
# price_list.sort()
# for i in price_list:
#     print(i)

print(buy_orders)
print("\n\n\n\n\n\n")    #had better gui for listing buy and sell orders, but lost it
print(sell_orders)