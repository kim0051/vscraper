from urllib.request import urlretrieve
from time import sleep
 
import requests
from bs4 import BeautifulSoup as bs

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
    
    while True:
        url = input("Enter the URL you want to scrape from: ")

        suffix = input("\nWhat type of file do you want to scrape? \
                   \nExamples: .png, .pdf, .doc - ")

        filepath = input("Specify a file path to save to: ")

        link_list = []
        file_names = []
        
        # start_time = time()
        if not url.startswith('http://') and not url.startswith('https://'):
            url += 'http://'

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
        for i, link in enumerate(link_list):
            urlretrieve(url.rsplit('/',1)[0] + '/' + link, filepath + '\\' + file_names[i])
            
        # db("--- %s seconds ---" %(time() - start_time))    
        printMessage(link_list, suffix)
        if not repeat(input("\nScrape from another URL? ")):
            break
        
############################################################################# 
def printMessage(lst, suffix):
    """ Notifies user when done downloading files OR
    if there are no files of the type they specified
    Input: List of file names, String for file extension """
    
    if lst:
        print("\nNo files of type", suffix, "were found.")
    else:
        print("\nFinished. Downloaded all files of type", suffix)
    
#############################################################################
def repeat(decision):
    """ Function for running the file scraper again
    Input: String 'yes' or 'no' """
    
    if decision.lower().startswith("y"):
        return True
    
    print("Closing program...")
    sleep(3)
    print("\nGoodbye")
    return False

getFiles()
