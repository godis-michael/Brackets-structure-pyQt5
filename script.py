import re


class BracketsErrors:
    def __init__(self, bracket_sign, error_code, pattern):
        self.bracket_sign = bracket_sign
        self.error_code = error_code
        self.pattern = pattern

    def delete(self, bracket_sign, bracket_input, arr_first):
        match = ''
        bracket_temp = bracket_input
        while match != bracket_temp:
            match = bracket_temp
            bracket_temp = re.sub(self.pattern, '', bracket_temp)
            if match == bracket_temp:
                for char in bracket_temp:
                    if char == bracket_sign:
                        arr_first.append(char)
                return len(arr_first)

    def count(self, bracket_input, arr_second):
        match = re.findall(self.pattern, bracket_input)
        if len(match) != 0:
            arr_second.append(len(match))
        return sum(arr_second)
