# pylint: disable=broad-except
import fnmatch
import click
import boto3
from commands.colors import color_yellow

dynamodb_client = boto3.client("dynamodb")


def highlight_pattern(text, pattern, highlight_func):
    """Highlight the pattern in the text for simple wildcard patterns."""
    start, _, end = pattern.partition("*")
    if start and text.startswith(start):
        text = highlight_func(start) + text[len(start) :]
    if end and text.endswith(end):
        text = text[: -len(end)] + highlight_func(end)
    return text


@click.command()
@click.option("--pattern", default="*", help="Wildcard pattern to match table names.")
def list_tables(pattern):
    """List DynamoDB tables matching the given pattern."""
    try:
        # Initialize variables
        all_tables = []
        last_evaluated_table_name = None

        # Fetch all table names with pagination
        while True:
            if last_evaluated_table_name:
                response = dynamodb_client.list_tables(
                    ExclusiveStartTableName=last_evaluated_table_name
                )
            else:
                response = dynamodb_client.list_tables()

            all_tables.extend(response.get("TableNames", []))

            # Check if there are more tables to fetch
            last_evaluated_table_name = response.get("LastEvaluatedTableName")
            if not last_evaluated_table_name:
                break

        # Apply wildcard pattern
        matched_tables = fnmatch.filter(all_tables, pattern)

        for table in matched_tables:
            # Highlight the matching pattern in each table name
            highlighted_table = highlight_pattern(table, pattern, color_yellow)
            click.echo(highlighted_table)
    except Exception as e:
        click.echo(f"An error occurred: {e}")
