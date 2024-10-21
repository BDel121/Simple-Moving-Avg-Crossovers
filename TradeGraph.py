import pandas as pd
import requests
import json
import time
import math
import plotly.graph_objects as go

# api keys 
    # The fmpapi key is "DEMO" this key has been replaced by a demo key 
    # to obtaian your own free key for this model go to https://site.financialmodelingprep.com/developer/docs/ and create an account 


api_key = "DEMO"


def stock_div_call(stock):
    stock_div = requests.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/stock_dividend/{stock}?apikey={api_key}').json()
    sdiv = stock_div['historical'][0]['dividend']
    return sdiv
    
def indicator_list(stock):
    # basic call for getting all simple moving average values 
    stock_sma = requests.get(f'https://financialmodelingprep.com/api/v3/technical_indicator/1day/{stock}?type=sma&period=10&apikey={api_key}').json()
    ssma = stock_sma[0]['sma']

    test_sma=[]
    # record of simple moving averages
    for n in stock_sma:
        S_sma= n['sma']
        test_sma.append(S_sma)
    
    # return test_sma
    moving_avg(test_sma,stock)

def ma_sort(test_sma,length):
    window_size = length
 
    i = 0
    # Initialize an empty list to store moving averages
    moving_averages = []
    
    # Loop through the array to consider
    # every window of size 3
    while i < len(test_sma) - window_size + 1:
    
        # Store elements from i to i+window_size
        # in list to get the current window
        window = test_sma[i : i + window_size]
    
        # Calculate the average of current window
        window_average = round(sum(window) / window_size, 2)
        
        # Store the average of current
        # window in moving average list
        moving_averages.append(window_average)
        
        # Shift window to right by one position
        i += 1

    # return the a variable of sorted 
    return moving_averages

def moving_avg(test_sma,stock):
    
    ten_sma,ten_pos_band,ten_neg_band = moving_avg_ten(test_sma)

    month_sma,month_pos_band,month_neg_band = moving_avg_month(test_sma)

    half_sma,half_pos_band,half_neg_band = moving_avg_half_year(test_sma)

    year_sma,year_pos_band,year_neg_band = moving_avg_year(test_sma)

    list_length=number_list(year_sma)
    trade_graph(list_length,year_sma,year_pos_band,year_neg_band,half_sma,half_pos_band,
                half_neg_band,month_sma,month_pos_band,month_neg_band,ten_sma,ten_pos_band,ten_neg_band,stock)
  

def moving_avg_ten(test_sma):
    # ten_avg_sma = []
    sma = ma_sort(test_sma,10)
    pos_band = []
    neg_band = []
    for n in sma:
        ten_band_form = math.sqrt(n)
        pos = n + ten_band_form * 2
        pos_band.append(pos)
        neg = n - ten_band_form * 2
        neg_band.append(neg)
    print("Ten:","sma: $",sma[0],"pos: $",pos_band[0],"neg: $",neg_band[0])
    return sma, pos_band, neg_band

def moving_avg_month(test_sma):
    # ten_avg_sma = []
    sma = ma_sort(test_sma,30)
    pos_band = []
    neg_band = []
    for n in sma:
        ten_band_form = math.sqrt(n)
        pos = n + ten_band_form * 2
        pos_band.append(pos)
        neg = n - ten_band_form * 2
        neg_band.append(neg)
    print("Month:","sma: $",sma[0],"pos: $",pos_band[0],"neg: $",neg_band[0])
    return sma, pos_band, neg_band

def moving_avg_half_year(test_sma):
    # ten_avg_sma = []
    sma = ma_sort(test_sma,180)
    pos_band = []
    neg_band = []
    for n in sma:
        ten_band_form = math.sqrt(n)
        pos = n + ten_band_form * 2
        pos_band.append(pos)
        neg = n - ten_band_form * 2
        neg_band.append(neg)
    print("Half Year:","sma: $",sma[0],"pos: $",pos_band[0],"neg: $",neg_band[0])
    return sma, pos_band, neg_band

