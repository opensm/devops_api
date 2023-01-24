from __future__ import print_function
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint

configuration = kubernetes.client.Configuration()
# Configure API key authorization: BearerToken
configuration.api_key = {"authorization": "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IlMxTUFHN1ZXNWpZQ2VLU2ZwbEZQVzJ2R3NXejlpRk1CeDFScGg4eVdDTFUifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJtb25pdG9yIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6Im9wc3lzdGVtLXRva2VuLWo4bGtmIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6Im9wc3lzdGVtIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZjRkZGRlNDAtMGZhMC00NDgxLWIwOGMtZGMzNGU4YmExNzkwIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Om1vbml0b3I6b3BzeXN0ZW0ifQ.QVit8ontC6qwzvQ9MG3S2iy7407-UVUz2KZbNQNmWjvTca5T6kFo5VsiyxeFtmK1g-EOEwUZDNrE4expPqMFI7q6wiQbOikv16H6FGfZifh9yw2oOLYErOJ0HmiMok4kFumqAZJkceH0l92R4hW3623ZKUyaRCisbfphBSjX1JxiiYyjc5y1B58H59j5ImXNye59Iu7_4ABX2A2HFqQ7KKwJsLP9VsSA1FrFi2NRPR1M8OyLJ82zMnzggv652mQYFxo84i0GhI_kRyFQpZZft_VUVHkQOnciICmkDva5-fz97PAxVx4vcxl6imnCiyfOTDU0eS4lxJ3hBRcF3dq6EA"}
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['authorization'] = 'Bearer'

# Defining host is optional and default to http://localhost
configuration.host = "https://172.18.0.120:6443"
configuration.verify_ssl = False

# Enter a context with an instance of the API kubernetes.client
with kubernetes.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = kubernetes.client.CoreV1Api(api_client)
    
    try:
        api_response = api_instance.list_namespace()
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling WellKnownApi->get_service_account_issuer_open_id_configuration: %s\n" % e)