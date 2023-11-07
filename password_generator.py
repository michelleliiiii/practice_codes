'''
This function generates passwords between min_length and max_length.
Letters are always included, while numbers and special characters can be optional.
'''

import random
import string


def generate_password (min_length, max_length, numbers = True, special_character = True):
    letter = string.ascii_letters
    digit = string.digits
    special = string.punctuation

    character = letter
    if numbers:
        character += digit
    if special_character:
        character += special
    password = ""

    meet_criteria = False
    has_number = False
    has_special = False
    has_letter = False

    while True:
        while len(password) < min_length or (not meet_criteria):
            new = random.choice (character)
            password += new
            if new in digit:
              has_number = True
            if new in special:
                has_special = True
            if new in letter:
                has_letter = True

            meet_criteria = has_letter
            if numbers:
                meet_criteria = meet_criteria and has_number          
            if special_character:
                meet_criteria = meet_criteria and has_special 

        if len(password) < max_length:
            return password
        else:
            password = ""
    


min_length = int (input("The minimum length of password:"))
max_length = int (input("The maximum length of password:"))
numbers = input("Do you want to have numbers? (y/n)").lower() == "y"
special_character = input("Do you want to have special characters? (y/n)").lower() == "y"
print ("The generated password is :", generate_password (min_length, max_length, numbers, special_character))
