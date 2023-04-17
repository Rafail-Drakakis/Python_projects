import pdf2docx

def pdf_to_word():
	pdf_path = input("Enter the name of the PDF file to convert (include the .pdf extension): ") # Prompt the user for the input file name
	docx_path = pdf_path.replace(".pdf", ".docx")  # Generate the output file name based on the input file name
	pdf2docx.parse(pdf_path, docx_path) # Convert the PDF to Word
	print(f"Conversion complete. Output file saved as {docx_path}") #print a message

pdf_to_word()
