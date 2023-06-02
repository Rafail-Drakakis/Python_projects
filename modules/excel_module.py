import tabula, openpyxl, os, tempfile, pandas as pd

def merge_excel_files(input_excel_paths, output_excel_path):
    # Create a new Excel workbook
    output_workbook = openpyxl.load_workbook(input_excel_paths[0])

    # Iterate over the remaining Excel files and copy their sheets to the output workbook
    for input_excel_path in input_excel_paths[1:]:
        input_workbook = openpyxl.load_workbook(input_excel_path)
        for sheet_name in input_workbook.sheetnames:
            input_sheet = input_workbook[sheet_name]
            output_workbook.create_sheet(title=sheet_name)
            output_sheet = output_workbook[sheet_name]
            for row in input_sheet.iter_rows():
                for cell in row:
                    output_sheet[cell.coordinate].value = cell.value

    # Save the merged workbook
    output_workbook.save(output_excel_path)

def read_pdf(input_pdf_path):
    # Read PDF and convert each page to a separate DataFrame
    return tabula.read_pdf(input_pdf_path, pages='all')

def write_data_frames_to_excel(data_frames, output_excel_path):
    # Create an Excel file using openpyxl engine
    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as excel_writer:
        # Write each DataFrame to a different worksheet in the Excel file
        for i, df in enumerate(data_frames):
            df.to_excel(excel_writer, sheet_name=f"Sheet{i+1}", index=False)

def merge_excel_sheets(input_excel_path):
    # Read each sheet into a DataFrame and concatenate them
    dfs = pd.read_excel(input_excel_path, sheet_name=None)
    return pd.concat(dfs.values(), ignore_index=True)

def save_merged_excel(merged_data_frame, merged_excel_path):
    # Save merged data to a new Excel file
    merged_data_frame.to_excel(merged_excel_path, index=False)

def shift_cells_left_in_workbook(input_excel_path, output_excel_path):
    # Load the Excel workbook
    excel_workbook = openpyxl.load_workbook(input_excel_path)

    # Iterate over each worksheet in the workbook
    for worksheet_name in excel_workbook.sheetnames:
        excel_worksheet = excel_workbook[worksheet_name]

        # Iterate over each row in the worksheet
        for row in excel_worksheet.iter_rows():
            empty_cell_list = []
            for current_cell in row:
                # Check if the cell is empty
                if current_cell.value is None:
                    empty_cell_list.append(current_cell)
                else:
                    # If there are empty cells before the current cell, move the current cell to the left
                    for empty_cell_to_fill in empty_cell_list:
                        empty_cell_to_fill.value = current_cell.value
                        current_cell.value = None
                        empty_cell_list.remove(empty_cell_to_fill)
                        empty_cell_list.append(current_cell)
                        break

    # Save the modified workbook
    excel_workbook.save(output_excel_path)

def pdf_to_excel_converter(input_pdf_path, temp_excel_path):
    # Read PDF and convert each page to a separate DataFrame
    pdf_data_frames = read_pdf(input_pdf_path)

    # Write the DataFrames to a temporary Excel file
    write_data_frames_to_excel(pdf_data_frames, temp_excel_path)

def process_pdf(input_pdf_path):
    output_excel_path = os.path.splitext(input_pdf_path)[0] + ".xlsx"

    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp_file:
        temp_excel_path = temp_file.name
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as merged_file:
        merged_excel_path = merged_file.name

    try:
        # Convert PDF to Excel
        pdf_to_excel_converter(input_pdf_path, temp_excel_path)

        # Merge Excel sheets
        merged_data_frame = merge_excel_sheets(temp_excel_path)
        # Save the merged data frame to a temporary file
        save_merged_excel(merged_data_frame, merged_excel_path)
        # Move the merged file to the output path
        os.replace(merged_excel_path, output_excel_path)

        option = input("Do you want to shift empty cells? (yes/no) ")
        if option == "yes":
            # Move cells left in the output Excel file
            shift_cells_left_in_workbook(output_excel_path, output_excel_path)
        print(f'file {output_excel_path} have created succesfully ')
    finally:
        # Remove temporary files
        os.remove(temp_excel_path)
        if os.path.exists(merged_excel_path):
            os.remove(merged_excel_path)

process_pdf("table.pdf")            