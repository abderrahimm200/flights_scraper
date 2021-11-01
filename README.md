# flights_scraper
this is my flights scraper script

# Getting started
## Installation
you will need to install Selenium and bs4 using pip as follows:
```
pip install Selenium
```
```
pip install bs4
```
# How to use it?
first you need to insert trip informations (date, destination ...)
here is an example:
```
trip['from']="barcelona"  #Departure city
trip['to']='londres'  #Arrival city
trip["depart"]="20/10/2021"  #Departure date
trip['return']="30/10/2021"  #Arrival date
```
then run the file and check the csv file created in the same directory as the script
