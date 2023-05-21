import boto3
import json
import os
 
# grab environment variables 
ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
 
# obtain sagemaker runtime
runtime = boto3.Session().client(service_name='sagemaker-runtime',region_name='us-east-1')

#obtain s3 client
s3 = boto3.client('s3')
 
def lambda_handler(event, context):
  
    #set the image categories
    image_categories = ['daisy', 'rose', 'tulip', 'dandelion', 'sunflower']
   
    #bucket name where image data is stored
    bucket = 'sagemaker-studio-ndc' 
    
    #key is the image file name - NOTE: select an image name from the test .lst file
    key = 'images/daisy/3546455114_cd2dea5e02.jpg'
    
    #retrieve the image of the flower from s3
    image_obj = s3.get_object(Bucket=bucket, Key=key)
    
    #retrieve the image contents
    image_contents = image_obj['Body'].read()
   
    #call model for predicting the flower, passing image
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                      ContentType='application/x-image',
                                      Body=bytearray(image_contents))
   
    
    #read the prediction result and parse the json
    result = response['Body'].read()
    result = json.loads(result)
    
    # Returns each class label with a probability score
    print(result)
    
    # the index of the flower with the highest probability score
    index = result.index(max(result))
    
    message = "The flower is a " + image_categories[index]
    
    return message