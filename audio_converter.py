from pydub import AudioSegment

# Get input and output file names from user
input_file = input("Enter input file name: ")
output_file = input("Enter output file name: ")

# Get the input file extension
input_file_ext = input_file.split(".")[-1]

# Get the output file extension
output_file_ext = output_file.split(".")[-1]

# Load audio file
audio = AudioSegment.from_file(input_file, format=input_file_ext)

# Export audio file
audio.export(output_file, format=output_file_ext)
