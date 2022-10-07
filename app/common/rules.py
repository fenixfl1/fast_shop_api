
# rules for validate json with cerberus.Validator

rules = dict(
    user_schema={
        "EMAIL": {
            "type": "string",
            "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
            "required": True
        },
        "FIRST_NAME": {
            "type": "string",
            "regex": "^[a-zA-Z]+$",
            "required": True
        },
        "LAST_NAME": {
            "type": "string",
            "regex": "^[a-zA-Z]+$",
            "required": True
        },
        "PASSWORD": {
            "type": "string",
            "required": True
        },
        "STATE": {
            "type": "string",
            "allowed": ["A", "I", "U"],
            "required": True
        },
        "USERNAME": {
            "type": "string",
            "regex": "^[a-zA-Z0-9_]+$",
            "required": True
        }
    },
    login_schema={
        "USERNAME": {
            "type": "string",
            "regex": "^[a-zA-Z0-9_]+$",
            "required": True
        },
        "PASSWORD": {
            "type": "string",
            "required": True
        },
        "REMEMBER_ME": {
            "type": "boolean",
            "required": False,
        }
    }
)
