import pandas as pd
import os

# Set input and output directories
input_directory = "C:\\Users\\Administrator\\Workspace\\수업\\실증적 AI개발 프로젝트\\Data\\02_최종_데이터\\전처리전_데이터\\통합"
# input_directory = "C:\\Users\\Administrator\\Workspace\\수업\\실증적 AI개발 프로젝트\\Data\\99_backup\\test\\"
output_file = "cmm_data-real-last.csv"

# Create an empty list
rows = []
quality_status = []
all_file_names = []

# Flag to track if the first file has been processed
first_file_processed = False
shape_item = None  # To store the shape_item from the first file

# Loop through all files in the input directory
count = 0 
for filename in os.listdir(input_directory):
    if filename.endswith(".csv"):
        # Read CSV file
        file_path = os.path.join(input_directory, filename)
        df = pd.read_csv(file_path, delimiter=',', encoding='UTF-8', index_col=False) # Set index_col=False
        #print(df)
        
        # Exclude rows where the value of the 'Item' column is "SMmf"
        df = df[df['항목'] != "SMmf"]

        # Create ‘Shape_Item’ column
        df['도형_항목'] = df['도형'] + '_' + df['항목'] 
    
        # Change missing deviation values ​​to 'NaN'or 0 instead of '-'        
        df['상한공차'] = df['상한공차'].replace('-', 0) 
        df['하한공차'] = df['하한공차'].replace('-', 0) 
        df['편차'] = df['편차'].replace('-', 0)
        
        
        # Convert '편차' column to numeric
        df['측정값'] = pd.to_numeric(df['측정값'], errors='coerce')
        df['기준값'] = pd.to_numeric(df['기준값'], errors='coerce')
        df['상한공차'] = pd.to_numeric(df['상한공차'], errors='coerce')
        df['하한공차'] = pd.to_numeric(df['하한공차'], errors='coerce')
        df['편차'] = pd.to_numeric(df['편차'], errors='coerce')


        # Check if this is the first file
        if not first_file_processed:
            # Store the shape_item from the first file
            shape_item = df['도형_항목'].tolist()
            print(df.shape)
            print(len(df['도형_항목'].tolist()))
            first_file_processed = True
            continue  # Move to the next file

        print(df.shape)
        print(len(df['도형_항목'].tolist()))

        # Check if the current file has the same structure as the first file
        if df['도형_항목'].tolist() != shape_item:
            count += 1
            #print(f"Skipping file: {filename}. Structure does not match the first file. shape : {df.shape}")
            continue  # Skip processing for this file
        
        # Add quality status column
        if df.iloc[1, 16] == 'OK': # If second column is 'OK', OK이면 1 레이블을 주는듯?
            quality_status.append(1)
        
        elif df.iloc[1, 16] == 'NG': # If second column is 'OK', OK이면 1 레이블을 주는듯?
            quality_status.append(0)
        else:
            quality_status.append(2) # 비어있으면 레이블 2
                # Extract deviation values
        
        measures = df['측정값'].tolist()
        ref_value = df['기준값'].tolist()
        upper = df['상한공차'].tolist()
        lower = df['하한공차'].tolist()
        deviations = df['편차'].tolist()

        combined_list = []
        combined_list.extend(measures)
        combined_list.extend(ref_value)
        combined_list.extend(upper)
        combined_list.extend(lower)
        combined_list.extend(deviations)
        
        # Add to list
        rows.append(combined_list)
        
        all_file_names.append(os.path.splitext(filename)[0]) # Save the file name without extension


final_shape = []
headers = ['측정값','기준값','상한공차','하한공차','편차']

for header in headers:
    for dohang in shape_item:
        final_shape.append(dohang + '_' + header)
    


# Create a data frame by arranging deviations as rows and shape_items as columns
combined_data = pd.DataFrame(rows, columns=final_shape) # Create a DataFrame using the shape_item from the first file

# Add file name as first column
combined_data.insert(0, '파일명', all_file_names)

# Add quality status column
combined_data['품질상태'] = quality_status

# Save the results as a CSV file
combined_data.to_csv(output_file, encoding='cp949', index=False) # Do not store index
