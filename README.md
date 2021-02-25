# Ava

Ava is a CLI application to return various items from the AWS Console without the need of logging in.  As long as you have configured your aws-cli to an account; you can run this tool. 

## Usage:

```
/ ❯ ava
Usage: ava [OPTIONS] COMMAND [ARGS]...

  Welcome to Ava!

Options:
  --help  Show this message and exit.

Commands:
  aws  AWS Utils
```

```
/ ❯ ava aws
Usage: ava aws [OPTIONS] COMMAND [ARGS]...

  AWS Utils

Options:
  --help  Show this message and exit.

Commands:
  ec2  Get EC2 things
  vpc  Return a list of VPCs

```

**Example :**

```
/ ❯ ava aws ec2 --profile aws-profile
                     ╷                       ╷               ╷                  ╷             ╷                ╷               ╷                   ╷                     ╷
 Instance ID         │ VpcID                 │ IP Address    │ Operating System │ Ping Status │ Instance State │ Instance Type │ Availability Zone │ Is Agent Up-To-Date │ Hostname
╶────────────────────┼───────────────────────┼───────────────┼──────────────────┼─────────────┼────────────────┼───────────────┼───────────────────┼─────────────────────┼───────────────────────────────────────────────────────────────────╴
 i-0f42c9088419a2c90 │ vpc-02cb1743          │ 10.79.102.132 │ Amazon Linux     │ Online      │ Running        │ t3.medium     │ eu-west-1b        │ False               │ Hostname/NatInstance-V20210217104440
 i-0f42c9088419a2c90 │ vpc-02cb1743          │ 10.79.102.225 │ Amazon Linux     │ Online      │ Running        │ t3a.large     │ eu-west-1b        │ False               │ Hostname/NatInstance-V20210217104440
 i-0f42c9088419a2c90 │ vpc-02cb1743          │ 10.79.102.223 │ Amazon Linux     │ Online      │ Running        │ t3a.large     │ eu-west-1b        │ False               │ Hostname/NatInstance-V20210217104440
 i-0f42c9088419a2c90 │ vpc-02cb1743          │ 10.79.102.157 │ Amazon Linux     │ Online      │ Running        │ t3a.large     │ eu-west-1b        │ False               │ Hostname/NatInstance-V20210217104440
```
