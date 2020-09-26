import praw
import config
import os
import yfinance as yf
import datetime
import time


keyphrase = "pls_gv_stock "


def botLogin():
    print("Logging in...")
    r = praw.Reddit(username=os.environ.get("redditBot_ID"),
                    password=os.environ.get("redditBot_pass"),
                    client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent=config.user_agent
                    )
    print("Logged in...")
    return r


def reply(tickerSymbol):
    tickerData = yf.Ticker(tickerSymbol)
    tickerInfo = tickerData.info
    investment = tickerInfo["shortName"]
    today = datetime.datetime.today().isoformat()
    Open = tickerInfo["open"]
    High = tickerInfo["dayHigh"]
    Low = tickerInfo["dayLow"]
    MktCap = tickerInfo["marketCap"]
    PrevClose = tickerInfo["previousClose"]
    fiftyTwoHigh = tickerInfo["fiftyTwoWeekHigh"]
    fiftyTwoLow = tickerInfo["fiftyTwoWeekLow"]
    Currency = tickerInfo["currency"]
    regularMarketPrice = tickerInfo["regularMarketPrice"]
    Type = tickerInfo["sector"]
    replyString = ("Company Name : "+investment + "\nDate-Time : "+today+"\nType : "+Type+"\nFigures in : "+Currency+"\nOpen : "+str(Open) + "   High : "+str(High) + "   Low : "+str(Low)+"\nPrevious-Close : "+str(PrevClose) + "\nRegular Market Price : "+str(regularMarketPrice) +
                   "\nMarket-Capital : "+str(MktCap)+"\n52-wk-high : "+str(fiftyTwoHigh)+"\n52-wk-low : "+str(fiftyTwoLow))
    return replyString


def runBot(r):
    print("Obtaining 25 comments...")
    subreddit = r.subreddit("testBot2704")
    for comment in subreddit.comments(limit=25):
        if keyphrase in comment.body:
            tickerSymbol = comment.body.replace(keyphrase, "")
            try:
                reply = reply(tickerSymbol)
                comment.reply(reply)
                print("Posted")
            except:
                print("Not Posted.....Too frequent")

    time.sleep(10)


while True:
    r = botLogin()
    runBot(r)
