# Section 1: Project Title
Smart Librarian

# Section 2: Executive Summary
The impact of Covid 19 has turned many businesses online and people toward activities that can be done individually and at home. The online book service market, is not an expectation to this trend, with an annual compounded growth of 6.2% per annum with an expectation to reach 23.8 Billion in 2026.

Major industry players in the fragmented ebook market that had a foothold in the ebook market also made moves to consolidate their position. For example, Amazon.com, offered the users a free trial of two months on their “Kindle Unlimited” service since June 2020 in an attempt to on board more users.
Most major players in the ebook market seeks to earn revenue by offering ebooks for sale or via a subscription model that offers a spectrum of books for download.

The Smart Librarian seeks to disrupt the market by offering the books for free through the NLB ebooks collection. The recommendation system also provides an additional feature to borrow/read the next book.

# Section 3: Credits
Full Name | Student ID | Areas of Responsibility
-|-|-
Yang Jieshen | A0003901Y | Conversational UI, Email RPA and Integration
Onn Wei Cheng | A0092201X | NLB Availablity Checker & Amazon Recommendation System
Nirav Janak Parikh | A0213573J | Intelligent Smart Title Matcher & Abstract Summariser

# Section 4: Video
### Promotional Video of Smart Librarian:
[![IMAGE ALT TEXT]()

### High Level System Design of Smart Librarian:
[![IMAGE ALT TEXT]()


# Section 5: Installation & User Guide
CookWhatAh rides on a Telegram application as the user interface to implement our system. Please install Telegram in your respective platforms to run the application.

### Installation instructions for Smart Librarian:
1.	Clone Github repository to location of choice
Note: Make sure file path does not have any spaces.

2.	Download GoogleNews-vectors-negative300.bin from https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
Note: This file is 3GB big

3.	Extract(unzip) and place GoogleNews-vectors-negative300.bin into “DialogFlow” folder

4.	Install system with Python 3.8.2.

5.	Run “install.bat” to install all required python packages

6.	If using own account and not the credentials provided, will need to import SmartLibrarian agent through the zip file provided in Github. If test is to be done on Google Assistant, integration setup with Google Assistant needs to be done under “Integrations” tab.
DialogFlow link: https://dialogflow.cloud.google.com/

For the provided credentials, all setup in dialogflow is done, including Google Assistant integration

7.	Log in to gmail account using tagui browser which is used to send the NLB email


### User Guide:
1.	Run “ngrok.bat”. Extract https tunnel link

2.	Paste and save https link into dialogflow fulfillment https://dialogflow.cloud.google.com/#/agent/librarian-qusu/fulfillment

3.	Run “run.bat”. 
Note: Webhook takes around 6mins to initialize the models.

4.	SmartLibrarian is ready for use!

5.	[Test Platform] Try it out using DialogFlow test console or, download Google Assistant on your device, log in using respective credentials, and initialize the agent by typing/saying “Talk to Smart Librarian”

6.	[Email Recipient] By default, email recipient is set to the gmail account that is logged in. To change the email recipient of the results of the NLB search, go to “DialogFlow” folder and add in the email address in “email_recipient.txt”

# Section 6: Group Report
Please refer to ProjectReport folder in the repository.
