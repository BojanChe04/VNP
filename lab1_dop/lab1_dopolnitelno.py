import time
import pandas as pd

import plotly
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

driver = Chrome()
driver.get("https://books.toscrape.com/")

category_elements = driver.find_elements(By.CSS_SELECTOR, ".nav-list ul li a")
categories = []
for element in category_elements:
    ime = element.text.strip()
    link = element.get_attribute("href")
    categories.append((ime,link))

category_count = len(categories)
print("Broj na kategorii: " , category_count)
# print("Kategorii: ")
# print(categories)


def funkcija(category_name,category_link):
    data = []
    url = category_link
    while True:
        driver.get(url)
        time.sleep(1)

        #sega gi zemame site knigi vo taja kateorija
        books = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
        for book in books:
            #go zema html za elementot (article vo slucajov)
            outer_html = book.get_attribute("outerHTML")
            #ova go parsirvit za da imat podobra truktura
            soup = BeautifulSoup(outer_html, "html.parser")

            #sega si gi zemame potrebnite pocaroci za sekoja kniga
            title = soup.h3.a['title']
            price = soup.find("p", class_="price_color").text.strip()
            availability = soup.find("p", class_="instock availability").text.strip()

            #zacuvuvame
            data.append({
                "category": category_name,
                "title": title,
                "price": price,
                "availability": availability
            })
        #provervime dali imat sledna strana, ona najdolu so e za next page
        next_page = driver.find_elements(By.CSS_SELECTOR, "li.next a")
        if next_page:
            next_page_url = next_page[0].get_attribute("href")
            url = next_page_url
        else:
            break

    return data

all_books = []
for i in range(category_count):
    ime, link = categories[i]
    # print("\n" + str(i) + " Kategorija: " + ime)

    books = funkcija(ime,link)
    # print(" ",len(books)," pronajdeni")
    all_books.extend(books)


driver.quit()
#sega prajme dataframe
df = pd.DataFrame(all_books)
df.to_csv("books.csv")
print("\nPrvite 5 reda")
print(df.head())

#vizuelizacija
#brojt kolku pati se pojavuva sekoja raz vrednost (title) vo kolonata
category_counts = df['category'].value_counts()
plt.figure(figsize=(6,6))
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Kategorii")
plt.ylabel("Broj na knigi")
plt.title("Raspredelba na knigi po kategorii")
plt.show()
