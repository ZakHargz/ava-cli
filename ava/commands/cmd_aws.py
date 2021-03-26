import click
import boto3
import os
from rich import box
from rich.console import Console
from rich.table import Table
from pathlib import Path
from ava.service import svc_aws

console = Console()


class Context:
    def __init__(self):
        self.session = svc_aws.AwsUtility()


@click.group()
@click.pass_context
def cli(ctx):
    """ AWS Utils """
    ctx.obj = Context()


@cli.command()
@click.option('--profile')
@click.option('--region', default='eu-west-1')
@click.pass_context
def ec2(ctx, profile, region):
    """Get EC2 things"""
    ec2_client = ctx.obj.session.ec2(
        profile=profile, region=region).client('ec2')
    ssm_client = ctx.obj.session.ec2(
        profile=profile, region=region).client('ssm')
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


@cli.command()
@click.option('--profile')
@click.option('--region', default='eu-west-1')
@click.pass_context
def vpc(ctx, profile, region):
    """ Return a list of VPCs """
    vpc_client = ctx.obj.session.vpc(
        profile=profile, region=region).client('ec2')
    list_of_vpcs = vpc_client.describe_vpcs()
    table = Table(show_header=True, pad_edge=False, box=box.MINIMAL)
    titles = ['VpcId', 'CidrBlock', 'State', 'Vpc Name']
    data = []
    for vpc in list_of_vpcs['Vpcs']:
        output = []
        output.append(vpc['VpcId'])
        output.append(vpc['CidrBlock'])
        output.append(vpc['State'])
        if 'Tags' in vpc:
            for tag in vpc['Tags']:
                if tag['Key'] == 'Name':
                    output.append(tag['Value'])
        data.append(output)

    for column in list(zip(titles)):
        table.add_column(*column)
    for row in list(data):
        table.add_row(*row)
    console.print(table)
