import os, sys
from Array_menu import HPE3Par
# Main Menu for 3Par Provisioning Menu
def main_menu():
    os.system('clear')
    print ('Welcome Storage Administrator, \n')
    print ('Please select the Storage Array you would like to work on: \n')
    print ('1. ESGMID3PAR7400C1\n')
    print ('2. ESGLYN3PAR7400C1\n')
    print ('3. ESGLYN3PAR-25K8\n')
    print ('4. ESGMID3PAR-22WT\n')
    print ('5. ESGNET3PAR7400C\n')
    print ('6. ESGPL3PAR20K1\n')
    print ('7. ESGPM3PAR20K1')
    print ('0. Quit\n')
    choice = input(' >> ')
    # Gets input from Storage Administrator and will call function to execute menu choice
    exec_menu(choice)
    return

# Takes the input and Logs into the Array of choice
def exec_menu(choice):
    os.system('clear')
    ch = choice.lower()
    if ch == '1':
        HPE3Par('192.168.142.50')
        main_menu()
    elif ch == '2':
        HPE3Par('192.168.18.40')
        main_menu()
    elif ch == '3':
        HPE3Par('192.168.18.26')
        main_menu()
    elif ch == '4':
        HPE3Par('140.163.142.66')
        main_menu()
    elif ch == '5':
        HPE3Par('140.163.146.193')
        main_menu()
    elif ch == '6':
        HPE3Par('192.168.18.23')
        main_menu()
    elif ch == '7':
        HPE3Par('10.254.200.29')
        main_menu()
    elif ch == '0':
        exit()
    else:
        main_menu()

# exit() will be used to simply exit the python program
def exit():
    print ('Later Lad')
    return

if __name__ == '__main__':
    main_menu()