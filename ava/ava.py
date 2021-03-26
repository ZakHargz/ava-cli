
import click
import boto3
import os
from ava.utilities import display_aws_profile_menu, get_boto3_session, select_aws_profile
from rich import box
from rich.console import Console
from rich.table import Table
from pathlib import Path

console = Console()
BOTO3_SESSION = None


@click.group()
@click.option('--profile')
@click.option('--region', default='eu-west-1')
@click.pass_context
def cli(ctx, profile, region):
    """
    Welcome to Ava!
    """
    if not (profile):
        profile = select_aws_profile()

    global BOTO3_SESSION
    BOTO3_SESSION = get_boto3_session(profile=profile, region=region)


@cli.command(name='ec2')
@click.pass_obj
def return_list_of_instances(ctx):
    """
    List EC2 instances and SSM status
    """
    ec2_client = BOTO3_SESSION.client('ec2')
    ssm_client = BOTO3_SESSION.client('ssm')
    ec2_instances = ec2_client.describe_instances()
    table = Table(show_header=True, pad_edge=False, box=box.MINIMAL)
    titles = ['Instance ID', 'VpcID', 'IP Address', 'Operating System', 'Ping Status', 'SSM Agent',
              'Instance State', 'Instance Type', 'Availability Zone', 'Hostname']
    data = []
    output = []
    next_token = ''

    for ec2id in ec2_instances['Reservations']:
        for iid in ec2id['Instances']:
            output = []
            output.append(iid['InstanceId'])
            output.append(iid.get('VpcId'))
            if next_token is not None:
                ssm = ssm_client.describe_instance_information(
                    Filters=[{'Key': 'InstanceIds', 'Values': ['i-02975bc7a520b2434']}], MaxResults=50, NextToken=next_token)
                for ssminfo in ssm['InstanceInformationList']:
                    output.append(ssminfo['IPAddress'])
                    output.append(ssminfo['PlatformName'])
                    output.append(ssminfo['PingStatus'])
                    output.append(str(ssminfo['IsLatestVersion']))
            output.append(str(iid['State']['Name']).capitalize())
            output.append(iid['InstanceType'])
            output.append(iid['Placement']['AvailabilityZone'])
            if 'Tags' in iid:
                for tag in iid['Tags']:
                    if tag['Key'] == 'Name':
                        output.append(tag['Value'])
            data.append(output)

    for column in list(zip(titles)):
        table.add_column(*column)
    for row in list(data):
        table.add_row(*row)
    console.print(table)
    console.print(
        '* ssm-agent column refers to whether the agent is up-to-date')
    console.print('* number of running instances: ',
                  len(ec2_client.describe_instances()['Reservations']))
