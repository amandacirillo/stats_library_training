import { Construct } from "constructs";
import { RemovalPolicy, Stack, StackProps as CdkStackProps, Duration } from "aws-cdk-lib";
import { aws_certificatemanager as acm } from "aws-cdk-lib";
import { aws_cloudfront as cloudfront } from "aws-cdk-lib";
import { aws_cloudfront_origins as origins } from "aws-cdk-lib";
import { aws_s3 as s3 } from "aws-cdk-lib";
import { aws_route53 as route53 } from "aws-cdk-lib";
import { aws_route53_targets as route53_targets } from "aws-cdk-lib";
import { aws_s3_deployment as s3deploy } from "aws-cdk-lib";

import * as CONST from "./const";

export interface StackProps extends CdkStackProps {
  readonly htmlPath: string;
  readonly subdomain: string;
}

/**
 * Deploys a static Sphinx-generated HTML site (built by CI in the
 * `generate_docs` stage) to S3, fronted by CloudFront with a
 * Route 53-validated ACM certificate for HTTPS on a friendly subdomain.
 *
 * This is the same three-piece pattern used to publish a package's docs
 * without hand-managing a webserver: build the static site as a CI
 * artifact, `cdk deploy` it, done. Every value under `lib/const.ts` here is
 * fictional -- swap in your own hosted zone before deploying for real.
 */
export class DocsSiteStack extends Stack {
  constructor(scope: Construct, id: string, props: StackProps) {
    super(scope, id, props);

    const hostName = `${props.subdomain}.${CONST.HOSTED_ZONE_NAME}`;

    const hostedZone = route53.HostedZone.fromHostedZoneAttributes(this, "hostedzone", {
      hostedZoneId: CONST.HOSTED_ZONE_ID,
      zoneName: CONST.HOSTED_ZONE_NAME,
    });

    const certificate = new acm.Certificate(this, "certificate", {
      domainName: hostName,
      validation: acm.CertificateValidation.fromDns(hostedZone),
    });

    const bucket = new s3.Bucket(this, "docs-bucket", {
      encryption: s3.BucketEncryption.S3_MANAGED,
      removalPolicy: RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
      enforceSSL: true,
      blockPublicAccess: s3.BlockPublicAccess.BLOCK_ALL,
      versioned: true,
      lifecycleRules: [
        {
          id: "mpu-cleanup-rule",
          abortIncompleteMultipartUploadAfter: Duration.days(7),
          enabled: true,
        },
      ],
    });

    const distribution = new cloudfront.Distribution(this, "distribution", {
      defaultRootObject: "index.html",
      defaultBehavior: {
        origin: origins.S3BucketOrigin.withOriginAccessControl(bucket),
        viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.HTTPS_ONLY,
      },
      domainNames: [hostName],
      certificate,
      priceClass: cloudfront.PriceClass.PRICE_CLASS_100,
    });

    new s3deploy.BucketDeployment(this, "deploy-docs", {
      sources: [s3deploy.Source.asset(props.htmlPath)],
      destinationBucket: bucket,
      distribution,
    });

    new route53.ARecord(this, "alias-record", {
      target: route53.RecordTarget.fromAlias(new route53_targets.CloudFrontTarget(distribution)),
      zone: hostedZone,
      recordName: props.subdomain,
    });
  }
}
