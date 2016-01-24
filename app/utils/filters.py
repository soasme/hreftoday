# -*- coding: utf-8 -*-

def datetimeformat(value, format="%Y-%m-%d %H:%I:%S"):
    return value.strftime(format)

def dateformat(value):
    return datetimeformat(value, "%Y/%m/%d")

FILTERS = globals()
