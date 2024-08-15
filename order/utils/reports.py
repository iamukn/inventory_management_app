#!/usr/bin/python3
from order.models import Orders
from order.serializer import OrderSerializer
from datetime import datetime, timedelta

"""
    Retrieves daily, weekly and monthly order reports
"""

def dailyReports() -> dict:
    
    # retrieves orders for today
    today = datetime.today()
    orders  = Orders.objects.filter(date_of_purchase=today)

    # serialize the data
    serializer = OrderSerializer(orders, many=True)
    reports = {"daily_report":{
        "date": today.strftime("%Y/%m/%d"),
        "total_orders": len(serializer.data),
        "total_revenue": sum([price.get('total') for price in serializer.data]),
        "orders": serializer.data
        }}
    return reports


def weeklyReports() -> dict:
    # generates weekly repots for orders
    
    today = datetime.today()
    last_week = today - timedelta(weeks=1)
    # retrieves orders for last week
    orders  = Orders.objects.filter(date_of_purchase__range=(last_week, today))

    # serialize the data
    serializer = OrderSerializer(orders, many=True)
    reports = {"weekly_report":{
        "week_start": last_week.strftime('%Y/%m/%d'),
        "week_end": today.strftime('%Y/%m/%d'),
        "total_orders": len(serializer.data),
        "total_revenue": sum([price.get('total') for price in serializer.data]),
        "orders": serializer.data
        }}

    return reports

def monthlyReports() -> dict:
    # generates monthly repots for orders
    today = datetime.today()
    last_month = today - timedelta(weeks=4)
    # retrieves orders for last month
    orders  = Orders.objects.filter(date_of_purchase__range=(last_month, today))
    # serialize the data
    serializer = OrderSerializer(orders, many=True)
    reports = {"monthly_report":{
        "month_start": last_month.strftime('%Y/%m/%d'),
        "month_end": today.strftime('%Y/%m/%d'),
        "total_orders": len(serializer.data),
        "total_revenue": sum([price.get('total') for price in serializer.data]),
        "orders": serializer.data
        }}

    return reports
