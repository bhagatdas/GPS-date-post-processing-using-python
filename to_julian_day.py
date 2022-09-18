#Civil date to GPS week and Seconds of week
import pandas as pd
import math as mt
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
DATA_PATH = os.path.join(BASE_DIR, 'Rinex_files/log_24h.15o')
DATA_PATH = DATA_PATH.replace(os.sep, '/')


def date_extraction():
    date=[]

    fid=open(DATA_PATH,"rt")
    while True:   #to find TIme of first obs in RINEX file
        line=fid.readline()
        if "TIME OF FIRST OBS" in line:
            break
    print(line)
    date=list(line.strip().split())

    year=int(date[0])
    month=int(date[1])
    day=int(date[2])
    hour=int(date[3])
    minute=int(date[4])
    second=mt.floor(float(date[5]))

    date.clear()
    date = [year, month, day, hour, minute , second]
    return date

def using_inbuid_fun(date):
    ts = pd.Timestamp(date[0], date[1], date[2],date[3], date[4], date[5])
    print("IB-Civil Date:",ts)
    julday=float(ts.to_julian_date()) 
    print("IB-Julian day:",int(julday))

def using_userdef_fun(date):
    y,m,d,h,m,s = date[0], date[1], date[2],date[3], date[4], date[5]

    h=h+(m/60)+(s/3600)

    if m <= 2:
        y = y-1
        m = m+12
        
    julday = mt.floor(365.25*(y+4716))  +mt.floor(30.6001*(m+1))+d+h/24-1537.5;
    print("Julian day:",int(julday))

    week = mt.floor((julday-2444244.5)/7)  #0 January 1980 UTC = JD 2,444,244.5)
    remain_week=((julday-2444244.5)/7)-week   # JD starts from noon
    print("Remain week",remain_week)
    week=week%1024
    print("GPS week:",week)                  #GPS time rollover 1024/52=19.7 years 

    sec_of_week=remain_week*7*24*60*60
    print("second of week",int(sec_of_week))

def main():
    date = date_extraction()
    using_inbuid_fun(date)
    print()
    using_userdef_fun(date)

if __name__ == "__main__":
    main()