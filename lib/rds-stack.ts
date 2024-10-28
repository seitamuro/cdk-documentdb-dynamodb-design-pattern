import * as cdk from "aws-cdk-lib";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import { Construct } from "constructs";

interface ConsumeProps extends cdk.StackProps {
  vpc: ec2.Vpc;
}

export class RdsStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: ConsumeProps) {
    super(scope, id, props);

    const vpc = props.vpc;

    const clusterSg = new ec2.SecurityGroup(this, "AuroraSecurityGroup", {
      vpc: vpc,
      allowAllOutbound: true,
    });
  }
}
