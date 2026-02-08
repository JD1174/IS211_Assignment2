import argparse
import urllib.request
import urllib.error
import logging
import datetime
import csv
import sys

def downloadData(url):
    """Downloads the data"""
    # Part II: Download the Data
    # Use urllib to download contents and return it
    # Don't catch exceptions here
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')

def processData(file_content):
    """Parses the CSV content and returns a dictionary"""
    # Part III: Process Data
    personData = {}
    logger = logging.getLogger('assignment2')
    
    # Split the content into lines to handle as CSV
    lines = file_content.splitlines()
    reader = csv.reader(lines)
    
    # Enumerate starting at 1 for line numbers
    for line_num, row in enumerate(reader, 1):
        # Ensure row has enough data (ID, Name, Birthday)
        if len(row) < 3:
            continue
            
        id_str = row[0]
        name = row[1]
        birthday_str = row[2]
        
        # Skip header row if present (assuming ID column header is not a digit)
        if line_num == 1 and not id_str.isdigit():
            continue
            
        try:
            person_id = int(id_str)
            # Convert string dd/mm/yyyy to datetime object
            birthday = datetime.datetime.strptime(birthday_str, "%d/%m/%Y")
            
            # Map ID to tuple (name, birthday)
            personData[person_id] = (name, birthday)
            
        except ValueError:
            # Log error if date formatting fails or ID is not an int
            logger.error(f"Error processing line #{line_num} for ID #{id_str}")
            
    return personData

def displayPerson(id, personData):
    """Prints person information based on ID"""
    # Part IV: Display / User Input
    if id in personData:
        name, birthday = personData[id]
        # Display the date as YYYY-MM-DD
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")
    else:
        print("No user found with that id")

def main(url):
    print(f"Running main with URL = {url}...")
    
    # Part V: 3. Configure Logger
    logging.basicConfig(filename='errors.log', level=logging.ERROR)
    
    # Part V: 2. Download Data with error handling
    try:
        csvData = downloadData(url)
    except urllib.error.URLError as e:
        print(f"Error downloading data: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred during download: {e}")
        sys.exit(1)

    # Part V: 4. Process Data
    personData = processData(csvData)
    
    # Part V: 5. User Input Loop
    while True:
        try:
            user_input = input("Enter an ID to lookup: ")
            
            # Handle potential non-integer inputs gracefully
            try:
                search_id = int(user_input)
            except ValueError:
                print("Please enter a valid integer.")
                continue

            if search_id <= 0:
                print("Exiting program.")
                sys.exit(0)
            else:
                displayPerson(search_id, personData)
                
        except (KeyboardInterrupt, EOFError):
            print("\nExiting program.")
            sys.exit(0)

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)