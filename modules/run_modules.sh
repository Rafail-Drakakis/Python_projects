#!/bin/bash

# Run all the Python scripts in the image_module folder
cd image_module
for file in *.py
do
  python3 "$file"
done

# Run all the Python scripts in the pdf_module folder
cd ../pdf_module
for file in *.py
do
  python3 "$file"
done
