from azure.servicemanagement import ServiceManagementService

sms = ServiceManagementService(
    'cd42b929-8458-4acd-b599-398cd51f4c6c', './mycert.pem')
prop = sms. get_hosted_service_properties('persistentvm51', embed_detail=True)
print prop
