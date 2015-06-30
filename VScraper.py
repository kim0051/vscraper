#!/usr/bin/env python3
import sys
from urllib.request import urlretrieve
import csv
import requests
from bs4 import BeautifulSoup as bs
import os

TYPES_DICT = {  'images':['.png', '.jpg', '.jpeg', '.gif', '.svg'],
                'audio':['.mp3', '.mp4', '.wmv', '.m4a', '.wav'],
                'text':['.txt', '.doc', '.docx', '.rtf', '.pdf', '.md'],
                'code':['.js', '.html', '.css', '.php', '.rb', '.py', '.java', '.c', '.cpp', '.h', '.go', '.cs', '.sql', '.m', '.mat'], }

files = []

debug = True
def db(string):
    if(debug):
        print('\t', string)

def main():
    """ Main function that asks for user input and prints out results """

    file_type = ""
  
    if len(sys.argv) == 1:
        csv_file_name = input("Enter the CSV file name you want to read from: ") + '.csv'
        if os.path.isfile(csv_file_name):
            print("File", "'" + csv_file_name + "'", "exists\n")
            print("Reading CSV file...")
            file_type = input("\nWhat type of file do you want to scrape? \nExamples: images, audio, text, code - ")
        else:
            print("\nFile", "'" + csv_file_name + "'", "does not exist in the current directory.")
   
    else:
        if os.path.isfile(sys.argv[1]):
            csv_file_name = sys.argv[1]
        else:
            print("\nFile", "'" + str(sys.argv[1]) + "'", "does not exist in the current directory.")
    
        try:
           file_type = sys.argv[2]
        except IndexError:
            file_type = input("\nWhat type of file do you want to scrape? \nExamples: images, audio, text, code - ")
            
    get_files(csv_file_name, file_type)
    #out_dir = '/path/to/dir'
    #os.system("mkdir {}".format(out_dir))
    print_message(files, file_type)
        
def get_files(file, file_type):
    """ Downloads files of type 'file_type', specified by the user.
    Input: The file name of the csv file, the type of file that
    the user wants to scrape; can be images, text, or audio
    """
    
    with open(file, 'r') as csvfile:
            filereader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for url in filereader:
                url = url[0]#.rpartition('/')[0]
                db("URL is: " + url)
                if not url.startswith('http://') and not url.startswith('https://'):
                    url = 'http://' + url
            
                response = requests.get(url, stream=True)
                soup = bs(response.text)

                for link in soup.find_all('a'):
                    db("Here is the link being examined: " + str(link.get('href')).rpartition('/')[2])
                    for suffix in TYPES_DICT[file_type]:
                        db("Suffix being examined: " + suffix)
                        if str(link.get('href')).endswith(suffix):
                            db("Suffix: " + suffix + " was found. Retrieving...")
                            files.append(link.get('href'))
                            urlretrieve(url + '/' + link.get('href'), link.get('href').rpartition('/')[2])


def print_message(lst, file_type):
    """ Notifies user when done downloading files OR
    if there are no files of the type they specified
    Input: List of file names, String for file extension
    """
    
    if lst:
        print("\nFinished. Downloaded all files of type", file_type)
        print("There were", str(len(lst)), "file(s).")
    else:
        print("\nNo files of type", file_type, "were found.")

if __name__ == '__main__':
    main()
