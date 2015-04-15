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
