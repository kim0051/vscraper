import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve

bs = BeautifulSoup

url = input("Enter the URL you want to scrape from: ")
print("")

link_list = []
file_names = []
suffix = input("What type of file do you want to scrape? \
               \nExamples: .png, .pdf, .doc - ")

filepath = input("Specify a file path to save to: ")

response = requests.get(url, stream=True)
soup = bs(response.text)

def getFiles():
        
    for link in soup.find_all('a'): # Finds all links
        # If the file is a link ending in the entered suffix 
        if suffix in str(link):
            link_list.append(link.get('href'))

    for link in link_list:
        file_names.append(link.rpartition('/')[-1])
    
    for link in link_list:
        for name in file_names:
            urlretrieve(link, filepath + name)
            
    printMessage(link_list)
    
def printMessage(lst):
        if lst == []:
            print("\nNo files of type", suffix, "were found.")
        else:
            print("\nFinished. Downloaded all files of type", suffix)

getFiles()
