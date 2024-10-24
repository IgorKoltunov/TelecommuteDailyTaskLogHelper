import argparse
from datetime import datetime, timedelta
from pprint import pprint as pp
import os
import time
import helpers

quarter_of_the_year = '' # Declairing global

def fiscal_year(myTime):
    
    if myTime.month in range(1,6):
        #print('DEBUG: Month 1 to 6')
        fiscalYear = 'FY' + str(int(myTime.year)-1)[2:] + '-' + str(myTime.year)[2:]

    else:
        #print('DEBUG: Month 7 to 12')
        fiscalYear = 'FY' + str(int(myTime.year))[2:] + '-' + str(int(myTime.year)+1)[2:]

    return fiscalYear


def main():
    
    commandLineArgsDic = helpers.parse_cli_args()
    if commandLineArgsDic["days_to_adjust"]:
        print("Using days_to_adjust to offset")
        days_to_adjust = int(commandLineArgsDic["days_to_adjust"])
        myTime = datetime.today() + timedelta(days=days_to_adjust)
    else:
        myTime = datetime.today()


    # Using Today
    #myTime = datetime.today()

    # DEBUG: Using Specific Date
    #myTime = datetime(2023, 7, 1)

    quarter_of_the_year = 'Q'+str((myTime.month-1)//3+1)
    weekNumber = str(int(myTime.strftime('%U'))+1)

    print('-' * 106)
    print('CY' + myTime.strftime('%Y'), fiscal_year(myTime), quarter_of_the_year, 'Week #' + weekNumber, sep=', ')
    print('-' * 106)
    print(myTime.strftime('%Y%m%d - %A'))
    if commandLineArgsDic["template"] == '1':
        print('''    * ITP Specific Tasks: 2509010, 2508010: 2.5
        * Organizing emails, files, tracking notes
        * Following up on assignments
        * Verifying and sending invoice for payment

    * Administrative/Concurrent Tasks: 5
        * Daily Tasks: Lunch/Breaks & Religious/Cultural Practices
        * Daily Tasks: Check in/Check out, monitor, sort email
        * County Election Worker Lead Training
        * Updating time tracking
            
    * ITP General Tasks/Concurrent Tasks: 0.5
        * Updating/organizing email templates
            ''')
    elif commandLineArgsDic["template"] and commandLineArgsDic["template"].lower() == 's':
        print('Under Construction!')
        taskStringList = helpers.get_file_contents('formattingDB.txt')

        #pp(taskStringList[5:25])
        print('	* ITP Specific Tasks: 2509010, 2508010: 2.5')
        print('\t' * 2 + taskStringList[5])

if __name__ == '__main__':
        main()
