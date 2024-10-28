import * as cdk from "aws-cdk-lib";
import { Construct } from "constructs";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as docdb from "aws-cdk-lib/aws-docdb";

interface ConsumeProps extends cdk.StackProps {
  vpc: ec2.Vpc;
}

export class CdkMongodbStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: ConsumeProps) {
    super(scope, id, props);

    const vpc = props.vpc;

    const keyPair = new ec2.KeyPair(this, "KeyPair");
    const instanceSg = new ec2.SecurityGroup(this, "InstanceSecurityGroup", {
      vpc: vpc,
      allowAllOutbound: true,
    });
    instanceSg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22));
    const userData = ec2.UserData.forLinux();
    userData.addCommands(
      "sudo echo '[mongodb-org-8.0]' >> /etc/yum.repos.d/mongodb-org-8.0.repo",
      "sudo echo 'name=Mongo DB Repository' >> /etc/yum.repos.d/mongodb-org-8.0.repo",
      "sudo echo 'baseurl=https://repo.mongodb.org/yum/amazon/2023/mongodb-org/8.0/x86_64/' >> /etc/yum.repos.d/mongodb-org-8.0.repo",
      "sudo echo 'gpgcheck=1' >> /etc/yum.repos.d/mongodb-org-8.0.repo",
      "sudo echo 'enabled=1' >> /etc/yum.repos.d/mongodb-org-8.0.repo",
      "sudo echo 'gpgkey=https://pgp.mongodb.com/server-8.0.asc' >> /etc/yum.repos.d/mongodb-org-8.0.repo",
      "sudo dnf install -qy mongodb-mongosh-shared-openssl3"
    );
    const instance = new ec2.Instance(this, "Instance", {
      vpc,
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.T2,
        ec2.InstanceSize.SMALL
      ),
      keyPair: keyPair,
      machineImage: ec2.MachineImage.latestAmazonLinux2023(),
      associatePublicIpAddress: true,
      securityGroup: instanceSg,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PUBLIC,
      },
      userData: userData,
    });
    const privateKey = new cdk.aws_secretsmanager.Secret(
      this,
      "EC2KeyPairPrivateKey",
      {
        secretName: "/ec2/keypair/" + keyPair.keyPairId,
        description: "EC2 Key Pair Private Key",
      }
    );

    const clusterSg = new ec2.SecurityGroup(this, "MongoDBSecurityGroup", {
      vpc: vpc,
      allowAllOutbound: true,
    });
    clusterSg.addIngressRule(instanceSg, ec2.Port.tcp(27017));

    const cluster = new docdb.DatabaseCluster(this, "DocumentDB", {
      masterUser: {
        username: "myuser",
        password: cdk.SecretValue.unsafePlainText("aaaaaaaa"),
      },
      engineVersion: "5.0.0",
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.R5,
        ec2.InstanceSize.LARGE
      ),
      vpcSubnets: {
        subnetType: ec2.SubnetType.PUBLIC,
      },
      vpc,
      securityGroup: clusterSg,
      port: 27017,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    new cdk.CfnOutput(this, "MongoDBURI", {
      value: cluster.clusterReadEndpoint.hostname,
    });
    new cdk.CfnOutput(this, "GetSSHKeyCommand", {
      value:
        "aws secretsmanager get-secret-value --secret-id " +
        privateKey.secretArn +
        " --query SecretString --output text > my-key.pem && chmod 400 my-key.pem",
    });
    new cdk.CfnOutput(this, "InstanceIp", {
      value: instance.instancePublicIp,
    });
  }
}
