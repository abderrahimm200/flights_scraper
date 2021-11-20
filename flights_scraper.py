trip={}
trip['from']="barcelona"  #Departure city
trip['to']='londres'  #Arrival city
trip["depart"]="20/10/2021"  #Departure date
trip['return']="30/10/2021"  #Arrival date

from bs4 import BeautifulSoup
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from datetime import datetime

driver = webdriver.Chrome()

#skip selenium errors while searching for an element
def skip_erreur(element,type):
    while True:
        try:
            if type=="id":
                result=driver.find_element_by_id(element)
            elif type=="class":
                result=driver.find_element_by_css_selector(element)
            elif type=="classes":
                result=driver.find_elements_by_css_selector(element)
            elif type=="xpath":
                result=driver.find_element_by_xpath(element)
            elif type=="xpaths":
                result=driver.find_elements_by_xpath(element)
            elif type=="link_text":
                result=driver.find_element_by_link_text(element)
            elif type=="tag":
                result=driver.find_element_by_tag_name(element)
            return result
        except:
            pass

#research for the flight in google based on the deparature city and the destination
def from_to(origin,dest):
    driver.get(f'https://www.google.com/search?q=google+flights+from+{origin}+to+{dest}&hl=en')
    try: #skip cookies requirements
        skip=driver.find_element_by_id('L2AGLb')
        ActionChains(driver).click(skip).perform()
    except:
        pass

#convert date
def convert(date):
    new_date=datetime.strptime(date,"%d/%m/%Y")
    converted=new_date.strftime("%a, %d %b")
    return converted

#search for the available fights
def search_flight(trip):
    origin=trip["from"]
    dest=trip["to"]
    from_to(origin,dest)
    soup=BeautifulSoup(driver.page_source, 'html.parser')
    results=skip_erreur(".MXl0lf.tKtwEb.wHYlTd","class")
    ActionChains(driver).click(results).perform()
    main=skip_erreur(".icWGef.A84apb.P0ukfb.bgJkKe.BtDLie","class")
    inputs=main.find_elements_by_tag_name("input")
    inputs[0].send_keys(Keys.CONTROL, 'a')
    depart=convert(trip["depart"])
    inputs[0].send_keys(depart)
    inputs[0].send_keys(Keys.ENTER)
    time.sleep(1)
    inputs[1].send_keys(Keys.CONTROL, 'a')
    return_=convert(trip['return'])
    inputs[1].send_keys(return_)
    inputs[1].send_keys(Keys.ENTER)

#get data from the website and clean it
def scrap_data():
    others=skip_erreur(".zISZ5c.QB2Jof","class")
    if "more flights" in others.text:
        try:
            ActionChains(driver).click(others).perform()
        except:
            pass
        time.sleep(5)
    html=driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    all_el="mxvQLc ceis6c uj4xv uVdL1c A8qKrc"
    classes = soup.find_all(class_=all_el) #select divs that contains flights data
    vols=[]
    for data in classes:
        company=data.find("div",class_="TQqf0e sSHqwe tPgKwe ogfYpf").span.get_text()
        if not "Separate" in company:
            p=data.find("div",class_="BVAVmf I11szd POX3ye").find_all("span")[-1]
            price=p.get_text()
            escale=data.find("div",class_="EfT7Ae AdWm1c tPgKwe").span.get_text()
            time_=data.find("div",class_="zxVSec YMlIz tPgKwe ogfYpf").span.find_all(attrs={"role": "text"})
            time1=time_[0].get_text()
            time2=time_[1].get_text()
            duree=data.find("div",class_="gvkrdb AdWm1c tPgKwe ogfYpf").get_text()
            li=[company,time1,time2,duree,escale,price]
            vols.append(li)
    return vols
  
#create csv file and fil it with data 
def csv_data(data,trip):
    origin=trip["from"]
    dest=trip["to"]
    titles=['company','depart time',"arrival time","duration","num of stops","price"]
    data=[titles]+data
    with open(f'{origin}_{dest}.csv','w',newline='') as f:
        writer=csv.writer(f)
        for row in data:
            writer.writerow(row)
    f.close
search_flight(trip)
data=scrap_data()
csv_data(data,trip)
driver.close()
