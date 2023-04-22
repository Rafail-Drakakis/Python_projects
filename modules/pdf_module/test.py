from pdf_module import pdf_to_word
from pdf_module import merge_pdfs
from pdf_module import split_pdf
from pdf_module import pdf_to_img
import os

if __name__ == "__main__":
    pdf_to_word("sample.pdf")
    merge_pdfs(2) 
    split_pdf("sample.pdf", [7,"2-5"]) 
    pdf_to_img("sample.pdf")

    os.remove("sample_pages_7_2_3_4_5.pdf")
    os.remove("merged_pdf.pdf")
    os.remove("sample.docx")
    for index in range(1, 11):
        os.remove(f'page_{index}.jpg')