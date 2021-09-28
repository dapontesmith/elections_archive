# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 20:34:47 2021

@author: dapon
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
url = "https://elections2019.belgium.be/en/results-figures?el=CK&id=CKR00000"
r = requests.get(url, verify = False)
soup = BeautifulSoup(r.text, "html.parser")
options = soup.find_all("option")
constit_links = []
for option in options:
    constit_links.append(option["value"])
#remove the unneccessary links 
constit_links = constit_links[3:]

url_prefix = "https://elections2019.belgium.be"
district_links = []#link = constit_links[0]

#get all the links of districts 
for link in constit_links: 
    url = url_prefix + link 
    r = requests.get(url, verify = False)
    soup = BeautifulSoup(r.text, "html.parser")
    district_options = soup.find_all("option")
    for option in district_options:
        district_links.append(option["value"])
    #district_links = [i for i in district_links if i]
    #district_links = district_links[2:]
    sleep(5)
district_links = [i for i in district_links if i]
district_links = district_links[1:]



def get_muni_links(start_num, end_num):
    muni_links = []
    url_prefix = "https://elections2019.belgium.be"
    for suffix in district_links[start_num : end_num]:
        if "999" not in suffix and "0000" not in suffix:
            print(suffix)
            link = url_prefix + suffix
            r = requests.get(link, verify = False)
            soup = BeautifulSoup(r.text, "html.parser")
            divs = soup.findAll("div", attrs = {"class" : "evolution-graphs"})
            main_link = []
            for div in divs:
                for a in div: 
                    if a.get("href") != None: 
                        main_link.append(url_prefix + a.get("href"))
            r = requests.get(main_link[0], verify = False)
            soup = BeautifulSoup(r.text, "html.parser")
            options = soup.findAll("select", attrs = {"id" : "navigation1"})
            for option in options:
                htmls = (option.find_all("option"))
                for html in htmls:
                    muni_links.append(html["value"])
    muni_links_unique = []
    for x in range(len(muni_links)):
        print(x)
        if "CKX" in muni_links[x]:
            muni_links_unique.append(muni_links[x])
    sleep(5)
    return muni_links_unique


################################
    #GET muniicpal links in separate lists
    #i do this to avoid getting SSL errors when I run the scraping
    

muni_links_full1 = []
muni_links_full1.append(get_muni_links(0, 11))
muni_links_full2 = []
muni_links_full2.append(get_muni_links(11, 25))
muni_links_full3 = []
muni_links_full3.append(get_muni_links(25, 38))
muni_links_full4 = []
muni_links_full4.append(get_muni_links(38, 50))
muni_links_full5 = []
muni_links_full5.append(get_muni_links(50, 65))
muni_links_full6 = []
muni_links_full6.append(get_muni_links(65, 80))
muni_links_full7 = []
muni_links_full7.append(get_muni_links(80, 95))
muni_links_full8 = []
muni_links_full8.append(get_muni_links(95, 110))
muni_links_full9 = []
muni_links_full9.append(get_muni_links(110, 125))
muni_links_full10 = []
muni_links_full10.append(get_muni_links(125, 140))
muni_links_full11 = []
muni_links_full11.append(get_muni_links(140, 155))
muni_links_full12 = []
muni_links_full12.append(get_muni_links(155, 176))

#combine all the link lists into one link

flat_list1 =[item for sublist in muni_links_full1 for item in sublist]
flat_list2 =[item for sublist in muni_links_full2 for item in sublist]
flat_list3 =[item for sublist in muni_links_full3 for item in sublist]
flat_list4 =[item for sublist in muni_links_full4 for item in sublist]
flat_list5 =[item for sublist in muni_links_full5 for item in sublist]
flat_list6 =[item for sublist in muni_links_full6 for item in sublist]
flat_list7 =[item for sublist in muni_links_full7 for item in sublist]
flat_list8 =[item for sublist in muni_links_full8 for item in sublist]
flat_list9 =[item for sublist in muni_links_full9 for item in sublist]
flat_list10 =[item for sublist in muni_links_full10 for item in sublist]


####################
#get the urls out 
def get_urls(flat_url_list):
    muni_urls = []
    url_prefix = "https://elections2019.belgium.be"
    for link in flat_url_list:
        muni_urls.append(url_prefix + link)
    return muni_urls

#apply function to each of the url lists
muni_urls1 = get_urls(flat_list1)
muni_urls2 = get_urls(flat_list2)
muni_urls3 = get_urls(flat_list3)
muni_urls4 = get_urls(flat_list4)
muni_urls5 = get_urls(flat_list5)
muni_urls6 = get_urls(flat_list6)
muni_urls7 = get_urls(flat_list7)
muni_urls8 = get_urls(flat_list8)
muni_urls9 = get_urls(flat_list9)
muni_urls10 = get_urls(flat_list10)

#define function for getting results from municipal urls
def get_results(muni_urls_list):
    df_return = pd.DataFrame()
    for url in muni_urls_list:
        print(url)
        r = requests.get(url, verify = False)
        soup = BeautifulSoup(r.text, "html.parser")
        name_h2 = soup.findAll("h2", attrs = {"class" : "article-dataheader__title"})
        #get the name of the municipality
        for name in name_h2: 
            muni_name = name.text.strip()
        #use read_html function to read the results tables
        df = pd.read_html(url)[0]
        df["municipality"] = muni_name
        df_return = df_return.append(df)
        sleep(5)
    return df_return

results1 = get_results(muni_urls1)
results2 = get_results(muni_urls2)
results3 = get_results(muni_urls3)
results4 = get_results(muni_urls4)
results5 = get_results(muni_urls5)
results6 = get_results(muni_urls6)
results7 = get_results(muni_urls7)
results8 = get_results(muni_urls8)
results9 = get_results(muni_urls9)
results10 = get_results(muni_urls10)

muni_urls11 = muni_urls7[0:27]
muni_urls12 = muni_urls7[27:len(muni_urls7)+1] 
results11 = get_results(muni_urls11)
results12 = get_results(muni_urls12)


#now put them all together!
final = pd.concat([results1, results2, results3, results4, results5, 
                   results6, results8, results9, 
                   results10, results11, results12])

#get the relevant columns and write to csv
    
final = final[["Party","2019","2014","%2019","%2014","municipality"]] 
    
final.to_csv("C:/Users/dapon/Dropbox/Harvard/Noah_SunYoung/data/belgium/belgium_municipality_2014_2019.csv")

    

 

    