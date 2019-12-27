#!/usr/bin/env python3
'''
This contains the main script execution to handle the task.
'''
from message_handler.message_handler import request_mileage, post_request
from image_detection import MAIN_data_processing
from time import sleep
import sys
import datetime

# Conversion factor for mileage
MILE_TO_KM = 1.609

# Coloured text
CGREEN = '\33[32m'
CRED = '\33[31m'
CEND = '\033[0m'
CYELLOW = '\33[33m'

def create_log(miles, kms, manual=False, date=None):
    '''
    Input: <int> miles, <int> kms - The mileage in both units of measurement.
    Output: None

    Description: Create a log file in the ./LOGS directory of the miles and kms that were stored for that date. 
        Also create a back up log of the file in the ./LOGS/BACKUP folder.
    '''
    today = datetime.datetime.now().strftime("%Y-%m-%d") if not manual else date
    log_title = "Mazda3_mileage_log"

    # Write to the main log.
    with open('./LOGS/{}.txt'.format(log_title), 'a') as log_file:
        write_list = [today, str(miles)+'mi', str(kms)+'km']
        log_file.write(" ".join(write_list))
        log_file.write('\n')

    log_file.close()

    # Write an individual text file entry as a backup.
    with open('./LOGS/BACKUP/{}.txt'.format(today), 'w+') as backup_file:
        write_list = [today, str(miles)+'mi', str(kms)+'km']
        backup_file.write("\n".join(write_list))

    backup_file.close()

    return

def mileage_conv(mileage):
    '''
    Input: mileage <str> - Mileage in the format: 1234mi or 1234km
    Output: kms_mileage, miles_mileage <int> 

    Description: Take mileage in string format, determine if it is Miles (mi) or Kilometers (km) and return the converted mileage
        in both units.
    '''
    if 'mi' in mileage:
        miles_mileage = int(mileage.split('m')[0])
        kms_mileage = int(float(miles_mileage) * MILE_TO_KM)
    else:
        kms_mileage = int(mileage.split('k')[0])
        miles_mileage = int(float(kms_mileage) / MILE_TO_KM)

    return kms_mileage, miles_mileage

def manual_input():
    '''
    Input: None
    Output: None

    Description: A manual mileage entry will require the mileage information in either Miles or Kilometers, and the date of the entry in the following
        format: <year>-<month>-<day> ex. 2019-12-25. Take that information and store it on the backend and in the log files.
    '''
    # Ask user for the mileage
    mileage = str(input('\n' + 'Input mileage in the following format ex. 1234mi OR 1234km: ')).strip()
    date = str(input('\n' + 'Input date in the following format: <year>-<month>-<day> ex. 2019-12-25: ')).strip()

    # Get the km and mi version of the mileage
    kms_mileage, miles_mileage = mileage_conv(mileage)

    # Submit a POST request to the backend server
    post_request(miles_mileage, kms_mileage, True, date)

    # Create a log of the mileage with a timestamp
    create_log(miles_mileage, kms_mileage, True, date)

    print('\n' + CGREEN + 'Successfully stored the following mileage: KMS - {}, MI - {} for {}.'.format(kms_mileage, miles_mileage, date) + CEND + '\n')


def task_execution():
    '''
    Input: None
    Output: date <datetime> - This today's date in year-month-day form.

    Description: This is the main task execution. Once it sends a text to the recipient, it will process the image 
        to retrieve and store the mileage information.
    '''
    # Send text to user to send a MMS of the mileage of the vehicle.
    request_mileage() 

    # When the user sends back an MMS, the Flask Python server will process the image and save it to ./images

    # Process the image and send a string. Wait until the user sends back an image of the mileage.
    while True:
        try:
            mileage = MAIN_data_processing()
            break
        except Exception as e:
            #print('The error is: {}'.format(e)) #NOTE: Uncomment for further debugging.
            print('\n' + CRED + 'Waiting for data!' + CEND + '\n')
            sleep(10)
            continue

    # Determine the mileage in miles and kms
    kms_mileage, miles_mileage = mileage_conv(mileage)

    # Submit a POST request to the backend server
    post_request(miles_mileage, kms_mileage)

    # Create a log of the mileage with a timestamp
    create_log(miles_mileage, kms_mileage)

    # Return the date this task was processed
    return datetime.date.today()

def main():

    # If option is passed in - ask user to input mileage value manually. 
    if sys.argv[1] == 'm':
        print('\n' + CYELLOW + 'Manual mileage logging selected.' + CEND + '\n')
        
        # Keep asking user for information to store manually until they specify that they are done.
        while True:
            manual_input()
            user = input('\n' + CYELLOW + 'If you have more entries select [y]. If you are done select [n]: )' + CEND + '\n')
            
            if user == 'n':
                sys.exit('Thank you for your information! -  Exiting')

    else:
        # Date the task was processed
        PROCESSED_DATE = ''

        while True:
            # Determine how long has passed since the task was last run
            if PROCESSED_DATE:
                date_difference = (datetime.date.today() - PROCESSED_DATE).days
            else:
                date_difference = 0

            print('Mit: {}'.format(date_difference))

            # If the task has never been run, or if it has been more than 2 weeks since we ran it, execute the task.
            if not PROCESSED_DATE or (date_difference >= 14):
                print('\n' + CGREEN + '{} days since last update - Requesting user now!'.format(date_difference) + CEND + '\n')
                PROCESSED_DATE = task_execution()
            else:
                print('\n' + CRED + 'Will request new update in {} days'.format(abs(14 - date_difference)) + CEND + '\n')
            
            print('\n' + CYELLOW + 'Processed - now going to sleep.' + CEND + '\n')
            # Sleep for 12 hours and check how much time has passed.
            sleep(12*60)

main()