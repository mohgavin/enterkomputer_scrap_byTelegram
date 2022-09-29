#!/home/nivag/.WebScrapping/bin/python

from selenium import webdriver
from selenium.webdriver.common.by import By
import dataframe_image as dfi
import pandas as pd
import re
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument("--window-size=1280, 1280")
chrome_options.add_argument("--disable-dev-shm-usage")

wd = webdriver.Chrome('chromedriver', options=chrome_options)
SCROLL_PAUSE_TIME = 6

# Get scroll height
def scroll_down():

    last_height = wd.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = wd.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height

def loading_website(sites):
    sites = wd.get(sites)
    scroll_down()
    return(wd.find_elements(By.CLASS_NAME, 'ps-product__container'))

def regex1(elem):
    list1 = []
    for i in range(len(elem)):
        if re.search("RTX", elem[i].text) and re.search("(3060|2060)", elem[i].text) :
            list1.append(elem[i].text)
    return(list1)

def regex2(elem):
    list2 = []
    for i in range(len(elem)):
        if re.search(".", elem[i].text):
            list2.append(elem[i].text)
        else:
            pass
    return(list2)

def table_process1(list, pic_location, csv_location):
    df = pd.DataFrame(list)
    df = df[0].str.split(pat='\n', expand=True, regex=None)
    df.rename(columns = {df.columns[0]:'Hardware', df.columns[1]:'Serial Number', df.columns[2]:'Current Price - Today', df.columns[3]:'Delta'}, inplace = True)
    df['Current Price - Today'].replace('(Rp|\.)', '', regex=True, inplace=True)
    df['Current Price - Today'] = df['Current Price - Today'].astype(str).astype(int)
    df.sort_values(by=['Current Price - Today'], inplace=True)

    pd.set_option('display.max_colwidth', 0)
    df.drop(df[df['Serial Number'].str.contains('Ready')].index, inplace=True)
    df.drop(['Delta'], axis=1, inplace=True)
    df_yesterday = pd.read_csv(csv_location)

    #VLOOKUP FUNCTION - LEFT ACTION 
    df = pd.merge(df, df_yesterday[['Serial Number', f'Current Price - Yesterday']], on='Serial Number', how='left')   
    df['Delta'] = df['Current Price - Today'] - df['Current Price - Yesterday']
    dfi.export(df, pic_location)
    df.drop(['Current Price - Yesterday', 'Delta'], axis=1, inplace=True)
    df.rename(columns={"Current Price - Today" : f'Current Price - Yesterday'}, inplace = True)
    df.to_csv(csv_location, index=False)

def table_process2(list, pic_location, csv_location):
    df = pd.DataFrame(list)
    df = df[0].str.split(pat='\n', expand=True, regex=None)
    df.rename(columns = {df.columns[0]:'Hardware', df.columns[1]:'Serial Number', df.columns[2]:'Current Price - Today', df.columns[3]:'Delta_From Site'}, inplace = True)
    df['Current Price - Today'].replace('(Rp|\.)', '', regex=True, inplace=True)
    df['Delta_From Site'].replace('(Rp|\.)', '', regex=True, inplace=True)
    #df['Current Price - Today'] = df['Current Price - Today'].astype(str).astype(int)
    df['Delta_From Site'] = df['Delta_From Site'].astype(str, errors='ignore').astype(int, errors='ignore')
    df.sort_values(by=['Delta_From Site'], inplace=True, ascending=False)

    pd.set_option('display.max_colwidth', 0)
    df.drop(df[df['Serial Number'].str.contains('Ready')].index, inplace=True)
    df.drop(df[df['Current Price - Today'].str.contains('[a-zA-Z]')].index, inplace=True)
    df_yesterday = pd.read_csv(csv_location)

    #VLOOKUP FUNCTION - LEFT ACTION 
    df = pd.merge(df, df_yesterday[['Serial Number', f'Current Price - Yesterday']], on='Serial Number', how='left')   
    #df['Delta'] = df['Current Price - Today'] - df['Current Price - Yesterday']
    dfi.export(df.iloc[:50], pic_location, max_rows=50)
    df.drop(['Current Price - Yesterday'], axis=1, inplace=True)
    df.rename(columns={"Current Price - Today" : f'Current Price - Yesterday'}, inplace = True)
    df.to_csv(csv_location, index=False)
