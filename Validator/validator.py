from label_type_identifier import LabelTypeIdentifier
from rules import RuleManager, RuleResult
import os,json
import logging
from config import config_validator

class ValidationResult:
    def __init__(self, rule_obj) -> None:
        self.rule = rule_obj
    
class Validator:
    def __init__(self, config_json) -> None:
        if os.path.exists(config_json):
            with open(config_json,"r", encoding="utf-8") as json_file:
                self.config = json.load(json_file)
            # print(self.config)
            if not self.is_config_valid(self.config):
                raise ValueError("Invalid config file format")
            self.label_type_identifier = LabelTypeIdentifier(self.config)
            # print(self.label_type_identifier)
            self.rule_mgr = RuleManager(self.config)
        else:
            raise ValueError(f"File not found - {config_json}")
        
    def is_config_valid(self, config):
        for key, value in config.items():
            validator_flag = config_validator.validate(value)
            if not validator_flag:
                return False
        return True

    def run(self, data_dict):
        ret = {}
        for label, value in data_dict.items():
            logging.info(f"Checking validation for field - {label}")
            print(f"Checking validation for field - {label} ::::: {value}")
            label_types = self.label_type_identifier.get_label_type(str(label).lower())
            print(label_types)
            if len(label_types) == 0:
                label_types=["others"]

            if len(label_types) > 1:
                logging.warning("More than one label type found")
            # print(f"{label}   {label_type}")
            rule_result_objs = []
            for label_type in label_types:
                rules =  self.rule_mgr.get_rules(label_type)
                rule_flag = True
                for rule in rules:
                    if not rule.check(value):
                        rule_flag = False
                        break

                rule_result_objs.append(RuleResult(rule_flag, rule.message, rule.level, rule.label_type)) 
            ret[label] = rule_result_objs
        return ret

if __name__ == "__main__":
    validator = Validator("labels_defination.json")
    ret = validator.run(
        {
            "Order Number" : "-===8089dsfdf=================+++++",
            "acc no" : "12345"
        }
    )

    for key, value in ret.items():
        print(ret[key][0].get_validation_results())

