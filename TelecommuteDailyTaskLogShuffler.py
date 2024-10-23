from datetime import datetime, timedelta
from pprint import pprint as pp
import helpers
import sys
''' 1. Extract tasks for the day. [x]
    2. Parse the text into dict structure
    3. Shuffle tasks and sections. [ ] '''

def main():
    taskStringList = helpers.get_file_contents('C:\\Users\\e618071\\OneDrive - County of Los Angeles\\Documents\\HR\\DailyTeleworkLog\\PWL20240923toPresent.txt', isKeepNewLineChar=False)
          
    # Confirm that today's date exists
    # TODO: Make work for relative dates
    if not [x for x in taskStringList if datetime.today().strftime('%Y%m%d') in x[:8]]:
        print("Today's date not found.")
        sys.exit("Today's date not found.")
    
    # Get line marker for section start and end
    toDoSectionStartIndex = 0
    nextSectionStartString = ''
    toDoSectionEndIndex = 0

        
    # Strart Index
    for index, i in enumerate(taskStringList):
        #pp(i[:8])
        if i[:8] == datetime.today().strftime('%Y%m%d'):
            #print(i)
            toDoSectionStartIndex = index
            break
    #print('toDoSectionStart:', toDoSectionStartIndex)


    # End Index
    for index, i in enumerate(taskStringList[toDoSectionStartIndex+1:]):
        #pp(i[:8])
        try: 
            if int(i[:8]):
                #print(i)
                nextSectionStartString = i
                break
        except:
             pass
        
    for index, i in enumerate(taskStringList):
        if i == nextSectionStartString:
             toDoSectionEndIndex = index
             
             
    

    #print('toDoSectionStart:', toDoSectionStartIndex)
    #print('nextSectionStartString:', nextSectionStartString)
    #print('toDoSectionEnd:', toDoSectionEndIndex)
    #pp(taskStringList[toDoSectionStartIndex:toDoSectionEndIndex])
    for i in taskStringList[toDoSectionStartIndex:toDoSectionEndIndex]:
        print(i)

if __name__ == '__main__':
        main()