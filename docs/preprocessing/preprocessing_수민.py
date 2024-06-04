import pandas as pd
import os
import zipfile

def extract_dataframe_from_file(file_path):
    # 'cp949' 인코딩으로 파일 읽기
    with open(file_path, "r", encoding='cp949') as file:
        lines = file.readlines()

     # 행을 저장할 빈 리스트 초기화
    data = []

    # 헤더 정보 추출
    header_info = {
        "품명": lines[1].split("품    명:")[1].split("품    번:")[0].strip(),
        "품번": lines[1].split("품    번:")[1].strip(),
        "측정시간": lines[2].split("측정시간:")[1].split("측 정 자:")[0].strip(),
        "측정자": lines[2].split("측 정 자:")[1].strip(),
        "특기사항": lines[3].split(":")[1].strip(),
        "검사형태": lines[3].split("_")[1].strip(),
        "검사시간대": lines[3].split("_")[2].strip()+"간",
        "종믈검사": lines[3].split("_")[3].strip()+"물",
        "품질상태": lines[3].split("_")[-1].strip()  
    }
    if header_info['품질상태'] == '':
        header_info['품질상태'] = "NTC" ##### Check

    # 데이터 추출을 위해 텍스트 파일의 각 줄을 반복
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # 번호와 도형이 있는 줄인지 확인
        if line and line[0].isdigit():
            number, shape = line.split(maxsplit=1)

            # 비어 있거나 다른 헤더가 나올 때까지 다음 줄을 읽음
            i += 1
            while i < len(lines) and lines[i].strip() and not lines[i].strip()[0].isdigit():
                parts = lines[i].split()

                # 누락된 데이터를 처리하고 데이터 값을 추출
                if len(parts) >= 3:
                    item = parts[0]
                    if item == '평면도':
                        measured_value = parts[1]
                        standard_value = parts[2]
                        upper_tolerance = '-'
                        lower_tolerance = '-'
                        deviation = '-'
                        judgement = parts[-1]
                    elif item == 'SMmf':
                        measured_value = parts[1]
                        standard_value = parts[2]
                        upper_tolerance = parts[3]
                        lower_tolerance = parts[4]
                        deviation = parts[-1]
                        judgement = '-'
                    elif item == '원통도' :
                        measured_value = parts[1]
                        standard_value = parts[2]
                        upper_tolerance = '-'
                        lower_tolerance = '-'
                        deviation = '-'
                        judgement = '-'
                    elif item == '직각도':
                        measured_value = parts[1]
                        standard_value = parts[2]
                        upper_tolerance = '-'
                        lower_tolerance = '-'
                        deviation = '-'
                        judgement = parts[-1]
                    elif item == '동심도':
                        measured_value = parts[1]
                        standard_value = parts[2]
                        upper_tolerance = '-'
                        lower_tolerance = '-'
                        deviation = '-'
                        judgement = '-'
                    elif item == '평행도':
                        measured_value = parts[1]
                        standard_value = parts[2]
                        upper_tolerance = '-'
                        lower_tolerance = '-'
                        deviation = '-'
                        judgement = parts[-1]
                    else:
                        measured_value = parts[1]
                        standard_value = parts[2]
                        upper_tolerance = parts[3]
                        lower_tolerance = parts[4]
                        deviation = parts[5]
                        judgement = parts[-1]

                    row = [header_info['품명'],header_info['품번'],header_info['측정시간'],
                           header_info['측정자'],header_info['검사형태'],header_info['검사시간대'],
                           header_info['종믈검사'],number, shape,
                           item, measured_value, standard_value,
                           upper_tolerance, lower_tolerance, deviation,
                           judgement,header_info['품질상태']]
                    data.append(row)

                i += 1
        else:
            i += 1

    # 행의 리스트를 DataFrame으로 변환
    df = pd.DataFrame(data, columns=[
        "품명", "품번", "측정시간",
        "측정자", "검사형태", "검사시간대",
        "종믈검사", "번호", "도형",
        "항목", "측정값", "기준값",
        "상한공차", "하한공차", "편차",
        "판정","품질상태"
        ])

    return df

if __name__ == "__main__":
    # 현재 디렉토리(드라이브에 있는 datasets 다운 받아서 저장한 디렉토리)
    data_path = os.getcwd()
    print(data_path)
    data_list = os.listdir(data_path)
    all_ex_files = list


    # 파일 목록 반복
    for file_name in data_list:
        if file_name.endswith(".zip"):
            # zip 파일 열기
            with zipfile.ZipFile(os.path.join(data_path, file_name), 'r') as zip_ref:
                # 모든 파일 압축 해제
                zip_ref.extractall(data_path)
                # 압축 해제된 파일 목록 가져오기
                extracted_files = zip_ref.namelist()
                # 압축 해제 후 파일 수 확인
                num_files_after = len(extracted_files)
                print(extracted_files)  ###########################['datasets/small_data.zip', 'datasets/large_data.zip']

                dataset_path = os.getcwd()+"\datasets"
                dataset_list = os.listdir(dataset_path)
                print(dataset_list)    ############################['large_data.zip', 'small_data.zip']

                for file_name in dataset_list:
                    print(file_name)
                    if file_name.endswith(".zip"):
                        with zipfile.ZipFile(os.path.join(dataset_path, file_name), 'r') as zip_ref:
                            # 모든 파일 압축 해제
                            info = zip_ref.infolist()
                            for i in info :
                                i.filename = i.filename.encode('cp437').decode('euc-kr')
                                zip_ref.extract(i)

                            # 압축 해제된 파일 목록 가져오기
                            extracted_files = zip_ref.namelist()
                            num_files_after = len(extracted_files)
                            # print(num_files_after)
                            for extracted_file in extracted_files:
                                df_test = extract_dataframe_from_file(os.path.join(data_path, extracted_file))
                                df_test.to_csv(os.path.join(data_path, os.path.splitext(extracted_file)[0] + ".csv"), index=False, encoding='cp949')
