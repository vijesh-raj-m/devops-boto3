import json
import boto3
import os
client = boto3.client('ecs')
ecs = boto3.client('application-autoscaling')
ApplicationName = os.environ['ApplicationName']
def lambda_handler(event, context):
   describeCluster = client.list_clusters()
   clusterarn = describeCluster['clusterArns']
   for arn in clusterarn:
        clusterTagsList = client.list_tags_for_resource(resourceArn=arn)
        shutdownTagValue=''
        applicationTagValue=''
        for tags in clusterTagsList['tags']:
            if tags["key"] == 'shutdown':
                shutdownTagValue = tags["value"]
            elif tags["key"] == 'ApplicationName':
                applicationTagValue = tags["value"]
        if shutdownTagValue == 'True' and applicationTagValue == ApplicationName:
            print ('cluster going  to modify is \t' , arn)
            serviceresponse = client.list_services(cluster=arn)
            nextToken=serviceresponse.get('nextToken',None)
            serviceNames=serviceresponse["serviceArns"]
            while (nextToken is not None):
                serviceresponse = client.list_services(cluster=arn,
                nextToken=nextToken)
                nextToken = serviceresponse.get('nextToken', None)
                serviceNames = serviceNames + serviceresponse["serviceArns"]
            for serviceName in serviceNames:
                update_service(serviceName,arn=arn)

def update_service(serviceName,arn):
    clustername = arn.split("/")[1]
    occurence = serviceName.count('/')
    serviceNamemodified=''
    if int(occurence) == 2:
        serviceNamemodified = serviceName.split("/")[2]
    else:
        serviceNamemodified = serviceName.split("/")[1]
    describe_response_autoscaling = ecs.describe_scaling_policies(ServiceNamespace='ecs',ResourceId='service/{0}/{1}'.format(clustername,serviceNamemodified))
    response_autoscaling = describe_response_autoscaling.get('ScalingPolicies')
    response_autoscaling_dictionary = not bool(response_autoscaling)
    if str(response_autoscaling_dictionary) == 'False':
        update_response = client.update_service(
        cluster=arn,
        service=serviceName,
        desiredCount=0
        )
        deregister_response_autoscaling_new = ecs.register_scalable_target(
        MaxCapacity=0,
        MinCapacity=0,
        ResourceId='service/{0}/{1}'.format(clustername,serviceNamemodified),
        ScalableDimension='ecs:service:DesiredCount',
        ServiceNamespace='ecs',
        )
        print('Stopped running tasks for service \t' +serviceNamemodified)
    else:
        update_response = client.update_service(
        cluster=arn,
        service=serviceName,
        desiredCount=0
        )
        print('Stopped running tasks for service \t' +serviceNamemodified)
