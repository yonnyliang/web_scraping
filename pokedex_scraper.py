# Import libraries 'requests' to get the html document, 'beautifulsoup' to parse the document and 'csv' to export the file

import requests
from bs4 import BeautifulSoup
import csv

# Create a list that we'll use later on to put all the data we want to take from the website
pokedex = []

# Create a variable the contain the html document
response = requests.get("https://scrapeme.live/shop/")

# In this case since we have to go through all the 48 pages to get all the data, we use a iterator 'for' to do it automatically

for i in range(1,49):
    # By changing just the path parameter with the iteration, we'll go through every page we need
    response = requests.get("https://scrapeme.live/shop/page/"+str(i))
    # Create a objet with the html document parse
    soup = BeautifulSoup(response.content, "html.parser")
    # Select the data you want to extract, in this case is all the tags 'li' in the document
    product_elements = soup.select("li.product")
    
    # Iterate again for every element 'li' to extract it's data
    for product_element in product_elements:
        # Put in a variable every data you want to extract to later save it in the list we create before
        name = product_element.find("h2").get_text()
        price = product_element.find(class_="price").get_text()
        url = product_element.find("a")["href"]
        image = product_element.find("img")["src"]
        # Make a dictionary to organize all the data
        entry = {
            "name" : name,
            "price" : price,
            "url" : url,
            "image" : image
        }
        # Insert the data with the method 'append' to the list we create before, every dictionary will be a row
        pokedex.append(entry)

#SCRAPING LOGIC FOR CSV

# Create the csv file
csv_file = open("complete_pokedex_file.csv", "w", encoding="utf-8", newline="") #(name, mode, encoding, for linebreak)

# Initialize a writer object for csv data
writer = csv.writer(csv_file)

# Convert each element of pokedex to a row and add it to the output file
for pokemon in pokedex:
    writer.writerow(pokemon.values()) #writer is the object, writerow means the only writes a row with the values

# Release the file
csv_file.close()