from google.cloud import firestore
from google.oauth2 import service_account
import requests
import json
import boto3

def handler(event, context):
    ssm = boto3.client("ssm")
    try:
        credentials_info_str = ssm.get_parameter(Name="gcp-key", WithDecryption=True)
    except:
        return "Could not get keys"
    
    credentials_info_str = credentials_info_str["Parameter"]["Value"]
    credentials_info = json.loads(credentials_info_str)
    
    try: 
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
    except:
        return "Could not authenticate keys"

    try:
        db = firestore.Client(project=credentials.project_id, credentials=credentials)
    except:
        return "Could not connect to firebase"

    try:
        response = requests.get(
            "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
        )
        response = response.json()
    except:
        return "Could not retreive joke data"

    try:
        doc_ref = db.collection("jokes").document(str(response["id"]))
    except:
        return "Could not insert joke id"

    try:
        if response["type"] == "twopart":
            doc_ref.set({"setup": response["setup"], "delivery": response["delivery"]})
        else:
            doc_ref.set({"joke": response["joke"]})
    except:
        return "Could not add attributes to joke id"

    return response
