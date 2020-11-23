import boto3
import os


client = boto3.client(
    "sns",
    aws_access_key_id= '',
    aws_secret_access_key= '',
    region_name= "us-east-2"
)
def sendtext(userphone, usersname):
    userphonenumber = '1' + userphone
    client.publish(
        PhoneNumber=userphonenumber,
        Message="Thanks for joining Clup " + usersname + "!"
 )
def enterqueue(userphone, storename):
    userphonenumber = '1' + userphone
    client.publish(
        PhoneNumber=userphonenumber,
        Message="You are now in queue for " + storename + "."
    )

