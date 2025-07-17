#pip install requests, dotenv, 
#pip install google-api-python-client, google-auth-httplib2, google-auth-oauthlib
#To-Do. Go over With User  the script, ask how we want to setup
#Setup .env file
#Setup credentials.json from google https://developers.google.com/workspace/gmail/api/quickstart/python
#Setup Task Scheduler

import requests
from dotenv import load_dotenv
import os

import os.path
from email.message import EmailMessage
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def composeGmail(checkedOutIpads):
    SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]
    creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
    if os.path.exists("token.json"):
        try:
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        except Exception as e:
            print(f"Corrupted token.json: {e}")
            creds = None

    # If no valid creds, go through OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Token refresh failed: {e}")
                creds = None
        if not creds or not creds.valid:
            try:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            except Exception as e:
                print(f"Login failed: {e}")
                exit(1)

    # 3. Save the token only if we got valid creds
        if creds and creds.valid:
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        else:
            print("Could not obtain valid credentials.")
            exit(1)
    try:
            # Call the Gmail API
            service = build("gmail", "v1", credentials=creds)
            for user in checkedOutIpads:
                name = user['name']
                to_email = user['email']
                description = user.get('description', 'your device')
                body = f"Hi {name},\n\nThis is a friendly reminder to return the following iPad:\n{description}\n\nPlease return it as soon as possible, and let us know if you have any questions.\n\nThanks,\nUser"
                message = EmailMessage()
                message.set_content(body)
                message['To'] =  to_email,
                message['Cc'] = 'Ask Avi'
                message['From'] = 'Ask Avi'
                message['Subject'] = "iPad Return Reminder"
                encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
                create_message = {"message": {"raw": encoded_message}} #comment when sending uncomment while drafting
                print(f'Draft id: {draft["id"]}') # comment when sending uncomment while drafting
                print(f'Draft message: {draft["message"]}') # comment when sending uncomment while drafting
                draft = service.users().drafts().create(userId='me', body=create_message).execute() #comment when sending. uncomment while drafting
                #draft = service.users().messages().send(userId='me', body={"raw": encoded_message}).execute() #uncomment when sending
                #print(f'Message Id: {send_message["id"]}')# uncomment when sending
    except HttpError as error:
            print(f'An error occurred: {error}')
            exit


def getRequest(headers, url):  # API GET Request with pagination. See https://api.assetbots.com/index.html for more info
    all_data = []
    limit = 1000
    offset = 0
    while True:
        modifiedURL = f"{url}&limit={limit}&offset={offset}"
        #print(modifiedURL)
        try:
            response = requests.get(modifiedURL, headers=headers)
            if response.status_code == 200:
                #print(f"Request successful! Offset: {offset}")
                data = response.json().get("data", [])
                if not data:
                    break  # No more data returned from the API
                all_data.extend(data)
                offset += limit
            else:
                print(f"Request failed with status code: {response.status_code}")
                exit()
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            exit()
    #print(all_data)
    return all_data

def getCheckedOut (data): #Function that process JSON response to get specfically MS SPARE descriptions and Checked Out devices
    #print(response.json()["data"][0]["description"])
    # Might want code segment if we want to just look at labels instead of item description
    # for label in item["labels"]:
    #print(item["labels"][0]["value"]["name"]) 
    loaners = [] #list for checked out IPads
    for item in data:
        if "MS Spare" in item.get("description", ""):
            if item.get("checkout") and item["checkout"].get("value", {}).get("status") == "CheckedOut":
                loaners.append({"name":item["checkout"]["value"]["person"]["value"]["name"], "email": item["checkout"]["value"]["person"]["value"]["email"], "description": item["description"]})
                print(f"{item["description"]} Checked out to: {item["checkout"]["value"]["person"]["value"]["email"]}")
            else:
                print(f"{item["description"]} Not checked out")
    return loaners

load_dotenv()  # load environment variables from .env.
api_key = os.getenv("API_KEY")

checkedOutIpads = getCheckedOut(getRequest(headers = {'Authorization': 'Bearer ' + api_key,}, url = "https://api.assetbots.com/v1/assets?")) #needed to make get requests for Assetbot API
composeGmail(checkedOutIpads)
