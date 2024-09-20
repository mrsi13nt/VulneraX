import itertools
import random
from typing import List, Dict

class PasswordGenerator:
    def __init__(self):
        self.leet_dict = {
            'a': '4', 'b': '8', 'e': '3', 'l': '1', 'o': '0', 's': '5', 't': '7', 'g': '9', 'i': '1', 'z': '2'
        }
        self.subs_dict = {
            'a': '@', 's': '$', 'i': '!', 'o': '0', 'e': '3'
        }
    
    def leet_transform(self, word: str) -> str:
        return ''.join(self.leet_dict.get(c.lower(), c) for c in word)
    
    def substitute_symbols(self, word: str) -> str:
        return ''.join(self.subs_dict.get(c.lower(), c) for c in word)
    
    def reverse_string(self, word: str) -> str:
        return word[::-1]
    
    def mix_case(self, word: str) -> str:
        return ''.join(random.choice([c.lower(), c.upper()]) for c in word)
    
    def date_variations(self, date: str) -> List[str]:
        return [date, date[-2:], date[:4], date[:2], date[2:4] + date[:2] + date[4:]]

    def shuffle_elements(self, elements: List[str]) -> List[str]:
        combined_passwords = set()
        for i in range(1, len(elements) + 1):
            for combo in itertools.permutations(elements, i):
                combo_str = ''.join(combo)
                combined_passwords.update({
                    combo_str,
                    self.leet_transform(combo_str),
                    self.substitute_symbols(combo_str),
                    self.reverse_string(combo_str),
                    self.mix_case(combo_str),
                    combo_str.capitalize(),
                    combo_str.upper(),
                    combo_str.lower()
                })
        return list(combined_passwords)

    def generate_password_list(self, info_dict: Dict[str, List[str]]) -> List[str]:
        elements = []
        for values in info_dict.values():
            elements.extend(values)

        password_list = self.shuffle_elements(elements)
        
        for key, values in info_dict.items():
            if 'date' in key:
                for date in values:
                    password_list.extend(self.date_variations(date))
        
        return list(set(password_list))

def get_user_input(prompt: str) -> List[str]:
    return input(prompt).split(',')

def wordlist():
    generator = PasswordGenerator()

    user_info = {
        'first_name': get_user_input("Enter your first name(s) (comma-separated if multiple): "),
        'last_name': get_user_input("Enter your last name(s) (comma-separated if multiple): "),
        'nickname': get_user_input("Enter your nickname(s) (comma-separated if multiple): "),
        'phone_number': get_user_input("Enter your phone number(s) (comma-separated if multiple): "),
        'birth_date': get_user_input("Enter your birth date(s) (comma-separated if multiple) (format: DDMMYYYY): "),
        'job_title': get_user_input("Enter your job title(s) (comma-separated if multiple): "),
        'pet_name': get_user_input("Enter your pet name(s) (comma-separated if multiple): "),
        'father_name': get_user_input("Enter your father's name(s) (comma-separated if multiple): "),
        'father_birth_date': get_user_input("Enter your father's birth date(s) (comma-separated if multiple) (format: DDMMYYYY): "),
        'father_phone_number': get_user_input("Enter your father's phone number(s) (comma-separated if multiple): "),
        'mother_name': get_user_input("Enter your mother's name(s) (comma-separated if multiple): "),
        'mother_birth_date': get_user_input("Enter your mother's birth date(s) (comma-separated if multiple) (format: DDMMYYYY): "),
        'mother_phone_number': get_user_input("Enter your mother's phone number(s) (comma-separated if multiple): "),
        'partner_name': get_user_input("Enter your partner's name(s) (comma-separated if multiple): "),
        'partner_birth_date': get_user_input("Enter your partner's birth date(s) (comma-separated if multiple) (format: DDMMYYYY): "),
        'partner_first_date': get_user_input("Enter your partner's first date(s) (comma-separated if multiple) (format: DDMMYYYY): "),
        'partner_phone_number': get_user_input("Enter your partner's phone number(s) (comma-separated if multiple): "),
        'best_friend_name': get_user_input("Enter your best friend's name(s) (comma-separated if multiple): "),
        'best_friend_birth_date': get_user_input("Enter your best friend's birth date(s) (comma-separated if multiple) (format: DDMMYYYY): "),
    }
    print('creating your passwordlist...')
    print('please wait a little')
    passwords = generator.generate_password_list(user_info)
    
    with open('password_list.txt', 'w') as f:
        for password in passwords:
            f.write(f"{password}\n")
    
    print("[\033[32m+\033[0m] Password list generated and saved to password_list.txt.")