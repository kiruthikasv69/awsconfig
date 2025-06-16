AWS config - Tracks and stores configuration changes of AWS resources (like EC2, S3, IAM, etc.)
"This Lambda checks if EC2 detailed monitoring is enabled. It’s triggered by AWS Config, evaluates the EC2 instance, and reports COMPLIANT/NON_COMPLIANT status. It helps ensure that all EC2s meet monitoring standards."


AWS Config monitors EC2 instances.

When an EC2 instance is created or changed:

AWS Config automatically triggers this Lambda.

It passes the EC2 instance details in event['invokingEvent'].

The Lambda checks whether "detailed monitoring" is enabled for that EC2 instance.

It reports back to AWS Config using put_evaluations().
