import argparse
import colorama
import datetime as dt
import os
import sys
import subprocess
from pprint import pprint as pp

def parse_cli_args():
    """ Setup and validate command line arguments.

    Returns:
    (dict) Dictionary of supplied command line arguments.
    """

    parser = argparse.ArgumentParser(description='Email Jobs Monitoring')
    parser.add_argument('-ds', '--days_to_subtract', required=False, metavar='',
                        help='Specify email date to check. Format YYYYMMDD.')
    parser.add_argument('-rd', '--relative', required=False, metavar='',
                        help='Check relative date. Format -x where x is number of days in the past from today.')
    argsDict = vars(parser.parse_args())

    #if argsDict['days_to_subtract'] and argsDict['relative']:
    #    print(red_color('Error:'), 'Use --date or --relative but not both. See usage.\n')
    #    parser.print_help()
    #    sys.exit()



    return argsDict
def parse_cli_args_Complicated():
    """ Setup and validate command line arguments.

    Returns:
    (dict) Dictionary of supplied command line arguments.
    """

    parser = argparse.ArgumentParser(description='Email Jobs Monitoring')
    parser.add_argument('-dt', '--date', required=False, metavar='',
                        help='Specify email date to check. Format YYYYMMDD.')
    parser.add_argument('-rd', '--relative', required=False, metavar='',
                        help='Check relative date. Format -x where x is number of days in the past from today.')
    argsDict = vars(parser.parse_args())

    if argsDict['date'] and argsDict['relative']:
        print(red_color('Error:'), 'Use --date or --relative but not both. See usage.\n')
        parser.print_help()
        sys.exit()

    if argsDict['date']:
        try:
            emailDate = dt.datetime.strptime(argsDict['date'], '%Y%m%d')
        except ValueError:
            print(red_color('Error:'), 'Date parameter supplied(' +
                  argsDict['date'] + ') is in an unexpected format. ' +
                  'See usage.\n')
            parser.print_help()
            sys.exit()

        try:
            if ((dt.datetime.now() - emailDate).days > 365 or
                    (dt.datetime.now() - emailDate).days < 0):
                raise ValueError()
        except ValueError:
            print(red_color('Error:'), 'Date parameter supplied(' +
                  argsDict['date'] + ') is outside expected date range. ' +
                  'See usage.\n')
            parser.print_help()
            sys.exit()

    return argsDict


def red_color(text):
    colorama.init()
    return colorama.Fore.RED + text + colorama.Style.RESET_ALL


def yellow_color(text):
    colorama.init()
    return colorama.Fore.YELLOW + text + colorama.Style.RESET_ALL


def get_file_contents(fileName, isKeepNewLineChar=True):
    if not os.path.isfile(fileName):
        print(red_color('Critical Error: ' + fileName + ' not found.'))
        raise OSError('Critical Error:', fileName, 'not found.')

    with open(fileName, 'r') as file:
        if not isKeepNewLineChar:
            fileContents = file.read().splitlines()
        else:
            fileContents = file.readlines()
        
    return fileContents


def check_for_unexpected_files(emailDate, fileNameList, exportEmailDir):
    fileList = os.listdir(exportEmailDir)
    todaysFileList = [file for file in fileList if emailDate in file]

    for file in todaysFileList:
        if file not in [expectedFile.format(emailDate) for
                        expectedFile in fileNameList]:
            print(red_color('Error:'), 'Unexpected file found:', file)


def is_today(emailDate):
    if emailDate == dt.datetime.now().strftime('%Y%m%d'):
        return True
    else:
        return False


def day_of_week(emailDate, integer=True):
    if integer:
        return int(dt.datetime.strptime(emailDate, '%Y%m%d').strftime('%w'))
    else:
        return dt.datetime.strptime(emailDate, '%Y%m%d').strftime('%A')


def time_of_day():
    return int(dt.datetime.now().strftime('%H%M'))


def check_if_file_scheduled(emailDate, expectedDays, expectedTimeOfDay, verbose=True):
    if expectedDays == 'M-F':
        expectedDays = [1, 2, 3, 4, 5]
    elif expectedDays == 'M-Sun':
        expectedDays = [0, 1, 2, 3, 4, 5, 6]

    if day_of_week(emailDate) not in expectedDays:
        if verbose:
            print("File isn't expected on", day_of_week(emailDate, integer=False))
        return False
    elif is_today(emailDate) and time_of_day() < expectedTimeOfDay:
        if verbose:
            print("File isn't expected today until", expectedTimeOfDay)
        return False
    else:
        return True


