import phonenumbers
from phonenumbers import carrier, geocoder, timezone

def get_info(mobile_number, filename, is_one):
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
    try:
        with open(file_path, 'r') as file:
            phone_numbers = file.read().splitlines()
            for phone_number in phone_numbers:
                get_info(phone_number, filename, is_one = False)
        print('Information saved in {}'.format(filename))
    except FileNotFoundError:
        print('File not found. Please provide a valid file path.')

def main():
    choice = int(input("1. Enter a single phone number\n2. Enter the path to a text file\n"))
    filename = input("Enter the name of the file you want to save the information: ")
    if choice == 1:
        mobile_number = input("Enter Phone number with country code (+xx xxxxxxxxx): ")
        get_info(mobile_number, filename, is_one = True)
    elif choice == 2:
        file_path = input("Enter the path to the text file: ")
        enter_file_path(filename, file_path)

main()