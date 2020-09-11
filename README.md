# ECS-STOP-START with boto3
Schedule lambda function to shut down your microservices during off-peak hours for your development environments for saving development cost

# Environmental setup

1) AWS Lambda function with python runtime version (https://docs.aws.amazon.com/lambda/latest/dg/lambda-python.html)
2) Cloudwatch event rule to schedule lambda function (https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/RunLambdaSchedule.html)
3) ECS cluster having necessary tags available to filter clusters we need to stop to save costs (here we have used "Auto-shutdown=True" and ApplicationName tags to filter clusters)
4) Lambda function having necessary environmental variables attached to it (here we have used ApplicationName) to filter out required ECS clusters to shutdown
(https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html)
