# commands/upload_images.py

import click
import boto3
import os
import uuid
import requests

from .login_to_cognito import login

# Configure Boto3 to use your AWS credentials
boto3.setup_default_session()


def upload_image_to_s3(image_path, bucket_name, virtual_path_prefix, s3_client):
    image_key = f"{virtual_path_prefix}{uuid.uuid4()}{os.path.splitext(image_path)[1]}"
    s3_client.upload_file(image_path, bucket_name, image_key)
    return image_key


def post_graphql_create_image(name, key, path, endpoint, id_token):
    mutation = """
    mutation CreateImage($input: CreateImageInput!) {
        createImage(input: $input) {
        ...ImageFragment
        benchmarkScores
        __typename
        }
    }

    fragment ImageFragment on Image {
        id
        name
        key
        paths
        folderIDs
        projectIDs
        permissionLookup
        scores
        color
        createdAt
        updatedAt
        owner
        size
        benchmarks {
        items {
            benchmarkID
            id
            imageID
            benchmark {
            name
            __typename
            }
            __typename
        }
        __typename
        }
        tags(limit: 25) {
        items {
            tag {
            label
            id
            __typename
            }
            tagID
            imageID
            id
            __typename
        }
        __typename
        }
        size
        __typename
    }
    """
    variables = {
        "input": {"name": name, "key": key, "path": path},
        "activeWorkspaceID": "1042f646-2849-45ab-9366-e1f5caa8ca67",
    }
    payload = {
        "operationName": "CreateImage",
        "query": mutation,
        "variables": variables,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {id_token}",
    }
    response = requests.post(
        endpoint,
        json=payload,
        headers=headers,
        timeout=30,
    )
    return response.json()


@click.command()
@click.option(
    "--images",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Directory with image files",
)
@click.option(
    "--bucket",
    required=True,
    default="uploads-241413258911-ent-dev",
    help="S3 bucket name",
)
@click.option(
    "--endpoint",
    required=True,
    default="https://2lw75t7ozjernbgedxz3kx3xdy.appsync-api.us-east-1.amazonaws.com/graphql",
    help="GraphQL API endpoint",
)
@click.option(
    "--virtual-path-prefix",
    default="public/",
    help="Prefix for virtual path in the application",
)
def uploadimages(images, bucket, endpoint, virtual_path_prefix):
    """
    Uploads images from the specified directory to S3 and creates image records via GraphQL.
    """
    print("hello")
    id_token = login()
    print("you have veen logged into Cognito", id_token)

    s3_client = boto3.client("s3")

    for image_file in os.listdir(images)[2000:]:
        if not image_file.lower().endswith(
            (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")
        ):
            continue
        image_path = os.path.join(images, image_file)
        print(f"Uploading image: {image_path}")
        image_key = upload_image_to_s3(
            image_path, bucket, virtual_path_prefix, s3_client
        )
        print("Image uploaded to S3:", image_key)
        virtual_path = f"{virtual_path_prefix}{image_key}"
        graphql_response = post_graphql_create_image(
            image_file, image_key, virtual_path, endpoint, id_token
        )
        # print response status
        print(graphql_response)


# This allows the command to be used as a module
if __name__ == "__main__":
    uploadimages()
