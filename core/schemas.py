signup_schema = {
    "title": "The schema for signup",
    "type": "object",
    "properties": {
        "firstName": {"type": "string", "minLength": 1},
        "lastName": {"type": "string", "minLength": 1},
        "email": {
            "type": "string",
            "pattern": "^[a-z0-9._]+[@]{1}[a-z0-9_]+[.]{1}[a-z0-9_]+$"
        },
        "password": {"type": "string", "minLength": 1},
        "phones": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "number": {
                        "type": "string",
                       "pattern": "^[0-9]+$"
                    },
                    "area_code": {
                        "type": "string",
                        "pattern": "^[0-9]+$"
                    },
                    "country_code": {
                        "type": "string",
                        "pattern": "\\+[0-9]{2}"
                    }
                },
                "required": ["number", "area_code", "country_code"],
                "additionalProperties": False,
            },
            "minItems": 1
        }
    },
    "required": ["firstName", "lastName", "email", "password", "phones"],
    "additionalProperties": False,
}

signin_schema = {
    "title": "The schema for signin",
    "type": "object",
    "properties": {
        "email": {
            "type": "string",
            "pattern": "^[a-z0-9._]+[@]{1}[a-z0-9_]+[.]{1}[a-z0-9_]+$"
        },
        "password": {"type": "string", "minLength": 1},
    },
    "required": ["email", "password"],
    "additionalProperties": False,
}
  
     