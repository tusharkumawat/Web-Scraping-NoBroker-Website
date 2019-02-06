from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import time
import random
import progressbar
import seaborn as sns
sns.set()

headers = ({'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})

# dataframe
titles = []
addresses = []
rents = []
sizes = []
deposits = []
furnishings = []
property_ages = []
available_fors = []
immediate_possessions = []

# progressbar for displaying % completion
bar = progressbar.ProgressBar(maxval=100)
bar.start()

# scraping through 1000 pages of nobroker website of places in Chennai
for page in range(100):
    bar.update(page+1)
    page += 1;
    link = "https://www.nobroker.in/property/rent/chennai/Chennai/?searchParam=W3sibGF0IjoxMy4wNDM3NjEyODI5MTkyLCJsb24iOjgwLjIwMDA2ODUxNjk2OTMsInNob3dNYXAiOmZhbHNlLCJwbGFjZUlkIjoiQ2hJSllUTjlULXBsVWpvUk05UmphQXVuWVc0IiwicGxhY2VOYW1lIjoiQ2hlbm5haSIsImNpdHkiOiJjaGVubmFpIn1d&sharedAccomodation=0&orderBy=nbRank,desc&radius=2&traffic=true&travelTime=30&propertyType=rent&pageNo="+str(page)

    response = get(link,headers=headers)

    # for testing if scraping of website is allowed...
    # print(response)
    # print(response.text[:1000])


    # Parsing through html page
    html_soup = BeautifulSoup(response.text,'html.parser')
    house_containers = html_soup.find_all('div', class_="card")
    if(house_containers != []):
        for container in house_containers:
            
            try:
                rent = container.find_all('h3')[2].find('span').text.replace(',','')
                rent = int(''.join(itertools.takewhile(str.isdigit,rent)))
                rents.append(int(rent))
            except:
                rents.append('-')
            try:
                size = int(container.find_all('h3')[0].find_all('span')[0].text.replace(',',''))
                sizes.append(int(size))
            except:
                sizes.append('-')
            try:
                deposit = int(container.find_all('h3')[1].find_all('span')[0].text.replace(',',''))
                deposits.append(int(deposit))
            except:
                deposits.append('-')
            title = (container.find('div','card-header-title').find('h2').text.replace('\n',''))
            address = (container.find('div','card-header-title').find('h5').text.replace('\n',''))
            titles.append(title)
            addresses.append(address)

            furnishing = (container.find('div','detail-summary').find_all('h5')[0].text.replace('\n',''))
            furnishings.append(furnishing)
    
            property_age = (container.find('div','detail-summary').find_all('h5')[1].text.replace('\n',''))
            property_ages.append(property_age)
    
            available_for = (container.find('div','detail-summary').find_all('h5')[2].text.replace('\n',''))
            available_fors.append(available_for)
    
            immediate_possession = (container.find('div','detail-summary').find_all('h5')[3].text.replace('\n',''))
            immediate_possessions.append(immediate_possession)
    else:
        break;

    time.sleep(random.randint(1,2))
bar.finish()
print("Successfully scraped {} pages containing {} properties.".format(page,len(titles)))


# creating dataframe to save data in .csv format
cols = ['Title', 'Address', 'Rent(Rs)', 'Deposit(Rs)', 'Size(Acres)', 'Furnishing', 'Property age', 'Available for', 'Immediate possession']

chennai = pd.DataFrame({'Title': titles,
                        'Address': addresses,
                        'Rent(Rs)': rents,
                        'Deposit(Rs)': deposits,
                        'Size(Acres)': sizes,
                        'Furnishing': furnishings,
                        'Property age': property_ages,
                        'Available for': available_fors,
                        'Immediate possession': immediate_possessions})[cols]
chennai.to_csv('chennai_rent.csv')
