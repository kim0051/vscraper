from urllib.request import urlretrieve
from time import sleep
import csv
import requests
from bs4 import BeautifulSoup as bs
import os.path

images = ['.png', '.jpg', '.jpeg', '.gif']
audio = ['.mp3', '.mp4']
text = ['.txt', '.doc', '.docx', '.rtf']
list_of_links = []
file_name = ''

debug = True
def db(string):
    if(debug):
        print('\t', string)

def get_files():
    """ Gets files of specified extension through user input
    from a specified full URL path; downloads each file to
    the user's specified local directory.
    """

    csvfilename = input("Enter the CSV file you want to read from: ") + '.csv'
    if os.path.isfile(csvfilename):
        print("File", "'" + csvfilename + "'", "exists\n")
        print("Reading CSV file...\n")
        
        with open(csvfilename, 'r') as csvfile:
            filereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in filereader:
                list_of_links.append(row)
            print("\nFinished reading rows")

        suffix = input("\nWhat type of file do you want to scrape? \nExamples: images, audio, text - ")
        print("\nOK. Scraping files of type:", suffix)
        db("List of links: " + str(list_of_links))
        
        for url in list_of_links:
            db("Link: " + str(url[0]))
            if not url[0].startswith('http://') and not url[0].startswith('https://'):
                url[0] += 'http://'
            
            response = requests.get(url[0], stream=True)
            soup = bs(response.text)

            for link in soup.find_all('a'):
                if suffix in str(link):
                    link.get('href')
                    db("href: " + link.get('href'))
                    file_name = link.rpartition('/')[-1]
                    db("fn: " + file_name)
                    urlretrieve(link.split('/', 1)[0] + '/' + link, file_name)
                    
        print("\nFinished scraping files")
        print_message(list_of_links, suffix)
        
    else:
        print("File, " "'" + csvfilename + "'", "does not exist \
              in the current directory.")

def print_message(lst, suffix):
    """ Notifies user when done downloading files OR
    if there are no files of the type they specified
    Input: List of file names, String for file extension
    """
    
    if lst:
        print("Finished. Downloaded all files of type", suffix)
        print("There where", str(len(lst)), "file(s).")
    else:
        print("No files of type", suffix, "were found.")


def repeat(decision):
    """ Function for running the file scraper again
    Input: String 'yes' or 'no'
    """
    
    if decision.lower().startswith("y"):
        return True
    
    print("Closing program...")
    sleep(3)
    print("\nGoodbye")
    return False

if __name__ == '__main__':
    get_files()
