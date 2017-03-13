# Used for command line parameters
import sys
import getopt
# Used for parsing information from each page's content
from bs4 import BeautifulSoup
# Used for getting "curl" content
import urllib2
# Used for file operations
import os



# Function gets a page's content, prints a page's content to a file, loops through each anchor tag in the page, and repeats for each tag on that page, for a certain number of steps
def walkLinks(presentUrl, numberOfSteps, storeDirectory):
    try:
        document = urllib2.urlopen(presentUrl)
        soup = BeautifulSoup(document, "html.parser")
        soupText = soup.get_text()
        fileName = presentUrl.replace("/", "<SLASH>")
        fileToWrite = open(storeDirectory + fileName, 'w')
        fileToWrite.write(soupText.encode('utf-8'))
        fileToWrite.close()
        soupAnchors = soup.find_all("a")
        anchorCount = len(soupAnchors)
        if (numberOfSteps > 0):
            for index in range(0, anchorCount):
                walkLinks(soupAnchors[index].attrs["href"], int(numberOfSteps)-1, storeDirectory)
    except ValueError:
        print("Did not know how to deal with URL: " + presentUrl)
    except urllib2.HTTPError:
        print("Encountered an issue when requesting URL: " + presentUrl)
    except urllib2.URLError:
        print("Had a problem trying connect with URL: " + presentUrl)



# Parameters! Default values with which the script starts
numberOfSteps = 3
presentUrl = "https://www.wikipedia.org/"
folderName = "/savedHtmlContent/"



# Get all user-provided values other than the filename
inputValues = sys.argv[1:]
options, arguments = getopt.getopt(inputValues, "s:u:f:", ["steps=", "url=", "folder="])

for argumentFlag, argumentValue in options:
    if (argumentFlag == "-s" or argumentFlag == "--steps"):
        numberOfSteps = argumentValue
    if (argumentFlag == "-u" or argumentFlag == "--url"):
        presentUrl = argumentValue
    if (argumentFlag == "-f" or argumentFlag == "--folder"):
        folderName = argumentValue

# Get path of this file, for storing output files
storeDirectory = os.path.dirname(os.path.realpath(__file__))
# Create new directory "savedHtmlContent" in the same directory of the python script
storeDirectory += folderName
if not os.path.exists(storeDirectory):
    os.makedirs(storeDirectory)

# Call the "action" function
walkLinks(presentUrl, numberOfSteps, storeDirectory)