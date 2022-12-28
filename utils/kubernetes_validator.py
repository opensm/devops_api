deployment = {
    'apiVersion': {'type': 'string', 'allowed': ['apps/v1'], 'required': True},
    'kind': {'type':'string', 'allowed': ['Deployment'], 'required': True},
    'metadata': {'type': 'object'},
    'spec': {'type': 'string', 'allowed': ['']},
}

service={
    'apiVersion': {'type': 'string', 'allowed': ['v1'], 'required': True},
    'kind': {'type':'string', 'allowed': ['Service'], 'required': True},
}

stateful_set={
    'apiVersion': {'type': 'string', 'allowed': ['apps/v1'], 'required': True},
    'kind': {'type':'string', 'allowed': ['StatefulSet'], 'required': True},
}

config_map={
    'apiVersion': {'type': 'string', 'allowed': ['v1'], 'required': True},
    'kind': {'type':'string', 'allowed': ['ConfigMap'], 'required': True},
}

secret = {
    'apiVersion': {'type': 'string', 'allowed': ['v1'], 'required': True},
    'kind': {'type':'string', 'allowed': ['Secret'], 'required': True},
}

ingress = {
    'apiVersion': {'type': 'string', 'allowed': ['networking.k8s.io/v1'], 'required': True},
    'kind': {'type':'string', 'allowed': ['Ingress'], 'required': True},
}

namespace={
    'apiVersion': {'type': 'string', 'allowed': ['v1'], 'required': True},
    'kind': {'type':'string', 'allowed': ['Namespace'], 'required': True},
}