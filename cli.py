#!/usr/bin/env python
import click
from commands import (
    query,
    list_tables,
    _login,
    uploadimages,
    _assume_search_role,
    # update,
    # put,
)


@click.group()
def cli():
    """DynamoDB CLI Tool"""


# Register commands
cli.add_command(query)
cli.add_command(list_tables)
cli.add_command(_login)
cli.add_command(uploadimages)
cli.add_command(_assume_search_role)
# cli.add_command(update)
# cli.add_command(put)

if __name__ == "__main__":
    cli()
