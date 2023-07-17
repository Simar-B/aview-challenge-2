# aview-challenge-2

## Installation
- Clone the repo
- build the docker image and tag it

## Run Application
- Create a GCP account and make a Firestore database
- Get a json key that has access to read/write to Firestore database
- Upload the built docker image to an ECR repo
- Create a parameter in Parameter store that is encrypted and call it `gcp-key`. Make the value equal to a string of the contents of the json file obtained in step 2.
- Create a lambda function that uses the docker image that was uploaded to the ECR repo as the source, make sure it has permission to access Parameter Store
- Create a function url for the lambda after it is created

**Note** the lambda function returns the joke that was retreived from the API. So, you can check that the joke that was returned was inserted into the database.

## Test
- Trigger the lambda by sending an http request to the function url
- You can check the Firestore database for the joke to be inserted

## Approach
My approach to this challenge was to make the architecture secure and simple as possible, since the content of the challenge was relatively easy.

Since the challenge required the use of a GCP NoSQL database, I decided to use Firestore as the main database. I saw Firestore was advertised as an improved Datastore, so I went with it. Either way, Datastore probably would have been fine too, so the choice of database was not hyper critical.

The code is relatively straight forward. It is mainly 3 steps, which are authenticate, retreive the joke, and store the joke in the database. For each major step, I have a try catch for any exception handling. 

One challenge I had for this was how to pass the credentials to access the GCP database in AWS Lambda. On my first iteration, I decided to pass the json file key as a string in the environment variables for the function. However, I realized this is not the best practice as the key is available in the AWS console for anybody to see.

Therefore, I decided to use Parameter Store as it is part of the AWS free tier and solves the problem stated above. Therefore, I used the boto3 client to be able to access the `gcp-key` from the parameter store which stores the credentials for the gcp key as a string. I then load the string as json object and pass it into the gcp client to authenticate.

## Other comments
I consulted the following resources for this assessment which may be helpful for running and installing the application:
- https://docs.aws.amazon.com/lambda/latest/dg/python-image.html#python-image-instructions
- https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameter.html
