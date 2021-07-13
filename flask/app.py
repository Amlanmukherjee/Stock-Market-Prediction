"""
AUTHOR: TISL Kolkata_Cronox

Team Members:
PRATTAY CHAKRABARTY
SREYAM DEY
AMLAN MUKHERJEE

"""
import pandas as pd
import numpy as np
import pandas_datareader.data as web
from fbprophet import Prophet
import datetime
from flask import Flask, render_template
from flask import request, redirect
from pathlib import Path
import os
import os.path
import csv
from itertools import zip_longest

app = Flask(__name__)

@app.after_request
def add_header(response):
    """
    add headers to force latest IE rendering engine and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response
    
@app.route("/")
def first_page():
    
    tmp = Path("static/back.png")
    tmp_csv = Path("static/record.csv")
    if tmp.is_file():
        os.remove(tmp)
    if tmp_csv.is_file():
        os.remove(tmp_csv)
    return render_template("index.html")

#function to retrieve data from yahoo finance
def yahoo_stocks(symbol, start, end):
    return web.DataReader(symbol, 'yahoo', start, end)

def get_historical_stock_price(stock):
    print ("Getting-past-stock-prices-for-stock", stock)
    
    #get 10 years stock data for NSE companies.
    startDate = datetime.datetime(2010, 1, 4)
    date = datetime.datetime.now().date()
    endDate = pd.to_datetime(date)
    stockData = yahoo_stocks(stock, startDate, endDate)
    return stockData

@app.route("/plot" , methods = ['POST', 'GET'] )
def main():
    if request.method == 'POST':
        stock = request.form['companyname']
        df_whole = get_historical_stock_price(stock)

        df = df_whole.filter(['Close'])
        
        df['ds'] = df.index
        #log transform the ‘Close’ variable.
        df['y'] = np.log(df['Close'])
        real_end = df['Close'][-1]
        
        model = Prophet()
        model.fit(df)

        num_days = 10
        future = model.make_future_dataframe(periods=num_days)
        predict = model.predict(future)
        
        print (predict[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
        
        #vizualization
        df.set_index('ds', inplace=True)
        predict.set_index('ds', inplace=True)
        
        #predict
        visual_df = df.join(predict[['yhat', 'yhat_lower','yhat_upper']], how = 'outer')
        visual_df['yhat_scaled'] = np.exp(visual_df['yhat'])

        close_data = visual_df.Close
        predicted_data = visual_df.yhat_scaled
        date = future['ds']
        #start predicting
        predict_start = predicted_data[-num_days]

        d = [date, close_data, predicted_data]
        export_data = zip_longest(*d, fillvalue = '')
        with open('static/record.csv', 'w', encoding="ISO-8859-1", newline='') as myfile:
            wr = csv.writer(myfile)
            wr.writerow(("DATE", "ACTUAL", "FORECASTED"))
            wr.writerows(export_data)
        myfile.close()

        return render_template("plot.html", real = round(real_end,2), predict = round(predict_start,2), stock_tinker = stock.upper())


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
