import boto3
import requests
from jprint import jprint
import click


def login():
    APPSYNC_API_URL = (
        "https://2lw75t7ozjernbgedxz3kx3xdy.appsync-api.us-east-1.amazonaws.com/graphql"
    )
    # AWS Cognito credentials
    USERNAME = "john@vizit.com"
    PASSWORD = "tga3CXZ-hmh2mqt@ypz"
    CLIENT_ID = "1fj2tr6o8antjl9vgabn1ejrgs"

    # login to AWS Cognito
    client = boto3.client("cognito-idp")
    response = client.initiate_auth(
        ClientId=CLIENT_ID,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={"USERNAME": USERNAME, "PASSWORD": PASSWORD},
    )

    id_token = response["AuthenticationResult"]["IdToken"]

    return id_token


@click.command(name="login")
def _login() -> str:
    """Login to Cognito"""

    id_token = login()
    print("id_token: ", id_token)
    print("you have veen logged into Cognito")

    return id_token

    print("you have veen logged into Cognito")
    print("you session token is: " + id_token)
    # return id_token

    api_url = (
        "https://2lw75t7ozjernbgedxz3kx3xdy.appsync-api.us-east-1.amazonaws.com/graphql"
    )
    query = """
    {
    __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types { name }
    }
    }
    """

    # Make the request
    headers = {"Authorization": f"Bearer {id_token}"}
    response = requests.post(
        api_url, json={"query": query}, headers=headers, timeout=10
    )

    # Print the response
    jprint(response.json())
