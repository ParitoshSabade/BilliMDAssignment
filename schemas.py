user_update_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string', 'pattern': '^[0-9a-fA-F]{24}$'},
        'first_name': {'type': 'string'},
        'middle_name': {'type': 'string'},
        'last_name': {'type': 'string'},
        'password': {'type': 'string', 'minLength': 8},
        'phone': {'type': 'string'},
        'updated_datetime': {'type': 'string', 'format': 'date-time'}
    },
    'required': ['user_id'],
    'additionalProperties': False
}