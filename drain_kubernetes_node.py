from __future__ import print_function
from kubernetes import client, config
import kubernetes.client
from kubernetes.client.rest import ApiException
import sys
import pprint
import time
from pprint import pprint
import os

# Configure API key authorization: BearerToken
configuration = config.load_kube_config()
#configuration.api_key['authorization'] = 'YOUR_API_KEY'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['authorization'] = 'Bearer'
# create an instance of the API class
api_instance = kubernetes.client.CoreV1Api(kubernetes.client.ApiClient(configuration))
name = 'nodename' # str | name of the Node
body = {"spec":{"unschedulable":True}}
pretty = True # str | If 'true', then the output is pretty printed. (optional)
dry_run = 'All' # str | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed (optional)
field_manager = 'application/strategic-merge-patch+json' # str | fieldManager is a name associated with the actor or entity that is making these changes. The value must be less than or 128 characters long, and only contain printable characters, as defined by https://golang.org/pkg/unicode/#IsPrint. This field is required for apply requests (application/apply-patch) but optional for non-apply patch types (JsonPatch, MergePatch, StrategicMergePatch). (optional)
force = False # bool | Force is going to \"force\" Apply requests. It means user will re-acquire conflicting fields owned by other people. Force flag must be unset for non-apply patch requests. (optional)
# schelude node
try:
    api_response = api_instance.patch_node(name, body, pretty=pretty, field_manager=field_manager, dry_run=dry_run)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CoreV1Api->patch_node: %s\n" % e)

#evict node's pods
v1 = client.CoreV1Api(configuration)
field_selector = 'spec.nodeName='+name
ret = v1.list_pod_for_all_namespaces(watch=False, field_selector=field_selector)
for i in ret.items:
    pod_name=i.metadata.name
    node_namespaces=i.metadata.namespace
    print(pod_name)
    body = kubernetes.client.V1beta1Eviction(metadata=kubernetes.client.V1ObjectMeta(name=pod_name, namespace=node_namespaces))
    api_response = v1.create_namespaced_pod_eviction(name=pod_name, namespace=node_namespaces, body=body, pretty=pretty,dry_run=dry_run)
    pprint(api_response)
# unschelude node
body = {"spec":{"unschedulable":False}}
try:
    api_response = api_instance.patch_node(name, body, pretty=pretty, field_manager=field_manager, dry_run=dry_run)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CoreV1Api->patch_node: %s\n" % e)
