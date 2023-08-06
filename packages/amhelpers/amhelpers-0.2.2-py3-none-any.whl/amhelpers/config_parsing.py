import copy
from .amhelpers import get_class_from_str
from .amhelpers import create_object_from_dict

def _check_value(value):
    if isinstance(value, (int, float)):
        return value
    elif isinstance(value, bool):
        return value
    elif isinstance(value, str):
        return value
    elif isinstance(value, list):
        return [_check_value(v) for v in value]
    elif isinstance(value, dict):
        if 'type' in value:
            is_called = value.pop('is_called')
            if is_called:
                return create_object_from_dict(value)
            else:
                type_str = value['type']
                return get_class_from_str(type_str)
        else:
            return {k: _check_value(v) for k, v in value.items()}
    elif value is None:
        return value
    else:
        raise ValueError('The value of type {} is unknown.'.format(type(value)))

def _get_object_and_parameters(name, default_params, specified_params={}):
    default_params.pop('is_called', None)
    specified_params.pop('is_called', None)

    prefix = name + '__'

    if 'type' in specified_params:
        out = {name: get_class_from_str(specified_params.pop('type'))}
        out.update(
            {prefix+k: _check_value(v) for k, v in specified_params.items()}
        )
    else:
        out = {name: get_class_from_str(default_params.pop('type'))}
        out.update(
            {prefix+k: _check_value(specified_params[k]) if k in specified_params else _check_value(default_params[k]) for k in default_params.keys()}
        )

    return out

def get_net_params(default, specified):
    '''Get parameters for a Skorch neural net.

    Parameters
    ----------
    default : dict
        Default parameter values on the format "parameter name: value".
    specified : dict
        Specified parameter values on the format "parameter name: value". Will replace the default values.

    Returns
    -------
    params : dict
        All model parameters.
    '''
    default = copy.deepcopy(default)
    specified = copy.deepcopy(default)
    params = {}
    for param, value in default.items():
        if param in (
            'module',
            'criterion',
            'optimizer',
            'iterator_train',
            'iterator_valid',
            'dataset'
        ):
            if param in specified:
                params.update(
                    _get_object_and_parameters(param, value, specified[param])
                )
            else:
                params.update(
                    _get_object_and_parameters(param, value)
                )
        else:
            params[param] = _check_value(specified[param]) if param in specified else _check_value(value)
    return params
