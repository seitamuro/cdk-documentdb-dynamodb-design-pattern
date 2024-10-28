import * as cdk from "aws-cdk-lib";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as dynamodb from "aws-cdk-lib/aws-dynamodb";
import { Construct } from "constructs";

interface ConsumeProps extends cdk.StackProps {
  vpc: ec2.Vpc;
}

export class DynamoDbStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: ConsumeProps) {
    super(scope, id, props);

    const vpc = props.vpc;

    const usersTable = new dynamodb.Table(this, "users", {
      partitionKey: { name: "id", type: dynamodb.AttributeType.STRING },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const contentsTable = new dynamodb.Table(this, "contents", {
      partitionKey: { name: "id", type: dynamodb.AttributeType.STRING },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const contentTagsTable = new dynamodb.Table(this, "contentTags", {
      partitionKey: { name: "id", type: dynamodb.AttributeType.STRING },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const tagsTable = new dynamodb.Table(this, "tags", {
      partitionKey: { name: "id", type: dynamodb.AttributeType.STRING },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    const sampleTable = new dynamodb.Table(this, "sample", {
      partitionKey: { name: "ID", type: dynamodb.AttributeType.STRING },
      sortKey: { name: "DataType", type: dynamodb.AttributeType.STRING },
    });
  }
}
