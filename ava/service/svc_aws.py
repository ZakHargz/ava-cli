import boto3


class AwsUtility:
    def __init__(self, profile=None, region=None):
        self.session = boto3.Session(profile_name=profile, region_name=region)

    def ec2(self, profile, region):
        return boto3.Session(profile_name=profile, region_name=region)

    def vpc(self, profile, region):
        return boto3.Session(profile_name=profile, region_name=region)

    def reduce(self, function, iterable, initializer=None):
        it = iter(iterable)
        if initializer is None:
            value = next(it)
        else:
            value = initializer
        for element in it:
            value = function(value, element)
        return value

    def collect(self, c, i):
        c[i['InstanceId']] = i
        return c

