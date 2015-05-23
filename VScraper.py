import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlretrieve
from time import sleep, time

debug = False

def db(string):
    """ Debugging function for program; won't have to
    write 'print' every time, and can turn on/off
    while still keeping in the debug calls """
    
    if debug:
        print("\t", string)
        
#############################################################################        
def getFiles():
    """ Gets files of specified extension through user input
    from a specified full URL path; downloads each file to
    the user's specified local directory. """
    
    url = input("Enter the URL you want to scrape from: ")

    suffix = input("\nWhat type of file do you want to scrape? \
               \nExamples: .png, .pdf, .doc - ")

    filepath = input("Specify a file path to save to: ")

    link_list = []
    file_names = []
    
    # start_time = time()
    response = requests.get(url, stream=True)
    soup = bs(response.text)

    # finds all links    
    for link in soup.find_all('a'):
        # If the file is a link ending in the entered suffix 
        if suffix in str(link):
            link_list.append(link.get('href'))

    # assigns the filename to each downloaded file
    # taken from the file name; after the last forward slash
    # in the website's directory
    for link in link_list:
        file_names.append(link.rpartition('/')[-1])

    # saves the file to the local directory specified by the user
    # with the file names assigned in the previous for loop
    i = 0
    for link in link_list:
        urlretrieve(url.rsplit('/',1)[0] + '/' + link, filepath + '\\' + file_names[i])
        i += 1
        
    # db("--- %s seconds ---" %(time() - start_time))    
    printMessage(link_list, suffix)
    decision = input("\nScrape from another URL? ")
    repeat(decision)
        
############################################################################# 
def printMessage(lst, suffix):
    """ Notifies user when done downloading files OR
    if there are no files of the type they specified
    Input: List of file names, String for file extension """
    
    if lst == []:
        print("\nNo files of type", suffix, "were found.")
    else:
        print("\nFinished. Downloaded all files of type", suffix)
    sleep(2)
    
#############################################################################
def repeat(decision):
    """ Function for running the file scraper again
    Input: String 'yes' or 'no' """
    
    if decision.startswith("y") or decision.startswith("Y"):
        getFiles()
    else:
        print("Closing program...")
        sleep(3)
        print("\nGoodbye")

getFiles()
