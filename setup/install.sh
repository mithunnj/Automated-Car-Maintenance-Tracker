#!/usr/bin/env bash

# Funky colors
red=`tput setaf 1`
cyan=`tput setaf 6`
green=`tput setaf 2`
yellow=`tput setaf 3`
bold=`tput bold`
reset=`tput sgr0`

# Give a welcome message to the start of the install script.
echo
echo "${yellow} ✌ Install script for Automated Maintenance Tracker by Mit! ✌ ${reset}"
echo

# Determine the OS and identify the method to install packages.
echo "${green} === Determining your OS... === ${reset}"
echo
OS="`uname`"
echo "${cyan} Your OS was detected to be: ${OS}${reset}"
# Set the install method for your packages/modules, only two options are Darwin (Mac OSX) and Linux
if [[ "$OS" == "Darwin" ]]
then
    INSTALL="brew install"
else
    INSTALL="sudo apt-get install"
fi
echo " The rest of the script will use ${bold}${INSTALL}${reset} to install packages."
echo

echo "${green} === Install Pillow (PIL) image handler ${bold}Python module ${reset} ${green} === ${reset}"
echo
pip3 install Pillow
echo

echo "${green} === Install GPSPhoto ${bold}Python module ${reset} ${green} === ${reset}"
echo
pip3 install gpsphoto
echo

echo "${green} === Install ExifRead ${bold}Python module ${reset} ${green} === ${reset}"
echo
pip3 install ExifRead
echo

echo "${green} === Install Piexif ${bold}Python module ${reset} ${green} === ${reset}"
echo
pip3 install piexif==0.7.1
echo

echo "${green} === Install Pytesseract ${bold}Python module ${reset} ${green} === ${reset}"
echo
pip3 install pytesseract
echo
${INSTALL} tesseract
echo
pip3 install tesseract
echo

echo "${green} === Instructions to do on your own === ${reset}"
echo
echo " Install ${bold}Google Cloud Vision API${reset} from this link: https://cloud.google.com/vision/docs/setup"
echo
echo "  - There are a lot of setup instructions including setting environment variables in order for this to work properly. ${bold}DON'T BE LIKE MY STUBBORN DAD${reset} and read the instructions carefully."
echo "  - At the end make sure to run the following: ${bold}pip install --upgrade google-cloud-vision${reset}"
echo
echo " Install ${bold}ngrok${reset}: https://ngrok.com/download (You need to install it using the instructions on their site)."
echo
echo " ${cyan}${bold}Some final advice before I leave you...${reset}${cyan} "
echo
echo " When starting your flask server to recieve MMS, make sure to run the following command: ${bold}sudo flask run -h localhost -p 80${reset} ${cyan}(as described in: https://stackoverflow.com/questions/41940663/why-cant-i-change-the-host-and-port-that-my-flask-app-runs-on)"
echo
echo " Make sure that the port number matches the port number of ngrok as described here: https://www.twilio.com/blog/2018/05/how-to-receive-and-download-picture-messages-in-python-with-twilio-mms.html.${reset}"
echo
echo "${green} === Thanks for installing this ! - Mit.J === ${reset}"
exit 0




