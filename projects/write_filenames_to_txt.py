import os

def write_filenames_to_txt(output_file, directory=os.path.dirname(os.path.abspath(__file__))):
    with open(output_file, "w") as file:
        for entry in os.listdir(directory):
            entry_path = os.path.join(directory, entry)
            if os.path.isdir(entry_path):
                write_filenames_to_txt(output_file, entry_path)
            else:
                file.write(entry + "\n")
