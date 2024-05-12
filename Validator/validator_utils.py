import re

def is_pattern_matching(value,patterns):
    for pattern in patterns:
        if bool(re.search(pattern, value)):
            return True