#!/usr/bin/env python
import click
from commands.query import query

# from commands.update import update
# from commands.put import put


@click.group()
def cli():
    """DynamoDB CLI Tool"""
    pass


# Register commands
cli.add_command(query)
# cli.add_command(update)
# cli.add_command(put)

if __name__ == "__main__":
    cli()
