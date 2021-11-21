#!/usr/bin/env python3

from flask import Blueprint, jsonify
from app.models.tables import Summary, Spots, Dashboard
from flask_jwt_extended import jwt_required
from datetime import timedelta



api = Blueprint("service", __name__)


@api.route("/dashboard")
@jwt_required()
def dashboard():
    dashboard_count = Dashboard.query.count()
    if (dashboard_count > 10):
        dashboard = [Dashboard.query.get(round(1+x*(dashboard_count-1)/10)) for x in range(10)] 
    else:
        dashboard = Dashboard.query.all()
    if dashboard:
        tmp = []
        for i in dashboard:
            update_time = i.update_time + timedelta(hours=8)
            tmp.append({
                "change": i.change,
                "update_time": update_time.timestamp()*1000
            })
        return jsonify({
            "status": True,
            "data": tmp
        })
    else:
        return jsonify({
            "status": False,
            "msg": "Error while querying dashboard data."
        })

@api.route('/spots/<string:coin>')
@jwt_required()
def spots(coin):
    coin = coin.upper()
    spots = Spots.query.filter_by(coin=coin).order_by(Spots.trade_time.desc()).all()
    if spots:
        tmp = []
        for i in spots:
            tmp.append({
                "coin": i.coin,
                "base": i.base,
                "amount": i.amount,
                "uamount": i.uamount,
                "commission": i.commission,
                "commission_type": i.commission_type,
                "tx_type": i.tx_type,
                "buy_price": i.buy_price,
                "trade_time": i.trade_time.strftime("%Y/%m/%d - %H:%M:%S")
            })
        return jsonify({
            "status": True,
            "data": tmp
        })
    else:
        return jsonify({
            "status": False,
            "msg": "Error while querying spots data."
        })

@api.route('/summary')
@api.route('/summary/<string:coin>')
@jwt_required()
def summary(coin=""):
    if coin:
        summaries = Summary.query.filter_by(coin=coin).first()
        return jsonify({
            "status": True,
            "data": {
                "coin": summaries.coin,
                "change": summaries.change,
                "cost": summaries.cost,
                "current_cost": round(summaries.amount*summaries.current_price, 5), # prevent weird floating point problem :/
                "amount": summaries.amount,
                "uamount": summaries.uamount,
                "current_price": summaries.current_price
            }
        })
    else:
        summaries = Summary.query.all()
        if summaries:
            tmp = []
            for i in summaries:
                tmp.append({
                    "coin": i.coin,
                    "change": i.change,
                    "cost": i.cost,
                    "current_cost": round(i.amount*i.current_price, 5), # prevent weird floating point problem :/
                    "amount": i.amount,
                    "uamount": i.uamount,
                    "current_price": i.current_price
                })
            sorted_summary = sorted(tmp, key=lambda x: x["uamount"], reverse=True)
            return jsonify({
                "status": True,
                "data": sorted_summary
            })
        else:
            return jsonify({
                "status": False,
                "msg": "Error while querying summary data."
            })
