import click
import boto3
import os
import utilities as ph
from rich import box
from rich.console import Console
from rich.table import Table
from pathlib import Path

console = Console()


@click.group()
@click.option('--profile')
@click.option('--region', default='eu-west-1')
@click.pass_context
def credentials(ctx, profile, region):
    if not profile:
        profile = ph.select_aws_profile()

    ctx.obj['SESSION'] = ph.get_boto3_session(profile=profile, region=region)
    ctx.obj['PROFILE'] = profile
    ctx.obj['REGION'] = region


@credentials.command(name='ec2')
@click.option('--update', required=False, default=None, help="Provide either 'instance_id' or 'all'")
@click.pass_obj
def return_list_of_instances(ctx):
    """
    List EC2 instances and SSM status
    """

    ec2_client = ctx['SESSION'].client('ec2')
    ssm_client = ctx['SESSION'].client('ssm')
    table = Table(show_header=True, pad_edge=False, box=box.MINIMAL)
    titles = ['Instance ID', 'VpcID', 'IP Address', 'Operating System', 'Ping Status',
              'Instance State', 'Instance Type', 'Availability Zone', 'Is Agent Up-To-Date', 'Hostname']
    ec2_instances = ec2_client.describe_instances()
    ssm_instances = ph.reduce(ph.collect, ssm_client.describe_instance_information()[
                              'InstanceInformationList'], {})
    data = []
    for instance in ec2_instances['Reservations']:
        output = []
        instance = instance['Instances'][0]
        instance_id = instance['InstanceId']
        output.append(instance['InstanceId'])
        output.append(instance.get('VpcId', ""))
        output.append(ssm_instances.get(instance_id, {}).get('IPAddress', ""))
        output.append(ssm_instances.get(
            instance_id, {}).get('PlatformName', ""))
        output.append(ssm_instances.get(instance_id, {}).get('PingStatus'))
        output.append(str(instance['State']['Name']).capitalize())
        output.append(instance['InstanceType'])
        output.append(instance['Placement']['AvailabilityZone'])
        output.append(str(ssm_instances.get(
            instance_id, {}).get('IsLatestVersion', "")))
        if 'Tags' in instance:
            for tag in instance['Tags']:
                if tag['Key'] == 'Name':
                    output.append(tag['Value'])
        data.append(output)

    for column in list(zip(titles)):
        table.add_column(*column)
    for row in list(data):
        table.add_row(*row)
    console.print(table)
