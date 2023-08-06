###################################
## filename : shsolarpredict.py
###################################

import pandas as pd
import numpy as np
import datetime
import warnings

warnings.filterwarnings(action='ignore')

# 실측 조도추정 데이터에 의한 일사량 예측
class SolarPredict:

    def __init__(self):
        pass
    
    def solarPred(self, total_df):
        # 일시순 정렬
        total_df = total_df.sort_values(by='date') 
        total_len = len(total_df)

        # 1시간전 realsolarradq인 presolarradq  초기값
        total_df['presolarradq'] = 0 

        # presolarradq = 1시간전 realsolarradq
        for j in range(total_len-1) :
            total_df['presolarradq'].iloc[j+1] = total_df['realsolarradq'].iloc[j] 

        # 8시 데이터 제외
        total_df = total_df[total_df['date'].dt.hour > 8] 

        total_df['const'] = 1 # 상수항 
        total_df['reh2'] = total_df['reh'] * total_df['reh'] # 습도 2제곱
        total_df['reh3'] = total_df['reh'] * total_df['reh'] * total_df['reh'] # 습도 3제곱

        # 회귀분석 독립변수
        X = total_df[['const', 'reh', 'reh2', 'reh3', 'transsolarradq', 'presolarradq', 'altitude']].iloc[0:-1,].to_numpy() 
        # 회귀분석 종속변수
        Y = total_df['realsolarradq'].iloc[0:-1,].to_numpy() 

        # 현재시각 일사량 추정용 독립변수
        current_X = total_df[['reh', 'reh2', 'reh3', 'transsolarradq', 'presolarradq', 'altitude']].iloc[-1,].values 

        # 회귀분석 계수 산출  w = inv((X'X))(X'Y)
        w = np.linalg.inv(X.T @ X) @ X.T @ Y

        # 추정 일사량 산출
        est_solarradq = w[0] + w[1] * current_X[0] + w[2] * current_X[1] + w[3] * current_X[2] + w[4] * current_X[3] + w[5] * current_X[4]  + w[6] * current_X[5]

        if est_solarradq < 0 :
            est_solarradq = 0

        if est_solarradq > 1367 :
            est_solarradq = 1367

        return round(est_solarradq,4)
