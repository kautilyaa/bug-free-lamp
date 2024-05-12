import re
from dateutil import parser
from abc import abstractmethod, ABCMeta
from typing import List
import logging
from itertools import groupby

class RuleResult:
    def __init__(self, flag, message, level, label_type) :
        # pass
        self.__flag = flag
        self.__message = message
        self.__level = level
        self.__label_type = label_type

    def get_validation_results(self):
        return {
            "flag":self.__flag,
            "message":self.__message,
            "level":self.__level,
            "label_type":self.__label_type
        }
    
class AbstractRule(metaclass = ABCMeta):
    def __init__(self):
        self.level = "Validated"
        self.message = "Validation Successful"

    @abstractmethod
    def check(self, value):
        return "abstract method 'check' is not implemented"
    
class Rule(AbstractRule):
    def __init__(self, label_type, rule_fn, msg, level, spl_chars_allowed) -> None:
        super().__init__()
        self.label_type = label_type
        self.rule_fn = rule_fn
        self.msg = msg
        self.level = level
        self.spl_chars_allowed = spl_chars_allowed

    def check(self, value) -> RuleResult:
        # return super().check(value)
        flag = eval("Rule."+self.rule_fn+f"('{value}', '{self.spl_chars_allowed}')")
        if flag:
            self.message = "Validation Successful"
            self.level = "Validated"

        logging.info(f"Validation {value}, {flag}, {self.message}, {self.level}, {self.label_type}")
        return flag

    @staticmethod
    def is_only_number(field_val, spl_chars = ""):
        return bool(re.search(r'^[0-9'+spl_chars+']+$', field_val))
    
    @staticmethod
    def is_only_alphabet(field_val, spl_chars = ""):
        return bool(re.search(r'^[A-Za-z'+spl_chars+']+$', field_val))
    
    @staticmethod
    def is_alphanumeric(field_val, spl_chars = ""):
        return bool(re.search(r'^[A-Za-z0-9'+spl_chars+']+$', field_val))
    
    @staticmethod
    def is_valid_date(field_value, spl_chars = ""):
        try:
            parsed_date = parser.parse(field_value)
            return True
        except Exception as e:
            return False
    
    @staticmethod
    def is_valid_email(field_val, spl_chars = ""):
        return bool(re.search(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', field_val))
    
    @staticmethod
    def check_continuous_spl_chrs(field_val, spl_chars = ""):
        groups = groupby(field_val)
        return len([char for char, group in groups if char in '\+&-=/' and sum(1 for _ in group) > 2]) == 0
    
    @staticmethod
    def check_others(field_value, spl_chars = ""):
        return True
    
class RuleManager:
    def __init__(self, config) -> None:
        # pass
        self.config = config

    def get_rules(self, label_type) -> List[Rule]:
        error_msg = self.config[label_type]["error_rules"]["error_msg"]
        level = self.config[label_type]["error_rules"]["level"]
        spl_chars_allowed = self.config.get(label_type).get("spl_chars_allowed","")
        rules_list = [Rule(label_type, r, error_msg, level, spl_chars_allowed)
                      for r in self.config[label_type]["error_rules"]["rules"]]
        return rules_list
    
if __name__ == '__main__':
    r1 = Rule("numerical_check", "is_only_number", "Not a valid number")
    r1.check("123")