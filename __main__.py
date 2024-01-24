"""An AWS Python Pulumi program"""

import pulumi
from pulumi_aws import ec2
import pulumi_aws as aws

# SETTING UP AN EC2 WITH NGINX WEB SERVER INSTALLED ON AWS

size = 't2.micro'  # t2.micro is available in the AWS free tier

# Fetch the ID of the most recent Amazon Linux AMI
ami = ec2.get_ami(most_recent=True,
                owners=['137112412989'],  # Owner ID for official AWS Amazon Linux AMI
                filters=[{'name': 'name', 'values': ['amzn-ami-hvm-*-x86_64-ebs']}])


# Create a new VPC
vpc = aws.ec2.Vpc("my_vpc",
    cidr_block="10.0.0.0/16",
    enable_dns_hostnames=True,
    enable_dns_support=True,
    instance_tenancy="default",
    tags={
        "Name": "my_vpc",
    })

# Create an Internet Gateway for the VPC
internet_gateway = aws.ec2.InternetGateway("vpc-igw",
    vpc_id=vpc.id)

# Create a public subnet
public_subnet = aws.ec2.Subnet("public-subnet", 
    vpc_id=vpc.id,
    cidr_block="10.0.1.0/24",
    map_public_ip_on_launch=True, # Ensure instances receive a public IP
    availability_zone="eu-west-2a",
    tags={
        "Name": "public_subnet",
    }
    )


# Create a route table for the public subnet that routes through the Internet Gateway
public_route_table = aws.ec2.RouteTable("public-route-table",
    vpc_id=vpc.id,
    routes=[aws.ec2.RouteTableRouteArgs(
        cidr_block="0.0.0.0/0",
        gateway_id=internet_gateway.id,
    )])

# Associate the public route table with the public subnet
public_route_table_association = aws.ec2.RouteTableAssociation("public-route-table-association",
    route_table_id=public_route_table.id,
    subnet_id=public_subnet.id)

# Allocate an Elastic IP for the NAT gateway
eip = aws.ec2.Eip("nat-eip")

# Create a NAT gateway and associate it with the public subnet and EIP
nat_gateway = aws.ec2.NatGateway(
    "nat-gateway",
    subnet_id=public_subnet.id,  # This should be a public subnet
    allocation_id=eip.id
)

# Create a private subnet
private_subnet = aws.ec2.Subnet("private-subnet",
    vpc_id=vpc.id,
    cidr_block="10.0.2.0/24",
    availability_zone="eu-west-2b",
    tags={
        "Name": "private_subnet",
    }
    )

# Create a route table for the private subnet to route traffic to the NAT gateway
private_route_table = aws.ec2.RouteTable(
    "private-route-table",
    vpc_id=vpc.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block="0.0.0.0/0",
            nat_gateway_id=nat_gateway.id
        )
    ]
)

# Associate the private route table with the private subnet
private_route_table_association = aws.ec2.RouteTableAssociation(
    "private-route-table-association",
    route_table_id=private_route_table.id,
    subnet_id=private_subnet.id
)




# Create a new security group for allowing SSH and HTTP access
group = ec2.SecurityGroup('nginx-secgrp',
                        vpc_id=vpc.id,
                        ingress=[
                            {'protocol': 'tcp', 'from_port': 22, 'to_port': 22, 'cidr_blocks': ['0.0.0.0/0']},
                            {'protocol': 'tcp', 'from_port': 80, 'to_port': 80, 'cidr_blocks': ['0.0.0.0/0']}
                        ],
                        egress=[
                            {'protocol': '-1', 'from_port': 0, 'to_port': 0, 'cidr_blocks': ['0.0.0.0/0']}
                        ],
                        tags={
                            "Name": "nginx_secgrp",
                        })


# User data script to run a simple web server
user_data = """#!/bin/bash
echo "Hello, World!" > index.html
nohup python -m SimpleHTTPServer 80 &
"""

# Create a new EC2 instance
server = ec2.Instance('web-server',
                    instance_type=size,
                    vpc_security_group_ids=[group.id],
                    ami=ami.id,
                    subnet_id=public_subnet.id,
                    user_data=user_data,
                    tags={
                    "Name": "nginx",
                    })  # Start a simple web server

# Export the public IP and DNS name of the instance and other outputs
pulumi.export('public_ip', server.public_ip)
pulumi.export('public_dns', server.public_dns)
pulumi.export("vpc_id", vpc.id)
pulumi.export("public_subnet_id", public_subnet.id)
pulumi.export("private_subnet_id", private_subnet.id)
pulumi.export("internet_gateway_id", internet_gateway.id)
pulumi.export("instance_id", server.id)
