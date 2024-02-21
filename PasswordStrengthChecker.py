import re
import requests


class PasswordStrengthChecker:
    @staticmethod
    def check_strength(password):
        PasswordStrengthChecker.has_consecutive_characters(password)
        if len(password) < 8 or PasswordStrengthChecker.has_consecutive_characters(password):
            return "red"

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

    @staticmethod
    def has_consecutive_characters(password):
        for i in range(len(password) - 1):
            if password[i] == password[i + 1]:
                return True
        return False

    @staticmethod
    def check_password_strength():
        url = "https://www.passwordmonster.com/check_password_strength"
        data = {"password": "9f86d08188"}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            result = response.json()
            return result["strength"]
        else:
            return None

# David Pinheiro
