#import pyodbc
import argparse
from datetime import datetime, timedelta
from pprint import pprint as pp
import os
import time

quarter_of_the_year = '' # Declairing global


def get_file_contents(fileName, isKeepNewLineChar=True):
    if not os.path.isfile(fileName):
        print('Critical Error: ' + fileName + ' not found.')
        raise OSError('Critical Error:', fileName, 'not found.')

    with open(fileName, 'r') as file:
        if not isKeepNewLineChar:
            fileContents = file.read().splitlines()
        else:
            fileContents = file.readlines()
        
    return fileContents


def parse_cli_args():
    """ Setup and validate command line arguments.

    Returns:
    (dict) Dictionary of supplied command line arguments.
    """

    parser = argparse.ArgumentParser(description='Email Jobs Monitoring')
    parser.add_argument('-ds', '--days_to_subtract', required=False, metavar='',
                        help='Specify email date to check. Format YYYYMMDD.')
    parser.add_argument('-t', '--template', required=False, metavar='',
                        help='Print template: 0/NULL, 1 (), S ([.....])')
    argsDict = vars(parser.parse_args())

    #if argsDict['days_to_subtract'] and argsDict['relative']:
    #    print(red_color('Error:'), 'Use --date or --relative but not both. See usage.\n')
    #    parser.print_help()
    #    sys.exit()



    return argsDict


def fiscal_year(myTime):
    
    if myTime.month in range(1,6):
        #print('DEBUG: Month 1 to 6')
        fiscalYear = 'FY' + str(int(myTime.year)-1)[2:] + '-' + str(myTime.year)[2:]

    else:
        #print('DEBUG: Month 7 to 12')
        fiscalYear = 'FY' + str(int(myTime.year))[2:] + '-' + str(int(myTime.year)+1)[2:]

    return fiscalYear

# Generate header for today (using MS SQL Server)
#Create connection to DB
# cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
#                       "Server=110HSAESSDBPW10;"
#                       "Database=HSAFSBPHI;"
#                       "Trusted_Connection=yes;")
# cursor = cnxn.cursor()
#
# for resultRow in cursor.execute("""
#                                 -- Using Today
#                                 SELECT 
#                                     FORMAT (GETDATE(), 'yyyyMMdd') AS [Todays Date]
#                                     ,DATEPART(YEAR, GETDATE()) AS [Callendar Year]
#                                     ,DATEPART(QUARTER, GETDATE()) as [Quarter of CY]
#                                     ,DATEDIFF(week, (SELECT DATEADD(yy, DATEDIFF(yy, 0, GETDATE()), 0)), GETDATE()) + 1 as [Week Number]
#                                     ,DATENAME(DW, GETDATE()) as [Week Day Name];"""):
#     #pp(cursor.description)
#     #print(resultRow)
#     print('-' * 106)
#     print('CY{}, Q{}, Week #{}'.format(resultRow[1], resultRow[2], resultRow[3]))
#     print('-' * 106)
#     print('{} - {}'.format(resultRow[0], resultRow[4]))

# Generate header(No DB) (wip)
# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior



def main():
    
    commandLineArgsDic = parse_cli_args()
    if commandLineArgsDic["days_to_subtract"]:
        print("Using days_to_subtract to offset")
        days_to_subtract = int(commandLineArgsDic["days_to_subtract"])
        myTime = datetime.today() - timedelta(days=days_to_subtract)
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
        print('''	* ITP Specific Tasks: 2509010, 2508010: 2.5
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
        taskStringList = get_file_contents('formattingDB.txt')

        #pp(taskStringList[5:25])
        print('	* ITP Specific Tasks: 2509010, 2508010: 2.5')
        print('\t' * 2 + taskStringList[5])

if __name__ == '__main__':
    while True:
        main()
        time.sleep(5)






##################
# REFERENCE CODE #
##################
# Generate for specific day (wip)
# for resultRow in cursor.execute("""
#                         DECLARE @DateString VARCHAR(10) 
#                         SET @DateString = '04/01/2021' 
#                         SELECT 
# 	                        @DateString as [Selected Date] 
# 	                        ,DATEPART(YEAR, @DateString) AS [Callendar Year] 
# 	                        ,DATEPART(QUARTER, @DateString) as [Quarter of CY]  
# 	                        ,DATEDIFF(week, (SELECT DATEADD(yy, DATEDIFF(yy, 0, @DateString), 0)), @DateString) + 1 as [Week Number];"""):
#     pp(cursor.description)
#     print(resultRow)

# for i in cursor.execute('SELECT \
# 	DATEPART(YEAR, GETDATE()) AS [Callendar Year] \
# 	,DATEPART(QUARTER, GETDATE()) as [Quarter of CY] \
# 	,DATEDIFF(week, (SELECT DATEADD(yy, DATEDIFF(yy, 0, GETDATE()), 0)), GETDATE()) + 1 as [Week Number];'):
#     print(i)

# for i in errorTupList:
#    cursor.execute("INSERT INTO ivk_RCOErrorChargesParsed_20200922(fileNumber, fac, uploadErrorDate, errorNumber ,errorReason, acct, chargeSvcDate, chargeCode, sourceOfRequest, quantity, creditFlag, fileName) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11])
#    cnxn.commit()
# cursor.close()

#pp(get_file_contents('formattingDB.txt', isKeepNewLineChar=False))