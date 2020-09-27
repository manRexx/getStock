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
                    client_id="DR18zicVBiDXcQ",
                    client_secret="QJwZCpL9uMgrqTsInfnMtIYI1pw",
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

    comments_replied_to = []

    subreddit = r.subreddit("testBot2704")
    for comment in subreddit.comments(limit=15):
        if keyphrase in comment.body and comment.id not in comments_replied_to:
            print("1")
            tickerSymbol = comment.body.replace(keyphrase, "")
            print("2")
            answer = reply(tickerSymbol)
            print("3")
            comment.reply(answer)
            print("Posted")

            comments_replied_to.append(comment.id)

    print(comments_replied_to)

    time.sleep(10)


r = botLogin()

while True:
    runBot(r)
