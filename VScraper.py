from urllib.request import urlretrieve
from time import sleep
import csv
import requests
from bs4 import BeautifulSoup as bs
import os.path

images = ['.png', '.jpg', '.jpeg', '.gif']
audio = ['.mp3', '.mp4']
text = ['.txt', '.doc', '.docx', '.rtf']


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
                print(', '.join(row))
            print("\nFinished reading rows")                
    else:
        print("File, " "'" + csvfilename + "'", "does not exist.")

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
