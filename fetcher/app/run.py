#!/usr/bin/env python3

from models.tables import Base, Spots, Summary, Dashboard, Users
from models import engine, db
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime
import schedule
from exchanges.Binance import Binance
from config import DEFAULT_EPOCH, PAIRS, STABLE_COIN
import time

def create_db(engine):
    create_database(engine.url)

def update_summary(session, client, pair):
    coin, base = pair
    current_price = client.get_current_price()
    if (session.query(Summary).filter(Summary.coin == coin).count() == 0):
        # Create new Summary
        summary = Summary(
            coin,
            0,
            0,
            0,
            current_price
        )
    else:
        # Update Summary
        summary = session.query(Summary).filter(Summary.coin == coin).first()
        summary.current_price = current_price
        summary.change = current_price * summary.qty - summary.cost
    
    session.add(summary)
    session.commit()

def update_summary_by_tx(session, client, pair, tx):
    """Update summary table by new fetched transaction data

    Args:
        session (Object): DB session
        client (Object): Client of exchanges
        pair (List): List of coin pairs
        tx (List): List of transactions
    """
    coin, base = pair
    if (base in STABLE_COIN):
        buy_price = 1
    else:
        buy_price = client.get_history_price(f"{base}USDT", tx["time"])
    current_price = client.get_current_price(f"{coin}USDT")
    commission = float(tx["commission"]) * float(tx["price"]) * buy_price
    new_amount = float(tx["qty"])
    new_uamount = buy_price * float(tx["quoteQty"])
    new_cost = new_uamount / new_amount
    if session.query(Summary).filter(Summary.coin==coin).count() == 0:
        # Create new Summary
        change = current_price * new_amount - new_uamount
        summary = Summary(
            coin,
            change,
            new_cost,
            new_amount,
            new_uamount,
            current_price
        )
        session.add(summary)
        session.commit()
    else:
        # Update Summary
        if tx["isBuyer"]:
            summary = session.query(Summary).filter(Summary.coin == coin).first()
            change = current_price * (summary.amount + new_amount) - (summary.uamount + new_uamount)
            summary.amount += new_amount
            summary.uamount += new_uamount
            summary.change = change
        else:
            summary = session.query(Summary).filter(Summary.coin == coin).order_by(Summary.id.desc()).first()
            change = current_price * (summary.amount - new_amount) - (summary.uamount - new_uamount)
            summary.amount -= new_amount 
            summary.uamount -= new_uamount
            summary.change = change

        # Check if coin sold out
        if (summary.amount <= 0.00001 or summary.uamount <= 0.1):
            summary.uamount = 0
            summary.cost = 0
            summary.change = 0
        else:
            summary.cost = new_cost
            

        session.commit()

def update_summary_by_current_price(session, client, pairs):
    for i in pairs:
        coin_summary = session.query(Summary).filter(Summary.coin==i[0]).first()
        if coin_summary:
            current_price = client.get_current_price(f"{i[0]}USDT")
            coin_summary.change = current_price * coin_summary.amount - coin_summary.uamount
            coin_summary.current_price = current_price
            session.commit()



def update_dashboard_by_summary(session, client, pairs):
    """Update dashboard by Summary
    Due to exchanges rate limit mechanism, the dashboard table will start record only from the day you start this service.

    Args:
        session (Object): DB session
    """
    change_sum = 0
    for i in pairs:
        coin_summary = session.query(Summary).filter(Summary.coin==i[0]).first()
        if coin_summary:
            current_price = client.get_current_price(f"{i[0]}USDT")
            change_sum += current_price * coin_summary.amount - coin_summary.uamount
    # Create coin's dashboard
    dashboard = Dashboard(change_sum)
    session.add(dashboard)
    session.commit()


def update_spot_by_tx(session, pair, tx):
    if tx["isBuyer"]:
        tx_type = True
    else:
        tx_type = False
    spot = Spots(
        pair[0],
        pair[1],
        float(tx["qty"]),
        float(tx["quoteQty"]),
        float(tx["commission"]),
        tx["commissionAsset"],
        tx_type,
        float(tx["price"]),
        datetime.fromtimestamp(int(tx["time"]) // 1000)
    )
    session.add(spot)
    session.commit()

def fetch_binance_data(api_key, api_secret):
    client = Binance(api_key, api_secret)
    session = db()
    for i in PAIRS:
        if (session.query(Spots).filter(Spots.coin==i[0], Spots.base==i[1]).count() == 0):
            tx_history = client.get_tx_history(''.join(i), limit=1000, startTime=DEFAULT_EPOCH)
        else:
            last_update = session.query(Spots).filter(Spots.coin==i[0], Spots.base==i[1]).order_by(Spots.id.desc()).first().trade_time.timestamp()
            tx_history = client.get_tx_history(''.join(i), limit=1000, startTime=int((last_update+1)*1000))
        if tx_history:
            for j in tx_history:
                update_spot_by_tx(session, i, j)
                update_summary_by_tx(session, client, i, j)
    update_summary_by_current_price(session, client, PAIRS)
    update_dashboard_by_summary(session, client, PAIRS)

def binance_wrapper():
    print("[+] Fetching data from Binance")
    try:
        user_count = session.query(Users).count()
        if (user_count == 1):
            user = session.query(Users).first()
            fetch_binance_data(user.api_key, user.api_secret)
    except: # Bad practice, but it works :p
        pass



if __name__ == '__main__':
    session = db()
    schedule.every(10).minutes.do(binance_wrapper)
    while True:
        schedule.run_pending()
        time.sleep(5)
