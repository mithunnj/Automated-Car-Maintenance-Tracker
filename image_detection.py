#!/usr/bin/env python3
'''
This file will contain all code related to the image detection functionality of this tool.
'''
   
from PIL import Image, ExifTags
from GPSPhoto import gpsphoto
from datetime import datetime
import pytesseract
import cv2
import numpy
import os
import sys
import json

try:
    VIN = os.environ['VIN']
except:
    sys.exit('Set VIN environment variable manually.')

try:
    os.environ['GOOGLE_APPLICATION_CREDENTIALS']
except:
    sys.exit('Set the authentication token for GOOGLE_APPLICATION_CREDENTIALS as specified in:  https://cloud.google.com/vision/docs/setup')

# Directories for the VIN and MILEAGE images.
CWD = os.path.dirname(os.path.abspath(__file__)) 

def coordinate_processing(image):
    '''
    Input: image <str> - Contains the filepath to the image.
    Output: latitude <str> - Concatenated to 5 decimal places.
        longitude <str> - Concatenated to 5 decimal places.

    Description: Parse GPS location in Exif format and return latitude and longitude rounded to 5 decimal places.
    '''
    # Fetch GPS metadata in Exif format.
    data = gpsphoto.getGPSData(image)

    # Concantenate to the coordinates to 5 decimal places.
    latitude = format(data['Latitude'], '.5f')
    longitude = format(data['Longitude'], '.5f')

    return latitude, longitude

def metadata(filepath):
    '''
    Input: filepath <str> - Contains the relative path to the image for processing.
    Output: <arr> - List in the following format: [time, latitude, logitude] metadata information.

    Description: Given image filepath, return the time, latitude and longitude metadata.
    '''
    img = Image.open(filepath)
    metadata = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS } # Create a dict containing all the metadata information available from phone image.

    # Parse the metadata information for time, and location of the photo.
    time = metadata['DateTimeOriginal'] 
    latitude, longitude = coordinate_processing(filepath)

    return [time, latitude, longitude]

def coordinate_diff(coordinate1, coordinate2):
    '''
    Input: <str> coordinate1, coordinate2: The coordinate (either latitude or longitude) of image1 and image2.
    Output: <float> - The absolute value of the difference between the coordinate values.

    Description: Take the coordinates and calulate the difference between them. Return a positive value for the distance.
    '''

    return abs(float(coordinate1) - float(coordinate2))

def valid_photo(filepath_list):
    '''
    Input: <list> filepath_list - List containing the two image paths containing the vehicle VIN and the mileage.
    Output: <bool> - True if the images pass the distance and time constraints, False otherwise.

    Description: Take two image file paths (first - vehicle VIN, second - vehicle mileage), and validate the images by checking distance and time constraints.
    '''
    image_metadata_store = [] # Will contain the metadata associated to each image.

    # Fetch metadata information for each image in the form [time, latitude, longitude]
    for image in filepath_list:
        image_metadata_store.append(image)
        image_metadata_store.append(metadata(image))

    # Two step process, will require only 2 images each time for the process.
    # Validate that the images were taken on the same date. Allow for +- 2 min buffer.
    fmt = '%Y:%m:%d %H:%M:%S'
    fulldate1 = image_metadata_store[1][0]
    fulldate2 = image_metadata_store[3][0]
    d1 = datetime.strptime(fulldate1, fmt)
    d2 = datetime.strptime(fulldate2, fmt)
    minDiff = int(str((d2-d1)).split(':')[1]) # Detemine the time difference in minutes.

    if (minDiff >= 2):
        return False

    # Validate that the images were taken of the same car based on the location of image. All for +- 0.005 variability.
    lat1 = image_metadata_store[1][1]
    lat2 = image_metadata_store[3][1]
    long1 = image_metadata_store[1][2]
    long2 = image_metadata_store[3][2]

    if (coordinate_diff(lat1, lat2) >= 0.005) or (coordinate_diff(long1, long2) >= 0.005):
        return False

    return True

def detect_text(path):
    '''
    Input: <str> path - Image file path.
    Output: <str> - The parsed text from the image with the whitespace before, after and inside the string, removed.

    Description: Leverage the Google Cloud Vision API to detect the text in the images. Parse the output of the API which is in the following form:
    [locale: "en"
        description: "5421 km\n"
        bounding_poly {
        vertices {
            x: 113
            y: 537
        }
        vertices {
            x: 917
            y: 537
        }
        vertices {
            x: 917
            y: 761
        }
        vertices {
            x: 113
            y: 761
        }
        }
        ...
    '''
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    # Return the first entry of the JSON - which refers to the text detected in the image. Remove all white spaces before, after and within the string.
    return texts[0].description.replace(" ","").strip()

def MILEAGE_processing(image_path):
    '''
    Input: <str> image_path -  The file path to the image.
    Output: <str> - The parsed output from the text in the image detection.

    Description: Given an image of the mileage, use the Py-Tesseract module to extracted the mileage from the image.
    '''

    # Open image, and rotate the image.
    image = Image.open(image_path)

    # Crop the image of the mileage for further processing.
    image_crop = (750, 1000, 1500, 2000)

    # Crop the rotated image.
    crop = image.crop(image_crop)

    # Save the cropped image, and feed it into CV API.
    save_fp = './PROCESSED/' + os.path.basename(image_path)
    crop.save(save_fp)
    text = detect_text(save_fp)

    return text

def latest_MILEAGE():
    '''
    Input: None
    Output: <str> mileage - Filepaths for the image of the mileage.

    Description: Fetch the latest image uploaded in the IMAGE folder.
    '''
    image = [CWD + '/images/' + relative_path for relative_path in os.listdir('./images')]

    return max(image, key=os.path.getctime)


def MAIN_data_processing():
    '''
    Input: None
    Output: <bool>, <str> detected_vin, <str> detected_mileage: Return True if there was a VIN match to validate the information. 
        Return the parsed vin and mileage information from the image.

    Description: This is the main task execution for this module. You can just import this function in subfiles.
    '''

    # Get the latest MILEAGE image.
    mileage = latest_MILEAGE()

    # Process the image of the MILEAGE
    detected_mileage = MILEAGE_processing(mileage)

    # Return the detected mileage in string format.
    return detected_mileage

    

