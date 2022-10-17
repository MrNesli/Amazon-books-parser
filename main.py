import time
import csv
import random
import typing
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


# Create Firefox options
options = Options()
# Show gui: True
options.headless = False


# Create Firefox webdriver instance
driver = webdriver.Firefox(options=options)
# Maximize the window
driver.maximize_window()
# Go to the page with genres
driver.get('https://www.amazon.fr/livre-achat-occasion-litterature-roman/b/?ie=UTF8&node=301061&ref_=nav_cs_books')
# Wait 1 sec
# time.sleep(1)


def get_genres(driver) -> dict:
	try:
		# Parse all the genres webelement (to click it and at the same time get the title)
		# And construct dictionary in such manner - {element.text : element(selenium element)}
		return { i.text: i for i in driver.find_elements(By.XPATH, '//div[@class="a-section octopus-pc-category-card-v2-category-title"]/span')}
	except:
		print('No genres found. You\'re probably on the wrong page. Or the page structure was changed')

def remove_empty_elements(arr: list) -> list:
	# Pretty self-explanatory. Check if elements in arr are not empty then we append them into a new_arr
	new_arr = []
	for i in arr:
		if i != '':
			new_arr.append(i)
	return new_arr

def pick_random_categories(amount: int) -> list:
	# Get all current genres on the page
	genres = remove_empty_elements(list(get_genres(driver).keys()))

	# Random genres to pick list
	pick = []
	# iterator
	i = 0
	# executed iterations
	current_iterations = 0
	# max possible executed operations
	max_iterations = 1000
	# Iterate while iterator lesser than amount of genres to be picked
	while i < amount:
		# Check if current iterations don't exceed the max iterations
		if current_iterations >= max_iterations:
			print('Max possible amount is:', len(pick))
			break

		# Randomly pick genre from page's available genres
		choice = random.choice(genres)

		# Check if randomly picked value wasn't already chosen
		if choice not in pick:
			pick.append(choice)
			i += 1

		current_iterations += 1

	return pick






# TODO: Figure out how to maximize window in headless mode
# And for portfolio just take a picture of the data in a file and name it amazon genres parser

# Output format genres
books = []
book_category = 'Les plus demandés'
	
# Currency of prices
currency = '€'
# Randomly pick 4 book genres
pick = pick_random_categories(4)
print(pick)


# Iterate through all the picked stuff
for i in pick:
	# Go to the genres link
	driver.get('https://www.amazon.fr/livre-achat-occasion-litterature-roman/b/?ie=UTF8&node=301061&ref_=nav_cs_books')
	driver.implicitly_wait(1)
	# Parse all the genres and clickable text elements
	genres = get_genres(driver)
	try:
		# Click on accept cookies button
		driver.find_element(By.XPATH, '//input[@id="sp-cc-accept"]').click()
	except:
		print('Cookies button not found')

	driver.implicitly_wait(1)
	
	try:
		# We wait for genre element to be clickable
		el = WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((genres[i])))
		# We scroll our viewport to the genres (To be able to click it because if your screen isn't within viewport of an element it will throw an exception)
		driver.execute_script('window.scrollTo(0, 450);')
		#action = ActionChains(driver)
		# This action doesn't work with firefox...
		# action.move_to_element(el).perform()
		el.click()
	except Exception as e:
		print(e)
		print('Element ({}) still not clickable'.format(i))

	
	# 1 second wait after page load
	driver.implicitly_wait(1)
	
	# Parse all possible titles on genre pages to get correct index of Les plus demande section
	page_title = [i.text for i in driver.find_elements(By.XPATH, '//div[@class="unified_widget pageBanner"]/h1/b')]
	main_titles = [i.text for i in driver.find_elements(By.XPATH, '//div[@class="a-section octopus-pc-card-title"]/span')]
	honor_category_title = [i.text for i in driver.find_elements(By.XPATH, '//div[@class="a-section octopus-pc-category-card-v2-title"]/span')]
	children_titles = [i.text for i in driver.find_elements(By.XPATH, '//div[@class="bxc-grid__text a-text-left   bxc-grid__text--light bxc-grid__text--beauty bxc-grid__text--beauty"]/h2')]
	school_titles = [i.text for i in driver.find_elements(By.XPATH, '//div[@class="bxc-grid__text a-text-left   bxc-grid__text--light"]/h2')]
	brands_related_titles = [i.text for i in driver.find_elements(By.XPATH, '//div[@class="a-section a-spacing-none _bXVsd_block_1vI8- _bXVsd_col_358pf"]/span')]
	extra_title = [i.text for i in driver.find_elements(By.XPATH, '//h2[@class="a-spacing-mini acswidget-carousel__header"]/span[@class="acswidget-carousel__title"]')]

	# Div element index 
	row_indx = 0
	
	# Check if there is page title
	if page_title:
		# Move the index
		row_indx += 1
		print('Plus page title length')

	# Check if there is honor title	
	if honor_category_title:
		# Move the index
		row_indx += len(honor_category_title)

	# Check if there is children titles
	if children_titles:
		# Move the index
		row_indx += len(children_titles)


	# Check if there is school titles or such
	if school_titles:
		# Move the index
		row_indx += len(school_titles)

	# Check if there is extra title which is among main titles on the website but has different html structure
	if extra_title:
		if main_titles.index(book_category) + 1 >= 2: 
			row_indx += len(extra_title)

	# Check if there is no main titles then we just skip an iteration
	if not main_titles:
		continue

	# Check if there is main titles
	if main_titles:
		# Move the index to our wanted category (Les plus demandes)
		row_indx += (main_titles.index(book_category) + 1)


	# Paths of the category's book titles, book prices, and fractions of those prices
	book_titles_path = '//div[@class="a-row apb-browse-two-col-center-pad"]/div[1]/div[{}]//div[@class="a-section octopus-pc-asin-title"]/span'.format(row_indx)
	prices_path = '//div[@class="a-row apb-browse-two-col-center-pad"]/div[1]/div[{}]//span[@class="a-price-whole"]'.format(row_indx) # if doesn't work set full xpath
	price_fractions_path = '//div[@class="a-row apb-browse-two-col-center-pad"]/div[1]/div[{}]//span[@class="a-price-fraction"]'.format(row_indx)


	# Parse the data
	book_titles = [i.text for i in driver.find_elements(By.XPATH, book_titles_path)]
	prices = [i.text for i in driver.find_elements(By.XPATH, prices_path)]
	price_fractions = [i.text for i in driver.find_elements(By.XPATH, price_fractions_path)]

	# Remove any empty elements in parsed lists
	book_titles = remove_empty_elements(book_titles)
	prices = remove_empty_elements(prices)
	price_fractions = remove_empty_elements(price_fractions)


	# Output format list
	output_format = []
	# Add current genre's title
	output_format.append(i + ':')

	
	# Check if all the data has the same length (1 book title for 1 price for 1 fraction price)
	if len(book_titles) == len(prices) == len(price_fractions):
		for i in range(len(book_titles)):
			# Construct Title:price string
			rs = book_titles[i] + ': ' + currency + prices[i] + '.' + price_fractions[i]
			# Add the output element
			output_format.append(rs)
	else:
		print('Something went wrong. The length of the data doesn\'t match.')
		exit(1)

	# Add to output genres
	books.append(output_format)
	

# File name
csv_file = 'prices.txt'
# Open file for writing or create new file
with open(csv_file, 'w') as file:
	# Iterate through all the books
	for i in books:
		for j in i:
			# Write the price
			file.write(j + '\n\n')
		file.write('\n')

driver.quit()
