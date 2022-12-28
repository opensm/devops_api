deployment = {
    'apiVersion': {'type': 'string', 'allowed': ['apps/v1'], 'required': True},
    'kind': {'type':'string', 'allowed': ['Deployment'], 'required': True},
    'metadata': {'type': 'dict',
        'schema': {
            'labels': {'type': 'dict','required': False },
            'name': {'type': 'string', 'required': True },
            'namespace': {'type':'string','required': True }
        },
    },
    'spec': {'type': 'dict', 
    'schema':{
        'replicas': {'type': 'integer','required': True },
        'selector': {'type': 'dict','required': True ,'schema': {
            'matchLabels': {'type': 'dict', 'required': True}
            },
        'template': {
            'type': 'dict','required': True, 'schema': {
                'metadata': {'type': 'dict','required': True},
                'spec': {
                    'type': 'dict','required': True,'schema': {
                        'containers': {
                            'type': 'list',
                            'items': [{
                                'type': 'dict','schema': {
                                    'name': {'type': 'string','required': True},
                                    'image': {'type': 'string','required': True},
                                    'imagePullPolicy': {'type': 'string','required': True},
                                    'ports': {'type': 'list','required': False, 'items': [{
                                        'type': 'dict','required': True, 'schema': {
                                           'protocol':{'type': 'string','required': True},
                                           'containerPort': {'type': 'integer','required': True},
                                        }
                                    }]},
                                    'resources': {'type':'dict','required': 'FaLse','schema': {
                                        'limits': {
                                            'type': 'dict','required': True,'schema':{
                                                    'type': 'string','required': True,
                                                    'cpu':{'type': 'integer','required': True},
                                                    'memory':{'type': 'integer','required': True}
                                                }
                                            }
                                        }
                                    }
                                }
                            }]
                        }
                    }
                }
            }
        },
        'strategy': {'type': 'dict','required': False },
        }
        },
    }
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