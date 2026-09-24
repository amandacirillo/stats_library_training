# infra/cdk

A TypeScript CDK stack (`lib/stack.ts`) that deploys a static HTML site --
in the real pipeline, the Sphinx docs built in the `build-docs` CI job -- to
S3, fronted by CloudFront with an ACM certificate validated against a
Route 53 hosted zone.

This is deliberately **not** wired into this training repo's CI. Deploying
it for real needs an actual AWS account and hosted zone. To try it against
your own AWS account:

```bash
cd infra/cdk
npm install
mkdir -p assets/docs/html
cp -a ../../docs/build/html/* assets/docs/html/   # build docs first: see docs/ README
npx cdk synth      # verify the template
npx cdk deploy     # requires bootstrapped AWS credentials + your own hosted zone in lib/const.ts
```

Update `lib/const.ts` with your own `HOSTED_ZONE_ID`/`HOSTED_ZONE_NAME`
before deploying -- the values checked in are fictional placeholders.
