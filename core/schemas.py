signup_schema = {
    "title": "The schema for signup",
    "type": "object",
    "properties": {
        "firstName": {"type": "string"},
        "lastName": {"type": "string"},
        "email": {"type": "string"},
        "password": {"type": "string"},
        "phones": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "number": {"type": "string"},
                    "area_code": {"type": "string"},
                    "country_code": {"type": "string"}
                },
                "required": ["number", "area_code", "country_code"],
                "additionalProperties": False,
            },
            "minItems": 1
        }
    }
    "required": ["firstName", "lastName", "email", "password", "phones"],
    "additionalProperties": False,
}
     