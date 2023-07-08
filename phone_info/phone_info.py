import phonenumbers
from phonenumbers import carrier, geocoder, timezone

def get_info(mobile_number, filename, is_one):
    """
    The function `get_info` takes a mobile number, a filename, and a boolean flag as input, and writes
    information about the mobile number to the specified file if the number is valid.
    
    :param mobile_number: The mobile_number parameter is the phone number that you want to get
    information about. It should be in a string format
    :param filename: The `filename` parameter is the name of the file where the information about the
    mobile number will be saved
    :param is_one: The parameter "is_one" is a boolean value that determines whether to print a
    confirmation message after saving the information for the phone number. If "is_one" is True, a
    confirmation message will be printed. If "is_one" is False, no confirmation message will be printed
    """
    parsed_number = phonenumbers.parse(mobile_number)
    if phonenumbers.is_valid_number(parsed_number):
        with open(filename, 'a') as file:
            file.write('Phone Number: {}\n'.format(parsed_number))
            time_zones = timezone.time_zones_for_number(parsed_number)
            if time_zones:
                file.write('Phone Number belongs to region: {}\n'.format(', '.join(time_zones)))
            else:
                file.write('Phone Number region not found\n')
            file.write('Service Provider: {}\n'.format(carrier.name_for_number(parsed_number, "en")))
            file.write('Phone number belongs to country: {}\n\n'.format(geocoder.description_for_number(parsed_number, "en")))
        if is_one:
            print('Information for the phone number {} saved in {}'.format(mobile_number, filename))
    else:
        print("Invalid mobile number:", mobile_number)

def enter_file_path(filename, file_path):
    """
    The function `enter_file_path` reads a file containing phone numbers, calls the `get_info` function
    for each phone number, and saves the information in the specified file.
    
    :param filename: The filename parameter is the name of the file where the information will be saved
    :param file_path: The file_path parameter is a string that represents the path to the file that
    contains phone numbers
    """
    try:
        with open(file_path, 'r') as file:
            phone_numbers = file.read().splitlines()
            for phone_number in phone_numbers:
                get_info(phone_number, filename, is_one = False)
        print('Information saved in {}'.format(filename))
    except FileNotFoundError:
        print('File not found. Please provide a valid file path.')

def get_single_phone_number(filename):
    mobile_number = input("Enter the phone number with the country code (+xx xxxxxxxxx): ")
    get_info(mobile_number, filename, is_one=True)

def get_file_phone_numbers(filename):
    file_path = input("Enter the path to the text file: ")
    enter_file_path(filename, file_path)

def main():
    try:
        choice = int(input("1. Enter a single phone number\n2. Enter the path to a text file: "))
        if choice == 1:
            filename = input("Enter the name of the file you want to save the information: ")
            get_single_phone_number(filename)
        elif choice == 2:
            filename = input("Enter the name of the file you want to save the information: ")
            get_file_phone_numbers(filename)
        else:
            print("Invalid choice. Please choose 1 or 2.")

    except ValueError:
        print("Enter an integer")
        exit(0)
main()