from ua import generate_random_ua
from bs4 import BeautifulSoup
import requests
import json
import csv
import numpy as np 
import time



def get_url():
	'''prompts user for url input and returns url as string'''

	url = input('provide valid cars.com url: ')

	while 'cars.com' not in url:
		print('must be a cars.com search result url')

		url = input('provide valid cars.com url: ')

	return url



def generate_html(url):
	'''generates html as a string given the url to a website as input'''
 
	headers = {'user-agent': generate_random_ua()}

	source = requests.get(url, headers=headers).text

	return BeautifulSoup(source, 'lxml')



def run_scraper():
	'''scrapes cars.com url and writes data to a csv'''
	url = get_url()

	soup = generate_html(url)

	num_results = soup.find_all('script')[1].text 

	num_results = num_results[61:-2]

	num_results = json.loads(num_results)

	urls = []
	for page in range(2): #range(num_results['page']['search']['totalNumPages']-1):
		url = url[:url.find('page=')+5] + str(page+1) + url[url.find('page=')+6:]
		urls.append(url)


	outfile = open('cars.com_scraper.csv', 'w')
	csv_writer = csv.writer(outfile, lineterminator = '\n')
	csv_writer.writerow(['listing_id', 'name', 'price', 'mileage', 'ext_color', 'int_color', 'transmission', 'drivetrain', 'make', 'model', 
		                    'condition', 'year', 'trim', 'bodystyle', 'dealer', 'state', 'rating', 'review_count', 'CPO', 'price2', 'mileage2'
		                    ])

	for url in urls:

		soup = generate_html(url)

		script = soup.find_all('script')[1].text 

		script = script[61:-2]

		script = json.loads(script)

		iteration = 0

		for listing in soup.find_all('div', class_='listing-row__details'):
		    name = listing.h2.text
		    name = name.strip()
		    print(name)
		    
		    try:
		        price = listing.find('div', class_='payment-section')
		        price = price.find('span', class_='listing-row__price ').text
		        price = price.strip()
		    except:
		        price = None
		    print(price)
		    
		    try:
		        mileage = listing.find('div', class_='payment-section')
		        mileage = mileage.find('span', class_='listing-row__mileage').text
		        mileage = mileage.strip()
		    except:
		        mileage = None
		    print(mileage)
		    
		    
		    attribute = listing.find('ul', class_='listing-row__meta')
		    ext_color = attribute.find_all('li')[0].text
		    ext_color = ' '.join(ext_color.split())
		    int_color = attribute.find_all('li')[1].text
		    int_color = ' '.join(int_color.split())
		    trans = attribute.find_all('li')[2].text
		    trans = ' '.join(trans.split())
		    drivetrain = attribute.find_all('li')[3].text
		    drivetrain = ' '.join(drivetrain.split())
		    
		    print(ext_color)
		    print(int_color)
		    print(trans)
		    print(drivetrain)
		    print('\n')
		    
		        
		    item = script['page']['vehicle'][iteration]
		    print('listing_id: ', item['listingId'])
		    print('make: ', item['make'])
		    print('model: ', item['model'])
		    print('condition: ', item['stockType'])
		    print('year: ', item['year'])
		    print('trim: ', item['trim'])
		    print('bodystyle: ', item['bodyStyle'])
		    print('dealer: ', item['seller']['name'])
		    print('state: ', item['seller']['state'])
		    print('rating: ', item['seller']['rating'])
		    print('review count: ', item['seller']['reviewCount'])
		    print('CPO: ', item['certified'])
		    print('price: ', item['price'])
		    print('mileage: ', item['mileage'])
		    print('\n')
		        
		    print('----------------------')
		    print('\n')
		    
		    iteration += 1
		    
		    csv_writer.writerow([item['listingId'], name, price, mileage, ext_color, int_color, trans, drivetrain, 
		                         item['make'], item['model'], item['stockType'], item['year'], item['trim'], item['bodyStyle'],
		                         item['seller']['name'], item['seller']['state'], item['seller']['rating'], item['seller']['reviewCount'],
		                         item['certified'], item['price'], item['mileage']
		                        ])

		lag = [2, 4, 1, 8, 3, 12, 7, 5, 18]
		lag = np.random.choice(lag)
		time.sleep(lag)
		    
		    
	outfile.close()



def test():

	url = get_url()

	for page in range(2): #range(num_results['page']['search']['totalNumPages']-1):
		page_num = url[url.find('page=')+5]
		print(url[:url.find('page=')+5] + str(page+1) + url[url.find('page=')+6:])



'''
	urls = []
	for page in range(2): #range(num_results['page']['search']['totalNumPages']-1):
		page_num = url[url.find('page=')+5]
		print(page_num)
		print(url)
		url = url.replace(page_num, str(page+1))
		urls.append(url)'''

run_scraper()