def moving_avg_year(test_sma):
    # ten_avg_sma = []
    sma = ma_sort(test_sma,360)
    pos_band = []
    neg_band = []
    for n in sma:
        ten_band_form = math.sqrt(n)
        pos = n + ten_band_form * 2
        pos_band.append(pos)
        neg = n - ten_band_form * 2
        neg_band.append(neg)
    print("Year:","sma: $",sma[0],"pos: $",pos_band[0],"neg: $",neg_band[0])
    return sma, pos_band, neg_band
    
def number_list(nml):

    number=len(nml)
    list_length = []
    a = 0
    while a < number + 1:
        a = a +1
        list_length.append(a)
    return list_length

def trade_graph(list_length,year_sma,year_pos_band,year_neg_band,half_sma,half_pos_band,
                half_neg_band,month_sma,month_pos_band,month_neg_band,ten_sma,ten_pos_band,ten_neg_band,stock):
    # Add data
    month = list_length
    basic = year_sma
    High = year_pos_band
    Low = year_neg_band
    basicH = half_sma
    HighH = half_pos_band
    LowH = half_neg_band
    basicM = month_sma
    HighM = month_pos_band
    LowM = month_neg_band
    basicT = ten_sma
    HighT = ten_pos_band
    LowT = ten_neg_band

    timescale = len(list_length)
    timescale = timescale/360
    timescale = round(timescale, 4)
    fig = go.Figure()
    # Create and style traces
    fig.add_trace(go.Scatter(x=month, y=basic, name='SMA',
                            line=dict(color='Blue', width=4)))
    fig.add_trace(go.Scatter(x=month, y=High, name = 'High Band',
                            line=dict(color='Blue', width=4, dash='dashdot')))
    fig.add_trace(go.Scatter(x=month, y=Low, name='Low Band',
                            line=dict(color='Blue', width=4,
                                dash='dashdot') # dash options include 'dash', 'dot', and 'dashdot'
    ))


    fig.add_trace(go.Scatter(x=month, y=basicH, name='Half Year SMA',
                            line=dict(color='Green', width=4)))
    fig.add_trace(go.Scatter(x=month, y=HighH, name = 'High Band',
                            line=dict(color='Green', width=4,dash='dash')))
    fig.add_trace(go.Scatter(x=month, y=LowH, name='Low Band',
                            line=dict(color='Green', width=4,
                                dash='dash')))

    fig.add_trace(go.Scatter(x=month, y=basicM, name='Month SMA',
                            line=dict(color='Red', width=4)))
    fig.add_trace(go.Scatter(x=month, y=HighM, name = 'High Band',
                            line=dict(color='Red', width=4, dash='dashdot')))
    fig.add_trace(go.Scatter(x=month, y=LowM, name='Low Band',
                            line=dict(color='Red', width=4,
                                dash='dashdot')))
    fig.add_trace(go.Scatter(x=month, y=basicT, name='Ten SMA',
                            line=dict(color='Red', width=4)))
    fig.add_trace(go.Scatter(x=month, y=HighT, name = 'High Band',
                            line=dict(color='Red', width=4, dash='dashdot')))
    fig.add_trace(go.Scatter(x=month, y=LowT, name='Low Band',
                            line=dict(color='Red', width=4,
                                dash='dashdot')))

    # Edit the layout
    fig.update_layout(title= f"{stock} stock Test Table, {timescale} Years",
                    xaxis_title='Days Time Periods',
                    yaxis_title='Price')
    fig['layout']['xaxis']['autorange'] = "reversed"


    fig.show()
def text_check():
    stock = input("Enter Stock Symbol:")
    
    if stock == "":
        stock = input("Enter Stock Symbol:")
    else:
        stock = stock.upper()
        return stock

wt = True

while wt==True:
    print("Run: Y or N")
    ask = input(":")
    ask = ask.upper()
    if ask == "Y" or ask == "YES":
        stock = text_check()
        stock_div_call(stock)
        indicator_list(stock)
    elif ask == "N" or ask == "NO":    
        wt = False
    else:
        ask = input("Try again Y or N:")
        ask = ask.upper()
