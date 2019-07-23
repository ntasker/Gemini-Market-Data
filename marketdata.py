import websocket
import json 
from sortedcontainers import SortedDict
from operator import neg

#Sorted dictionaries for storing data, highest is at top in bid_dict, lowest is at top in ask_dict
bid_dict = SortedDict()
ask_dict = SortedDict(neg)

def on_message(ws, message):
    market_data = json.loads(message)
    #Setup inital values if it is the first message
    if(market_data['socket_sequence'] == 0):
        raw_data = market_data['events']
        set_initial(raw_data)
    #Add update to dictionaries, if not first message
    else:
        change_event = market_data['events']
        set_update(change_event)

def on_error(ws, error):
    print(error)

def on_close(ws):
    #Run when connection to websocket is closed
    print("### closed ###")

def set_initial(data):
    global bid_dict
    global ask_dict

    #Sort inital response into correct dictionaries
    for item in data:
            side = item['side']
            if side == 'bid':
                price = item.pop('price')
                bid_dict[float(price)] = item
            else:
                price = item.pop('price')
                ask_dict[float(price)] = item

def set_update(change_event):
    global bid_dict
    global ask_dict
    
    #Only check for updates with type change
    if change_event[0]['type'] == 'change': 
        change_price = float(change_event[0]['price'])
        change_quantity = float(change_event[0]['remaining'])
        
        #Seperate bid and ask updates
        if change_event[0]['side'] == 'bid':
            #if quantity of update is 0, remove price level
            if(change_quantity == 0):
                bid_dict.pop(change_price)
                #print values to reflect any changes
                print_values()
            else:
                change_event[0].pop('price')
                bid_dict[change_price] = change_event
                print_values()
        else:
            if(change_quantity == 0):
                ask_dict.pop(change_price)
                print_values()
            else:
                change_event[0].pop('price')
                ask_dict[change_price] = change_event
                print_values()

def print_values():
    global bid_dict
    global ask_dict

    #data from top of dictionaries
    bid_tmp = bid_dict.peekitem()
    ask_tmp = ask_dict.peekitem()

    #values from top of dictionaries
    curr_best_bid = float(bid_tmp[0])
    curr_bid_quant = float(bid_tmp[1][0]['remaining'])

    curr_best_ask = float(ask_tmp[0])
    curr_ask_quant = float(ask_tmp[1][0]['remaining'])


    print("{0:.2f} {1:.8f} - {2:.2f} {3:.8f}".format(curr_best_bid, curr_bid_quant, curr_best_ask, curr_ask_quant))

def main():
    #uncomment for debugging 
    #websocket.enableTrace(True)

    #WebSocket settings
    ws = websocket.WebSocketApp("wss://api.gemini.com/v1/marketdata/BTCUSD",
    on_message = on_message,
    on_error = on_error,
    on_close = on_close)
    
    #Open connection to websocket
    ws.run_forever()

if __name__ == '__main__':
    main()
