# commands/upload_images.py

import click
import boto3
import os
import uuid
import requests

from .login_to_cognito import login

# Configure Boto3 to use your AWS credentials
boto3.setup_default_session()


@click.command()
def uploadimages():
    """
    Uploads images from the specified directory to S3 and creates image records via GraphQL.
    """
    print("hello")
    id_token = login()
    print("you have veen logged into Cognito", id_token)
    input()


# This allows the command to be used as a module
if __name__ == "__main__":
    uploadimages()
