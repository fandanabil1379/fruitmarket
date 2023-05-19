import csv
import sys
import os
import pyinputplus as pypi
import fruitmarket as fm


def clearScreen():
    """
    Function for cleaning the user's screen
    """
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

def main():
    """
    The main program to run the whole process
    """
    global db
    while True:
        # Display the program's main view
        prompt = f"Welcome to the market! \n\nPlease select the menu:\n"
        # Select the feature to be executed
        choice = ["show", "add", "delete", "buy", "exit"]
        response = pypi.inputMenu(prompt=prompt, choices=choice, numbered=True)
        # Run the selected fitur
        if response != 'exit':
            eval(f'fm.{response}(db)')
        # Otherwise, exit from the menu
        else:
            break
    # Importing database file
    file = open(path, "w")
    # Keep database up to date
    writer = csv.writer(file, delimiter=";")
    writer.writerows(db.values())
    # Close the database file
    file.close()


if __name__ == "__main__":
    # Cleaning the user screen
    clearScreen()
    # Setting the path of database file
    path = os.path.join(f'{os.getcwd()}/src/data.csv')
    # Check the database contents, if empty, display a message.
    if os.path.getsize(path) == 0:
        print('Database is empty, please enter available stock first')
    # Otherwise, execute the program.
    else:
        # Importing database file
        file = open(path)
        # Read the data from database file
        reader = csv.reader(file, delimiter=";")
        # Create dictionary from database
        headings = next(reader)
        db = {"column": headings}
        # Input row into dictionary
        i = 0
        for row in reader:
            db.update(
                {
                    str(row[1]): [
                        int(row[0]), 
                        str(row[1]), 
                        int(row[2]), 
                        int(row[3]),
                    ]
                }
            )
            i += 1
        # Close the database file
        file.close()
        # Run main program
        main()
    # Close the program
    sys.exit()
