#!/usr/bin/env node
import "source-map-support/register";
import * as cdk from "aws-cdk-lib";
import { CdkMongodbStack } from "../lib/cdk-mongodb-stack";
import { VpcStack } from "../lib/vpc-stack";
import { DynamoDbStack } from "../lib/dynamodb-stack";
import { RdsStack } from "../lib/rds-stack";

const app = new cdk.App();

const vpcStack = new VpcStack(app, "vpc-stack", {});

new CdkMongodbStack(app, "mongodb-stack", {
  vpc: vpcStack.vpc,
});

new DynamoDbStack(app, "dynamodb-stack", {
  vpc: vpcStack.vpc,
});

new RdsStack(app, "rds-stack", {
  vpc: vpcStack.vpc,
});
