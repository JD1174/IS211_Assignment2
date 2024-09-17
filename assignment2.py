import urllib.request
import logging
import argparse
from datetime import datetime

def downloadData(url):
    response = urllib.request.urlopen(url)
    return response.read().decode('utf-8')

def processData(file_content):
    personData = {}
    lines = file_content.split('\n')
    logger = logging.getLogger('assignment2')
    
    for linenum, line in enumerate(lines, start=1):
        parts = line.split(',')
        
        # Skip lines with missing or non-numeric IDs
        if len(parts) < 3 or not parts[0].isdigit():
            continue
        
        id, name, birthday = parts[0], parts[1], parts[2]
        
        try:
            # Attempt to parse the birthday
            birthday = datetime.strptime(birthday, '%d/%m/%Y')
            personData[int(id)] = (name, birthday)
        except ValueError:
            # Log only birthday parsing errors
            logger.error(f"Error processing line #{linenum} for ID #{id}")
    
    return personData

def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")
    else:
        print("No user found with that id")

def setupLogger():
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)
    handler = logging.FileHandler('errors.log')
    logger.addHandler(handler)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, help='URL of the CSV file')
    args = parser.parse_args()

    try:
        csvData = downloadData(args.url)
    except Exception as e:
        print(f"Failed to download data: {e}")
        return

    setupLogger()
    personData = processData(csvData)

    while True:
        try:
            id = int(input("Enter an ID number: "))
            if id <= 0:
                break
            displayPerson(id, personData)
        except ValueError:
            print("Invalid input. Please enter a valid ID number.")

if __name__ == "__main__":
    main()