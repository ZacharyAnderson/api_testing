import os, sys
from Array_menu import ESGMID3PAR7400C1
# Main Menu for 3Par Provisioning Menu
def main_menu():
    os.system('clear')
    print ('Welcome Storage Administrator, \n')
    print ('Please select the Storage Array you would like to work on: \n')
    print ('1. ESGMID3PAR7400C1\n')
    print ('0. Quit\n')
    choice = input(' >> ')
    # Gets input from Storage Administrator and will call function to execute menu choice
    exec_menu(choice)
    return

# Takes the input and Logs into the Array of choice
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        main_menu()
    elif ch == '1':
        #this calls the function ESGMID3PAR7400C1 to execute the API calls
        ESGMID3PAR7400C1()
        main_menu()
    elif ch == '0':
        exit()

# exit() will be used to simply exit the python program
def exit():
    print ('Later Lad')
    return

if __name__ == '__main__':
    main_menu()