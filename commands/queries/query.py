import click
import fnmatch
import boto3
from botocore.exceptions import ClientError
from pygments import highlight
from pygments.lexers import TextLexer
from pygments.formatters import TerminalFormatter
from pygments.token import Token

from jprint import jprint


dynamodb_client = boto3.client("dynamodb")


def transform_dynamodb_item_to_json(dynamodb_item):
    """Converts DynamoDB item to regular JSON object."""
    json_item = {}
    for key, value in dynamodb_item.items():
        # DynamoDB returns a dictionary for each attribute value with its type as the key (e.g., 'S', 'N', 'L')
        data_type = next(iter(value))
        if data_type == "L":  # It's a List
            json_item[key] = [list(item.values())[0] for item in value[data_type]]
        elif data_type == "M":  # It's a Map
            json_item[key] = transform_dynamodb_item_to_json(value[data_type])
        else:  # It's a Scalar (S, N, BOOL)
            json_item[key] = value[data_type]
    return json_item


def extract_fields(data, fields):
    if not fields:
        return data
    field_list = fields.split(",")
    extracted = {}
    for field in field_list:
        keys = field.split(".")
        value = data
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                value = None
                break
        if value is not None:
            extracted[
                field.replace(".", "_")
            ] = value  # Replace dots with underscores for nested keys
    return extracted


@click.command()
@click.option("--table", prompt="Table name", help="The name of the DynamoDB table.")
@click.option(
    "--id", "item_id", prompt="Item ID", help="The ID of the item to retrieve."
)
@click.option(
    "--fields", help="Comma-separated list of fields to include in the output."
)
def query(table, item_id, fields):
    """Query an item in the table by ID."""
    try:
        response = dynamodb_client.get_item(
            TableName=table,
            Key={"id": {"S": item_id}},
        )
        item = response.get("Item", {})
        json_item = transform_dynamodb_item_to_json(item)
        item_to_display = extract_fields(json_item, fields) if fields else json_item
        # if fields:
        #     item_to_display = extract_fields(json_item, fields)
        # else:
        #     item_to_display = json_item
        jprint(item_to_display, sort_keys=True, indent=4)
    except ClientError as e:
        print(f"An error occurred: {e.response['Error']['Message']}")
