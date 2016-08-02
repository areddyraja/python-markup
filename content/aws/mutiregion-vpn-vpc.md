title: OpenVPN: Connecting VPCs between regions
date: 2016-05-02
description: AWS Open VPN
tags: AWS Open VPN

### VPC's in single region
Multiple AWS instances living within a single VPC can communicate each other using private IP addresses. You can also directly connect instances in two separate VPC’s within a single region using VPC Peering.

Assuming that you’ve set up your subnets so they don’t overlap, a peering connection enables direct traffic routing between VPCs using private IP address ranges. 

But what if you want to connect instances hosted in separate AWS regions? OpenVPN can make it happen.

If your organization cannot afford VPN's like a commercial product from Cisco or an on-premise applicance, one can use the open source OpenVPN package to secure communications between your distributed resources at no cost.

OpenVPN’s SSL/TLS based user-space VPN supports Linux, Solaris, OpenBSD, FreeBSD, NetBSD, Mac OS X, and Windows 2000/XP.

#### Scenarios to use OpenVPn

* You have a configured disaster recovery setup in another region and want to connect using private communication.
* You would like to regularly transfer data over a secure tunnel.
* You have deployed high-availability architecture across VPCs but need to maintain direct, private communication between them.
* You are a big fan of open source and don’t want to pay for commercially available VPN services.

##### Configure VPCs

VPCs configured with both public and private subnets in at least two different AWS regions. In this guide, we will assume that there is one VPC in AWS’s US East Region which we will call VPC-1, and a second VPC in EU West that we’ll call VPC-2.

From the Launch Instance menu of the EC2 dasboard, search for “Open VPN Access Server” from AWS Marketplace and launch the instance in the public subnet of VPC-1.

Make sure the security group associated with this instance has ports 22 (SSH), 443 (SSL), 993 (Admin Web UI), and 1194 (OpenVPN UDP port) open. You should also allocate an Elastic IP to this instance.


http://cloudacademy.com/blog/openvpn-aws-vpc/



