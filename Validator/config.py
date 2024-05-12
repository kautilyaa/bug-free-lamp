import cerberus
schema = {
    "patterns" :{"type":"list"},
    "error_rules" : {"type":"dict"},
    "spl_chars_allowed":{"type":"string"}
}
config_validator = cerberus.Validator(schema, require_all =True)