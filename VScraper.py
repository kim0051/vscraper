import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve


url = input("Enter the URL you want to scrape from: ")
print("")

bs = BeautifulSoup

link_list = []
file_names = []
suffix = input("What type of file do you want to scrape? \
               \nExamples: .png, .pdf, .doc - ")
response = requests.get(url, stream=True)
soup = bs(response.text)

def getPDFs():
        
    for link in soup.find_all('a'): # Finds all links
        if suffix in str(link): # If the link ends in .pdf
            link_list.append(link.get('href'))

    for i in range(len(link_list)):
        file_names.append(str(link_list[i]).replace('/[^/]*$',''))
    print(file_names)