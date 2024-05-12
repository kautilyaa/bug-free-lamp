"""
Given the label name - find the label type
    """
from validator_utils import is_pattern_matching

class LabelTypeIdentifier:
    def __init__(self,config) -> None:
        self.config = config
    
    def get_label_type(self, label):
        matching_label_types = []
        for key, value in self.config.items():
            if is_pattern_matching(label, value["patterns"]):
                a = value["patterns"]
                print(f"{label}           {a}")
                matching_label_types.append(key)
        return matching_label_types