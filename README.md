# AWS Python Pulumi Program - EC2 with Nginx

## Overview

This Pulumi program demonstrates how to set up a secure infrastructure on AWS to deploy an EC2 instance with an Nginx web server. The infrastructure includes a Virtual Private Cloud (VPC), public and private subnets, an Internet Gateway, a Network Address Translation (NAT) Gateway, and associated route tables. Additionally, security groups are configured to allow traffic on ports 22 (SSH) and 80 (HTTP).

## Prerequisites

Before running this Pulumi program, make sure you have the following:

* Pulumi CLI

* AWS CLI

* AWS credentials configured with the necessary permissions


## Getting Started

Clone the repository:

```bash
$ git clone <repository-url>
$ cd <repository-directory>
```

Install dependencies:

```bash
$ pulumi plugin install
$ pulumi up
```

Follow the prompts to confirm the resources to be created.

## Resources Created
The Pulumi program creates the following AWS resources:

* **VPC:** A Virtual Private Cloud to isolate your network.

* **Public and Private Subnets:** For hosting public-facing and internal resources.

* **Internet Gateway:** To enable communication with the internet.

* **NAT Gateway:** For outbound internet access from private subnets.

* **Security Groups:** Allowing inbound traffic on ports 22 (SSH) and 80 (HTTP).

* **EC2 Instance:** Running Nginx, placed in the public subnet.

## Outputs

The Pulumi program exports the following information:

* **public_ip:** Public IP address of the EC2 instance.

* **public_dns:** Public DNS name of the EC2 instance.

* **vpc_id:** ID of the created VPC.

* **public_subnet_id:** ID of the public subnet.

* **private_subnet_id:** ID of the private subnet.

* **internet_gateway_id:** ID of the Internet Gateway.

* **instance_id:** ID of the EC2 instance.


## Clean Up

To remove the resources created by the Pulumi program, run:

```bash
$ pulumi destroy
```

## Note

* Ensure that you have the necessary AWS credentials and permissions.

* Review and customize the program to meet specific requirements.

* This program is intended for educational purposes and may require adjustments for production use.

* For more details on Pulumi, refer to the official documentation.



#### Thank you :) 
<p>  <br /><br />
</p>