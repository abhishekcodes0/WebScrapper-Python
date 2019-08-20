from bs4 import BeautifulSoup
from selenium import webdriver
from csv import writer
import time

url = "https://www.pokemon.com/us/pokedex/"
browser = webdriver.Firefox()
browser.get(url)
time.sleep(8)

browser.find_element_by_id('cookie-dismisser').click()
browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
loadmore = browser.find_element_by_link_text('Load more Pokémon')
loadmore.click()
time.sleep(2)

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(4)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

html = browser.page_source

soup = BeautifulSoup(html,'html.parser')

li = soup.find_all(class_='animating')

with open('poke.csv','w') as csv_file:
    csv_writer = writer(csv_file)
    headers = [ 'ID', 'Name', 'Abilities', 'Img-Src']
    csv_writer.writerow(headers)
    for element in li:
        try:
            link=element.find('img')['src'].strip()
            id = element.find('p').text.strip()
            name = element.find('h5').text.strip()
            abilities =[]
            ability = element.find_all(class_="pill")      
            for i in ability:
                abilities.append(i.text.strip())
            final_abilities = " ".join(map(str, abilities))
            csv_writer.writerow([id,name,final_abilities,link])
        except :
            pass

browser.quit()