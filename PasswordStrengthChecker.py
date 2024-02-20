import re


class PasswordStrengthChecker:
    @staticmethod
    def check_strength(password):
        if len(password) < 8:
            return "Weak"

        has_uppercase = bool(re.search(r'[A-Z]', password))
        has_lowercase = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*()-_+=]', password))

        if has_uppercase and has_lowercase and has_digit and has_special:
            return "green"
        elif has_uppercase or has_lowercase or has_digit or has_special:
            return "yellow"
        else:
            return "red"
