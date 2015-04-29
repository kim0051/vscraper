import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
import time

bs = BeautifulSoup
debug = False
def db(string):
    """ Debugging function for program; won't have to
    write 'print' every time, and can turn on/off
    while still keeping in the debug calls"""
    
    if debug:
        print("\t", string)
        
def getFiles():
    """ Gets files of specified extension through user input"""
    
    url = input("Enter the URL you want to scrape from: ")

    suffix = input("\nWhat type of file do you want to scrape? \
               \nExamples: .png, .pdf, .doc - ")

    filepath = input("Specify a file path to save to: ")

    link_list = []
    file_names = []

    response = requests.get(url, stream=True)
    soup = bs(response.text)
        
    for link in soup.find_all('a'): # Finds all links
        # If the file is a link ending in the entered suffix 
        if suffix in str(link):
            link_list.append(link.get('href'))

    for link in link_list:
        file_names.append(link.rpartition('/')[-1])

    i = 0
    for link in link_list:
        urlretrieve(url.rsplit('/',1)[0] + '/' + link, filepath + '\\' + file_names[i])
        i += 1
            
    printMessage(link_list, suffix)

    repeat = input("\nScrape from another URL? ")
    if repeat.startswith("y") or repeat.startswith("Y"):
        getFiles()
    else:
        print("Closing program...")
        time.sleep(3)
        print("\nGoodbye")
        
def printMessage(lst, suffix):
    """ Notifies user when done downloading files OR
    if there are no files of the type they specified"""
    
    if lst == []:
        print("\nNo files of type", suffix, "were found.")
    else:
        print("\nFinished. Downloaded all files of type", suffix)
    time.sleep(2)

getFiles()
