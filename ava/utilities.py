import boto3
import click


def display_aws_profile_menu(available_profiles):
    profile_choices = list(map(str, range(1, len(available_profiles) + 1)))
    profile_choice_num = 1

    click.echo("\nWhich AWS profile do you want to use?\n")

    for profile in available_profiles:
        msg = str(profile_choice_num) + " - " + profile
        click.echo("\t" + msg)
        profile_choice_num = profile_choice_num + 1

    profile_choice = click.prompt("\nProfile", type=click.Choice(
        profile_choices), show_choices=False)
    return available_profiles[int(profile_choice) - 1]


def get_boto3_session(profile, region):
    return boto3.Session(profile_name=profile, region_name=region)


def select_aws_profile():
    available_profiles = boto3.session.Session().available_profiles
    aws_profile_choice = display_aws_profile_menu(available_profiles)
    return aws_profile_choice
