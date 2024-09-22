user_update_schema = {
    'type': 'object',
    'properties': {
        '_id': {'type': 'object'},
        'first_name': {'type': 'string'},
        'middle_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'password': {'type': 'string', 'minLength': 8},
        'phone': {'type': 'string'},
        'updated_datetime': {'type': 'string', 'format': 'date-time'}
    },
    'required': ['_id'],
    'additionalProperties': False
}

user_signup_schema = {
    'type': 'object',
    'properties': {
        'first_name': {'type': 'string'},
        'middle_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'password': {'type': 'string', 'minLength': 8},
        'phone': {'type': 'string'}
    },
    'required': ['first_name', 'last_name', 'password', 'phone'],
    'additionalProperties': False
}

user_login_schema = {
    'type': 'object',
    'properties': {
        'phone': {'type': 'string'},
        'password': {'type': 'string'}
    },
    'required': ['phone', 'password'],
    'additionalProperties': False
}