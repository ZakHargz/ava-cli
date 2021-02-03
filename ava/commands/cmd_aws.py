import click, boto3, os
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
    ec2_client = ctx.obj.session.ec2(profile=profile, region=region).client('ec2')
    ssm_client = ctx.obj.session.ec2(profile=profile, region=region).client('ssm')
    table = Table(show_header=True, pad_edge=False, box=box.MINIMAL)
    titles = ['Instance ID', 'VpcID', 'IP Address', 'Operating System', 'Ping Status', 'Instance State', 'Instance Type', 'Availability Zone', 'Is Agent Up-To-Date', 'Hostname']
    ec2_instances = ec2_client.describe_instances()
    ssm_instances = ctx.obj.session.reduce(ctx.obj.session.collect, ssm_client.describe_instance_information()['InstanceInformationList'], {})
    data = []
    for instance in ec2_instances['Reservations']:
        output = []
        instance = instance['Instances'][0]
        instance_id = instance['InstanceId']
        output.append(instance['InstanceId'])
        output.append(instance.get('VpcId', ""))
        output.append(ssm_instances.get(instance_id, {}).get('IPAddress', ""))
        output.append(ssm_instances.get(instance_id, {}).get('PlatformName', ""))
        output.append(ssm_instances.get(instance_id, {}).get('PingStatus'))
        output.append(str(instance['State']['Name']).capitalize())
        output.append(instance['InstanceType'])
        output.append(instance['Placement']['AvailabilityZone'])
        output.append(str(ssm_instances.get(instance_id, {}).get('IsLatestVersion', "")))
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

@cli.command()
@click.option('--profile')
@click.option('--region', default='eu-west-1')
@click.pass_context
def vpc(ctx, profile, region):
    """ Return a list of VPCs """
    vpc_client = ctx.obj.session.vpc(profile=profile, region=region).client('ec2')
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
