
from utils.exceptions import ParamErrorException

def format_request_params(request,model):
    print(request)
    params = {}
    for key, value in request.GET.items():
        if len(value) == 0:
            raise ParamErrorException(message="Missing parameter")
        elif len(value) == 1:
            params[key] = value[0]
        else:
            params["{}__in".format(key)] = value
    print(model)
    return params

__all__ = ['format_request_params']