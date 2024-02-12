# pylint: disable=missing-function-docstring
import functools
import boto3
from jprint import jprint
import os
import click

AOSS_ACCOUNT_ID = os.environ["AOSS_ACCOUNT_ID"]


@functools.lru_cache
def assume_search_role():
    sts = boto3.client("sts")

    role_keys = sts.assume_role(
        RoleArn=f"arn:aws:iam::{AOSS_ACCOUNT_ID}:role/SearchAccessRole",
        RoleSessionName="searchAccount",
        DurationSeconds=3600,  # 1 hour
    )

    return role_keys


@click.command(name="assume_role")
def _assume_search_role():
    role_keys = assume_search_role()
    jprint(role_keys["Credentials"])
