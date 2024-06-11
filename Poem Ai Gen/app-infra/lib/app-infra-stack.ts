import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apiGateway from 'aws-cdk-lib/aws-apigateway';
import * as dotenv from "dotenv";

dotenv.config()

export class AppInfraStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);
    
    const layer = new lambda.LayerVersion(this, "BaseLayer", {
      code :lambda.Code.fromAsset("lambda_base_layer/layer.zip"),
      compatibleRuntimes: [lambda.Runtime.PYTHON_3_9]
    });

    const apiLambda = new lambda.Function(this, "ApiFunction", {
      runtime: lambda.Runtime.PYTHON_3_9,
      code: lambda.Code.fromAsset("../app/"),
      handler: "poem_ai_api.handler",
      layers: [layer],
      environment: {
        OPENAI_API_KEY = process.env.OPENAI_API_KEY ?? "",
      }
    });

    const poemApi = new apiGateway.RestApi(this, "RestApi", {
      restApiName: "Poem Ai Generator API"
    });

    poemApi.root.addProxy({
      defaultIntegration: new apiGateway.LambdaIntegration(apiLambda),
    });
  }
}
