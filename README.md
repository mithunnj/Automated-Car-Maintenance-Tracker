# Automated Car Maintenance Tracker

This script is meant to automate the logging and storing of mileage information for my car. Bi-weekly, the script will send me a text - requesting an image of the mileage of the vehicle. I reply to the text via MMS, and reply back with an image of the mileage in Miles or Kilometers. The script processes the image, and parses the text of the mileage. It will then store that information for the webapp to access, and will store the information locally in a text file as a backup. 

## Steps taken to design and implement this solution.

1. Take image of the VIN and mileage, and use Image Detection algorithm to determine both values.

2. Validate that the mileage claims are true by leveraging camera metadata to verify that it is true.
	- Can be achieved by using the following validation:
	a) time - The pic should be taken within a minute of eachother. 
		- This will ensure that we're not spoofing the mileage data with old information. 
		- To make sure that someone doesn't keep using the same old pic of the VIN to keep updating the mileage. It must be a two-step process.
	b) location - The pic of the VIN and mileage must be within a really small radius because the VIN is on the fron windshield, and the mileage is on the drivers dash.

3. Make a PUT request to the backend server to store the information for the webapp. In addition, create a backup of the mileage with a timestamped text file in both miles and kms. 

4. Fall asleep and start task execution all over again once two weeks has passed.

## Notes:
- Justified rounding the latitude and longitude to 5 decimal places because of: https://www.google.com/search?q=how+many+decimal+places+matter+for+coordinates&oq=how+many+decimal+places+matter+for+coordinates&aqs=chrome.0.69i59j33.1483j0j4&sourceid=chrome&ie=UTF-8
- The allowable difference in location values was experimental (going to try it with 5 thousands tolerance first).

### Package dependencies:
- Pillow : https://pypi.org/project/Pillow/
- GPSPhoto: https://pypi.org/project/gpsphoto/
- ExifRead: https://pypi.org/project/ExifRead/
- piexif: https://pypi.org/project/piexif/0.7.1/
- Py-Tesseract: https://pypi.org/project/pytesseract/
	- Had to run the following commands additionally: https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i
		- brew install tesseract
		- pip3 install tesseract
- Google Cloud Vision API: https://cloud.google.com/vision/docs/setup
	- There is a lot to setup, so follow the instructions in that link.
	- pip install --upgrade google-cloud-vision
- ngrok: https://ngrok.com/download (You need to install it using the instructions on their site).
- NOTE: When starting your flask server to recieve MMS, make sure to run the following command: sudo flask run -h localhost -p 80 (as described in: https://stackoverflow.com/questions/41940663/why-cant-i-change-the-host-and-port-that-my-flask-app-runs-on)
	- Make sure that the port number matches the port number of ngrok as described here: https://www.twilio.com/blog/2018/05/how-to-receive-and-download-picture-messages-in-python-with-twilio-mms.html.

- Important notes for the final depolyment on the Apple server - NOTE: Create setup scripts to setup all the things below.
	1. You have to copy over the authentication.json file and keep that in the same location as the GOOGLE.. env variable that you set.
	2. Make sure to copy over the .gitignore file.
	3. Make sure to copy over the set_env.sh file.
	4. (This in the ./message_handler folder to start the MMS recieving server) Make sure to run : ./ngrok http 80 first, and update the webhook link in the Twilio console.
	5.  (This in the ./message_handler folder to start the MMS recieving server) Make sure to run: sudo flask run -h localhost -p 80, and it's important to run the sudo part of it. 
	6. And you have to make sure to start both the frontend and backend (app.py) in the web_app folder to make sure that this all works.

## Release notes
- BUG FIX: There were 2 issues that were the cause of this. 
	1. When you copy and paste the ngrok forwarding URL to Twilio, you forgot to include the '/sms' extention. This URL is specified in your Flask server to handle your message.
	2. You deleted the PROCESSED folder which should not be deleted. Stop indescriminately deleting files as part of your "refactoring". Always test out changes before refactoring.
