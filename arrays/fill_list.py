#fill_list.py
def fill_list():
  # Create an empty list
  array = []

  # Keep prompting the user for input until they enter a blank line
  while True:
    # Get the user's input
    user_input = input("Enter a value : ")

    # Check if the input is blank
    if not user_input:
      # Exit the loop if the input is blank
      break

    # Convert the input to an integer
    user_input = int(user_input)

    # Append the input to the list if it is not blank
    array.append(user_input)

  # Return the list of input values
  return array

