import json
import csv
import pandas as pd
import numpy as np
from tqdm import tqdm  # tqdm 라이브러리 임포트
import random
import torch
import os
from collections import Counter

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
    
def get_data(file_path):
    # 파일 읽기 (인코딩을 cp949로 설정)
    # Read the file with 'cp949' encoding
    with open(file_path, "r", encoding='cp949') as file:
        lines = file.readlines()

    # Initialize empty list to store the rows
    data = []
    split_line = lines[3].split("_")
    print(split_line, split_line[0])
    # Extract Header info
    header_info = {
        "품명": lines[1].split("품    명:")[1].split("품    번:")[0].strip(),
        "품번": lines[1].split("품    번:")[1].strip(),
        "측정시간": lines[2].split("측정시간:")[1].split("측 정 자:")[0].strip(),
        "측정자": lines[2].split("측 정 자:")[1].strip(),
        "특기사항": lines[3].split(":")[1].strip(),
        "검사형태": lines[3].split("_")[1].strip(),
        "검사시간대": lines[3].split("_")[2].strip()+"간",
        "종물검사": lines[3].split("_")[3].strip()+"물",
        "품질상태": lines[3].split("_")[-1].strip()
    }
    print(header_info)
    if header_info['품질상태'] == '':
        header_info['품질상태'] = "NTC" # Need to Check

    # Iterate through the lines to extract the data
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Check if the line contains 번호 and 도형
        if line and line[0].isdigit():
            number, shape = line.split(maxsplit=1)

            # Read the next lines until an empty line or another header is found
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip()[0].isdigit():
                parts = lines[i].split()

                # Extract the data values with generalized handling for missing data
                if len(parts) >= 3:
                    item = parts[0]
                    # Check if parts has enough elements
                    if len(parts) == 7:
                        measured_value = parts[1]
                        standard_value = parts[2]
                        upper_tolerance = parts[3]
                        lower_tolerance = parts[4]
                        deviation = parts[5]
                        judgement = parts[-1]
                        
                    elif len(parts) == 6 and item == "SMmf": # SMmf 인 경우
                        measured_value = parts[1]
                        standard_value = parts[2]
                        upper_tolerance = parts[3]
                        lower_tolerance = parts[4]
                        deviation = parts[5]
                        judgement = '-'
                    else:
                        measured_value = parts[1]
                        standard_value = parts[2]
                        upper_tolerance = '-'
                        lower_tolerance = '-'
                        deviation = '-'
                        # Check if parts has judgement value
                        judgement = parts[-1] if len(parts) > 3 and is_float(parts[-1]) else '-'

                    row = [header_info['품명'],header_info['품번'],header_info['측정시간'],
                           header_info['측정자'],header_info['검사형태'],header_info['검사시간대'],
                           header_info['종물검사'],number, shape,
                           item, measured_value, standard_value,
                           upper_tolerance, lower_tolerance, deviation,
                           judgement,header_info['품질상태']]
                    data.append(row)

                i += 1
        else:
            i += 1

    # Convert the list of rows to a DataFrame
    df = pd.DataFrame(data, columns=[
        "품명", "품번", "측정시간",
        "측정자", "검사형태", "검사시간대",
        "종물검사", "번호", "도형",
        "항목", "측정값", "기준값",
        "상한공차", "하한공차", "편차",
        "판정","품질상태"
        ])

    return df



if __name__ == "__main__":
    files = []
    # path = os.getcwd() + "\\02_최종_데이터\\전처리전_데이터\\all_data\\"
    path = os.getcwd() + "\\99_backup\\init_data(702)\\"

    text_files = os.listdir(path)
    files.extend(text_files)
    # output_dir = os.path.join("C:\\Users\\Administrator\\Workspace\\수업\\실증적 AI개발 프로젝트\\Data\\02_최종_데이터\\전처리전_데이터\\통합")
    output_dir = os.path.join("C:\\Users\\Administrator\\Workspace\\수업\\실증적 AI개발 프로젝트\\Data\\99_backup\\test")
    print(output_dir)    
    # 디렉토리가 존재하지 않으면 생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("len of the file:",len(text_files))
    for file_name in text_files:
        # print(file_name)
        file_path = path + file_name
        df = get_data(file_path)
        output_file = os.path.join(output_dir, f"{file_name[:-4]}.csv")  # .txt를 제거하고 .csv로 변경
        df.to_csv(output_file, index=False)