def check_email_datetme(expectedTime, expectedDate, emailDict):
    if abs(expectedTime - int(emailDict['sentDate'].strftime('%H%M'))) < 3:
        print('Email was sent at expected time.')
    else:
        print(red_color('Error:'), 'Email was sent at unexpected time.')
        print('\tExpected Time:', expectedTime)
        print('\tSent Time:', emailDict['sentDate'].strftime('%H%M'))
        # This is buggy. Taking out till fixed.
        # print('\tDifference in minutes:', abs(expectedTime - int(emailDict['sentDate'].strftime('%H%M'))))
    
    if expectedDate == emailDict['sentDate'].strftime('%Y%m%d'):
        print('Email was sent on expected date.')
    else:
        print('Email was sent on unexpected date.')
        print('\tExpected Date:', expectedDate)
        print('\tSent Time:', emailDict['sentDate'].strftime('%Y%m%d'))


def is_monitoring_reminder_running(programName='reminder.py'):
    isPythonwRunning = None
    outputLines = []

    cmd = 'wmic process get description'
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            universal_newlines=True)

    for line in proc.stdout:
        if 'python.exe' in line:
            isPythonwRunning = True

    if not isPythonwRunning:
        return False

    cmd = 'wmic process where caption="python.exe" get commandline'
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            universal_newlines=True)

    if any(programName in line for line in proc.stdout):
        return True
    else:
        return False


def compile_eParms_file_list():
    # Get list of files from SOURCE and BACKUP folders
    fileListInSource =  os.listdir(r'\\ttcmainapp2\EPARMS\SOURCE')
    fileListInSourceBackup =  os.listdir(r'\\ttcmainapp2\EPARMS\BACKUP\Source')
    fileListInRefundResponseBackup =  os.listdir(r'\\ttcmainapp2\EPARMS\BACKUP\RefundResponse')
    fileListInRefundStatus =  os.listdir(r'\\ttcmainapp2\EPARMS\REFUND_STATUS')
    fileListInImport =  os.listdir(r'\\ttcmainapp2\EPARMS\IMPORT')
    fileListInExport =  os.listdir(r'\\ttcmainapp2\EPARMS\EXPORT')

    combinedFileList = (fileListInSource +
                        fileListInSourceBackup +
                        fileListInRefundResponseBackup +
                        fileListInRefundStatus +
                        fileListInImport +
                        fileListInExport)
    cleanFileList = []

    # Removing batch number from file names
    for file in combinedFileList:
            cleanFileName = remove_number_from_file_name(file)
            cleanFileList.append(cleanFileName)

    return cleanFileList


def check_eParms_dirs_for_files(cleanEPARMSFileList, expectedFilesList):


    for f in expectedFilesList:
        if f in cleanEPARMSFileList:
            print(f, 'has been found in eParms')
        else:
            print(red_color('Error:'), f, 'is not in eParms')


def fridays_date_on_mondays(emailDateObj, fileNameDateFormat, fileNameTemplate):
    ''' Friday's date expected on Mondays.
    '''
    if int(emailDateObj.strftime('%w')) == 1:
        expectedFileName = fileNameTemplate.format((emailDateObj -
                                    dt.timedelta(days=3)).strftime(
                                    fileNameDateFormat))
    else:
        expectedFileName = fileNameTemplate.format((emailDateObj -
                                    dt.timedelta(days=1)).strftime(
                                    fileNameDateFormat))
    return expectedFileName


def remove_number_from_file_name(fileName):
    ''' If file name includes a random number, change digits to #s. 
    '''
    try: # Handling cases where parsing fails 
        if (fileName.split('_')[0].split('.')[1]).isdigit():
            correctFileName = fileName.replace(fileName.split('_')[0].split('.')[1],
                                    '#' * len(fileName.split('_')
                                                [0].split('.')[1]))
        else:
            correctFileName = fileName

    except IndexError:
        correctFileName = fileName
        
    return correctFileName


def main():
    pass


if __name__ == '__main__':
    main()
