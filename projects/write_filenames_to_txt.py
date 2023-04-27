import os

def write_filenames_to_txt(output_file, directory=os.path.dirname(os.path.abspath(__file__))):
    with open(output_file, "w") as file:
        for filename in os.listdir(directory):
            file.write(filename + "\n")

