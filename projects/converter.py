from pdf2docx import parse
from pydub import AudioSegment

#audio_converter.py
def convert_audio(input_path, output_path):
    # Get the input file extension
    input_file_ext = input_path.split(".")[-1]
    # Get the output file extension
    output_file_ext = output_path.split(".")[-1]
    # Load audio file
    audio = AudioSegment.from_file(input_path, format=input_file_ext)
    # Export audio file
    audio.export(output_path, format=output_file_ext)

#pdf_to_word_converter.py    
def pdf_to_word(pdf_path):
	# Generate the output file name based on the input file name
	docx_path = pdf_path.replace(".pdf", ".docx")  
	# Convert the PDF to Word
	parse(pdf_path, docx_path) 
	print(f"Conversion complete. Output file saved as {docx_path}")