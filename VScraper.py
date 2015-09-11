#!/usr/bin/env python3
import sys
from urllib.request import urlretrieve
import csv
import requests
from bs4 import BeautifulSoup as bs
import os

# a dictionary containing all possible file types that may be scraped from URLs
TYPES_DICT = {  'images': ['.png', '.jpg', '.jpeg', '.gif', '.svg'],
                'video' : ['.swf', '.mpg', '.mpeg'],
                'audio' : ['.mp3', '.mp4', '.wmv', '.m4a', '.wav'],
                'text'  : ['.txt', '.doc', '.docx', '.rtf', '.pdf', '.md'],
                'code'  : ['.js', '.html', '.css', '.php', '.rb', '.py',
                           '.java', '.c', '.cpp', '.h', '.go', '.cs',
                           '.sql', '.m', '.mat'], }

files = []

debug = False
def db(string):
    if(debug):
        print('\t', string)


def main():
    """ Main function that reads user input from the command line or
    asks for user input directly in IDLE and prints out results """

    file_type = ""

    # prompts for more information if the user only executes VScraper.py from the command line 
    if len(sys.argv) == 1:
        csv_file_name = input("Enter the CSV file name you want to read from: ") + '.csv'
        if os.path.isfile(csv_file_name):
            print("File", "'" + csv_file_name + "'", "exists\n")
            print("Reading CSV file...")
            file_type = input("\nWhat type of file do you want to scrape? \nExamples: images, audio, text, code - ")
        else:
            print("\nFile", "'" + csv_file_name + "'", "does not exist in the current directory.")

    # otherwise, check if the command line arguments fit the parameters to run the functions
    else:
        if os.path.isfile(sys.argv[1]):
            csv_file_name = sys.argv[1]
        else:
            print("\nFile", "'" + str(sys.argv[1]) + "'", "does not exist in the current directory.")
    
        try:
           file_type = sys.argv[2]
        except IndexError:
            file_type = input("\nWhat type of file do you want to scrape? \nExamples: images, audio, text, code - ")
        
    get_files(csv_file_name, file_type, file_type)
    print_message(files, file_type)

        
def get_files(file, file_type, out_dir):
    """ Downloads files of type 'file_type', specified by the user.
    Input: The file name of the csv file, the type of file that
    the user wants to scrape (can be images, text, or audio) and
    the output folder that needs to be created for the files
    """
        
    with open(file, 'r') as csvfile:
            filereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for url in filereader:
                url = url[0]
                db("URL is: " + url)
                if not url.startswith('http://') and not url.startswith('https://'):
                    url = 'http://' + url
            
                response = requests.get(url, stream=True)
                soup = bs(response.text)

                # if file type is images, then find <img> tags and concatenate
                # images links with main URL links
                if file_type == 'images':
                    for link in soup.find_all('img'):
                        db("Here is the link being examined: " + str(link.get('src')))
                        for suffix in TYPES_DICT['images']:
                            if str(link.get('src')).endswith(suffix):
                                db("Suffix: " + suffix + " was found. Retrieving...")
                                files.append(link.get('src'))
                                os.system("mkdir {}".format(out_dir))
                                urlretrieve('http:' + link.get('src'), out_dir + '/' + link.get('src').rsplit('/')[-1])

                # otherwise, search for all <a> tags and then retrieve files based on hrefs
                else:
                    for link in soup.find_all('a'):
                        db("Here is the link being examined: " + str(link.get('href')).rpartition('/')[2])
                        for suffix in TYPES_DICT[file_type]:
                            db("Suffix being examined: " + suffix)
                            if str(link.get('href')).endswith(suffix):
                                db("Suffix: " + suffix + " was found. Retrieving...")
                                files.append(link.get('href'))
                                os.system("mkdir {}".format(out_dir))
                                urlretrieve(url + '/' + link.get('href'), out_dir + '/' + link.get('href').rpartition('/')[2])


def print_message(lst, file_type):
    """ Notifies user when done downloading files OR
    if there are no files of the type they specified
    Input: List of file names, String for type of files
    """
    
    if lst:
        print("\nFinished. Downloaded all files of type", file_type)
        print("There were", str(len(lst)), "file(s).")
    else:
        print("\nNo files of type", file_type, "were found.")


if __name__ == '__main__':
    main()
