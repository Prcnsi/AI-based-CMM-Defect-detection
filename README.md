# Deep-learning-based_CMM_Anomaly-detection
# 주제: CMM 데이터 이상치 탐지 딥러닝 모듈 개발

### 1 CMM(Coordinate Measuring Machine)이란? 
- CMM(Coordinate Measuring Machine) 3차원 측정기로 대상물의치수를측정하는기기
- CMM은 자동차/항공 부품 물체를 측정하여 복잡한 형상을 데이터화하는데 사용됨.
- 제품 제작 이후에 제품이 치수대로 잘 가공되었는지 확인하기 위해 사용됨.

### 2 프로젝트 목표 
- 기존에는 제품 제작 이후 검수 단계에서 사람이 직접 CMM 데이터를 보고 불량을 판별했다. 
- 본 프로젝트의 목표는 딥러닝을 사용해서 CMM 데이터의 불량을 판별하는 모듈 개발하는 것이다.
- 이를 통해 기존에 불필요하게 소비되던 시간과 비용을 감축하고, 이를 통해 더욱 효율적인 워크플로우 구축이 가능. 

### 3. 기존 워크플로우
- 기존 워크플로우는 CMM 데이터에서 제품의 불량을 판별하는데 두 단계의 절차를 거쳤다.  
  ![image](https://github.com/Prcnsi/Deep-learning-based_CMM_Defect-detection/assets/86015194/6dfcd177-7c69-4095-8781-8b04ef75e3fa)

- 1차 검수 시 측정사원이 데이터로부터 불량을 판별해서 이때 정상으로 나오면 문제가 없거나 불량(Defective)으로 나오거나 판정 불가로 나오면 2차 검수가 필요하다. 2차 검수에서는 불량이나 판정불가인 제품에 대해 더 상위 측정 실장이 재측정, 재검수를 통해 최종 불량 여부를 판별한다.
- 불필요한 재측정과 수작업으로 인해 기존 워크플로우에서는 불필요한 비용과 시간이 많이 소모됐다.
  
![image](https://github.com/Prcnsi/Deep-learning-based_CMM_Defect-detection/assets/86015194/05d53fb9-c52a-4dc3-ba30-588b28aa24fc)

### 4. 머신러닝 기반 불량품 판별 실험 결과
- 비용 효율성 측면에서 우선 머신러닝으로 CMM 불량 판별을 수행한 결과 성능은 아래 표와 같다. 
- 실험은 3가지 그룹에 대해서 평가를 진행, 첫 번째는 CMM 데이터의 주요 특성만으로 머신러닝 모델을 학습, 평가한 결과 평균 약 86%의 성능에 도달했다ㅏ.
- 두 번째로 CMM의 모든 특성에 대해 평가한 결과도 약 85%의 정확도로 주요 특성 실험 결과와 유사했다. 
- 마지막으로 PCA로 CMM 데이터의 차원을 축소해서 성능은 평가한 결과 약 99%의 높은 정확도를 보였다. 

| 모델 | 기준 | 주요 Feature | 모든 Feature | 차원 축소 후 |
|------|-----|--------------|--------------|--------------|
| <strong>Random Forest</strong> | <strong>0.83 (+10%)</strong> | <strong>0.88</strong> | <strong>0.89</strong> | <strong>1.0</strong> |
| Logistic regression | 0.45 | 0.83 | 0.82 | <strong>1.0</strong> |
| KNN (K-Nearest Neighbors) | 0.62 | 0.87 | 0.87 | <strong>1.0</strong> |
| SVM(Support Vector Machine) | 0.45 | 0.84 | 0.87 | <strong>1.0</strong> |
| Gradient Boosting | 0.52 | 0.89 | 0.88 | <strong>0.99</strong> |
| XGBoost | 0.53 | 0.9 | 0.9 | <strong>1.0</strong> |
| <strong>평균</strong> | <strong>0.58</strong> | <strong>0.86 <span style="color:blue;">(+33%)</span></strong> | <strong>0.85 <span style="color:blue;">(+34%)</span></strong> | <strong>0.99 <span style="color:red;">(+42%)</span></strong> |


### 5. 실험 해석
- PCA로 차원 축소 이후 높은 정확도를 보인 것은 데이터의 분포에서 원인을 찾을 수 있다.
- 기존 데이터의 주요 특성이나 모든 특성을 사용해서 T-SNE로 시각화한 결과, 불량(0)과 정상(1)의 경계가 모호했지만 PCA 차원 축소 후 데이터의 분포에서는 두 라벨의 차이를 더욱 뚜렷했다.
- 따라서 결론적으로 PCA로 차원 축소를 해서 불량의 패턴을 더욱 명확하게 식별할 수 있던 것으로 해석된다.
- 향후 연구는 딥러닝을 사용하여 불량을 근본 원인을 탐지하는 것에 대한 연구를 수행할 예정이다. 


| ![image](https://github.com/Prcnsi/Deep-learning-based_CMM_Defect-detection/assets/86015194/7a87a33f-094a-430e-b931-3c93f040561a)| ![image](https://github.com/Prcnsi/Deep-learning-based_CMM_Defect-detection/assets/86015194/32dec6cc-f670-4be6-9064-065ef208b914) | ![image](https://github.com/Prcnsi/Deep-learning-based_CMM_Defect-detection/assets/86015194/0a1dbe9a-7515-4056-a91d-e7cbbfbf476b) |
|:-----------------------------------:|:-----------------------------------:|:-----------------------------------:|
| Main feature | All feature | Features that compress the dimensions
