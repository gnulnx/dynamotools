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
@click.option(
    "--images",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Directory with image files",
)
# @click.option("--bucket", required=True, help="S3 bucket name")
@click.option(
    "--endpoint",
    required=True,
    default="https://2lw75t7ozjernbgedxz3kx3xdy.appsync-api.us-east-1.amazonaws.com/graphql",
    help="GraphQL API endpoint",
)
# @click.option(
#     "--virtual-path-prefix",
#     default="uploaded_images/",
#     help="Prefix for virtual path in the application",
# )
def uploadimages(images, endpoint):
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
