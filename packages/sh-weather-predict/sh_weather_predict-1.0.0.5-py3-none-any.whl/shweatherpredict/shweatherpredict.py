###################################
## filename : shweatherpredict.py
###################################

import pandas as pd
import numpy as np
from statsmodels.tsa.api import VAR
import datetime as dt
import warnings

warnings.filterwarnings(action='ignore')

# 훈련데이터 생성 및 기후정보 예측
class WeatherPredict:

    def __init__(self):
        pass
    
    def trainAndPredict(self, total_df, prev_day, current_day, prev_year):
        # 훈련 데이터프레임 설정
        train_df = pd.DataFrame(columns = ['date', 'temp', 'reh', 'solarradq', 'altitude', 'clearness'])

        # 10년치 훈련용 데이터 가져오기
        for year_len in range(prev_year+1):

            # 기준일시 전후 1개월 정의
            start_day = current_day - pd.DateOffset(years=prev_year-year_len) - pd.DateOffset(months=2)
            stop_day = current_day - pd.DateOffset(years=prev_year-year_len) + pd.DateOffset(months=1)

            # 10년동안 1년전 데이터까지는 시작일부터 종료일 1일 전까지 가져오기, 금년 데이터는 시작일부터 현재일 하루전까지 가져오기  
            if year_len < prev_year :
                year_df = total_df[(total_df['date'] < stop_day) & (total_df['date'] >= start_day)]
            else:
                year_df = total_df[(total_df['date'] < current_day) & (total_df['date'] >= start_day)]

            # 10년치 훈련용 데이터 생성  
            train_df = pd.concat([train_df, year_df], axis=0)


        # 온도 습도 훈련용 데이터 설정 (청명도 제외)
        train_temp_df = train_df.drop(['solarradq','clearness'], axis=1)
        train_temp_base = train_temp_df.values

        # 일사량 훈련용 데이터 설정(온도 제외)
        train_solar_df = train_df.drop(['temp', 'altitude'], axis=1)
        train_solar_base = train_solar_df.values

        # 시험 데이터는 현재일부터 prev_day 이전 데이터 가져오기
        test_df = total_df[(total_df['date'] >= prev_day) & (total_df['date'] < current_day)]
        test_y = test_df.values


        # 온도 습도 예측치 저장 array
        pred_temp_value = []

        # 일사량 예측치 저장 array
        pred_solar_value = []


        # 이빨빠진 사항을 감안하여 hhset 재 설정
        #hhset = int(test_y.size/test_y.shape[1])
        hhset = int(test_y.shape[0])

        # 예측(온도, 습도, 일사량)
        for i in range(hhset) :
            # 예측시간 정의
            forecast_time = current_day + pd.DateOffset(hours=i)

            # ---------------------- 온도 습도 예측 --------------------------------------------------------

            # 시계열 피처단위로 변경
            train_temp_df['date'] = pd.to_datetime(train_temp_df['date'])
            train_temp_df = train_temp_df.astype({'temp': 'float', 'reh': 'float', 'altitude': 'float'})

            # date를 index로 지정
            train_temp_df.index = train_temp_df['date']
            train_temp_df.set_index('date', inplace=True)

            # 훈련 데이터
            train_temp = train_temp_df.values

            # VAR 모델 정의 및 결과 저장용 array 정의
            temp_forecasting_model = VAR(train_temp)

            # VAR 모델 학습(72시간 지연)
            results_temp = temp_forecasting_model.fit(maxlags=72)

            # 72시간(3일) 지연 데이터 지정 및 예측
            temp_laaged_values = train_temp_df.values[-72:]
            temp_forecast = pd.DataFrame(results_temp.forecast(y=temp_laaged_values, steps=24), columns=['temp', 'reh', 'altitude'])

            # 예측 습도 조정 계수 곱하기
            temp_forecast.iloc[0,1] = temp_forecast.iloc[0,1] * 1.009  

            # 예측치 중에서 첫번째 예측치 정의 후 (4, 1)을 (1,4)로 모양 변경
            temp_first_forecast = np.array([forecast_time, round(temp_forecast.iloc[0,0], 1), int(temp_forecast.iloc[0,1]), 
                                           round(temp_forecast.iloc[0,2],4)])
            temp_first_forecast = temp_first_forecast.reshape(1,4)

            # 온도 습도 훈련용 기준 데이터에 첫번째 예측치 추가
            train_temp_base = np.append(train_temp_base, temp_first_forecast)

            # 온도 습도 훈련용 기준 데이터 크기 정의 및 모양 변경 
            train_temp_len = train_temp_base.size
            train_temp_base = train_temp_base.reshape(int(train_temp_len/4), 4)

            # 온도 습도 훈련용 기준 데이터를 데이터 프레임으로 변경
            train_temp_df = pd.DataFrame(train_temp_base, columns=['date', 'temp', 'reh', 'altitude'])

            # 온도 습도 1시간 예측치를 추가
            pred_temp_value = np.append(pred_temp_value, temp_forecast.iloc[0,:].values)
            #print(temp_forecast.iloc[0,0:1].values,temp_forecast.iloc[0,1:2].values,temp_forecast.iloc[0,2:3].values)
            #print(temp_forecast.iloc[0,:].values)

            # ---------------------- 일사량 예측 --------------------------------------------------------

            # 시계열 피처단위로 변경
            train_solar_df['date'] = pd.to_datetime(train_solar_df['date'])
            train_solar_df = train_solar_df.astype({'reh': 'float', 'solarradq': 'float', 'clearness': 'float'})

            # day를 index로 지정
            train_solar_df.index = train_solar_df['date']
            train_solar_df.set_index('date', inplace=True)

            # 훈련 데이터
            train_solar = train_solar_df.values

            # VAR 모델 정의 및 결과 저장용 array 정의
            solar_forecasting_model = VAR(train_solar)

            # VAR 모델 학습
            results_solar = solar_forecasting_model.fit(maxlags=72)

            # 72시간(3일) 지연 데이터 지정 및 예측
            solar_laaged_values = train_solar_df.values[-72:]
            solar_forecast = pd.DataFrame(results_solar.forecast(y=solar_laaged_values, steps=24), columns=['reh', 'solarradq', 'clearness'])

            # 예측 습도 조정 계수 곱하기
            solar_forecast.iloc[0,1] = solar_forecast.iloc[0,1] * 1.009  

            # 예측치 중에서 첫번째 예측치 정의 후 (4, 1)을 (1,4)로 모양 변경
            solar_first_forecast = np.array([forecast_time, int(solar_forecast.iloc[0,0]), round(solar_forecast.iloc[0,1],2), 
                                                             round(solar_forecast.iloc[0,2],4)])
            solar_first_forecast = solar_first_forecast.reshape(1,4)

            # 일사량 훈련용 기준 데이터에 첫번째 예측치 추가
            train_solar_base = np.append(train_solar_base, solar_first_forecast)

            # 일사량 훈련용 기준 데이터 크기 정의 및 모양 변경 
            train_solar_len = train_solar_base.size
            train_solar_base = train_solar_base.reshape(int(train_solar_len/4), 4)

            # 일사량 훈련용 기준 데이터를 데이터 프레임으로 변경
            train_solar_df = pd.DataFrame(train_solar_base, columns=['date', 'reh', 'solarradq', 'clearness'])
            train_solar_df['reh'] = train_temp_df['reh'] # 이전 예측 습도로 대체

            # 일사량 1시간 예측치를 추가
            pred_solar_value = np.append(pred_solar_value, solar_forecast.iloc[0,:].values)
            #print(solar_forecast.iloc[0,0:1].values,solar_forecast.iloc[0,1:2].values,solar_forecast.iloc[0,2:3].values)
            #print(solar_forecast.iloc[0,:].values)
    
    
        # 예측 결과 저장용 데이터프레임 설정
        df_predict_climate = pd.DataFrame(columns = ['date', 'realtemp', 'predtemp', 'realreh', 'predreh', 'realsolrad', 'predsolrad'])
        cnt = 0
        
        # 예측 결과 저장 및 출력
        for j in range(hhset):

            # 예측시간 정의
            predict_time = current_day + pd.DateOffset(hours=j)
            predict_hour = pd.to_datetime(predict_time).hour

            # 습도가 99보다 클 경우 99
            if pred_temp_value[1+3*j] > 99 :
                pred_temp_value[1+3*j] = 99

            # 습도가 음수일 경우 0
            if pred_temp_value[1+3*j] < 0 :
                pred_temp_value[1+3*j] = 0        

            # 8시 이전시간 18시 이후 시간 또는 예측 일사량이 음수이면 일사량 = 0
            if (predict_hour < 8) | (predict_hour > 18) | (pred_solar_value[1+3*j] < 0) :
                test_y[j][3] = 0
                pred_solar_value[1+3*j] = 0

            # 실측와 예측치를 데이터프레임에 저장
            df_predict_climate.loc[cnt] = [predict_time, 
                                           test_y[j][1], round(pred_temp_value[0+3*j],1), 
                                           int(test_y[j][2]), int(pred_temp_value[1+3*j]),
                                           round(test_y[j][3], 2), round(pred_solar_value[1+3*j], 2)]
            cnt = cnt + 1

##############
# 배포시 삭제
##############
            # 실측치 예측치 출력
#            print(predict_time,
#                  "실측기온: {:.1f}, 예측기온: {:.1f}, 실측습도: {:3d}, 예측습도: {:3d}, 실측일사량: {:.2f}, 예측일사량: {:.2f}". 
#                  format(test_y[j][1], round(pred_temp_value[0+3*j],1), 
#                         int(test_y[j][2]), int(pred_temp_value[1+3*j]),
#                         round(test_y[j][3], 2), round(pred_solar_value[1+3*j], 2))) 
#
#        savetime = current_day.strftime('%Y%m%d%H')
#        path = "./climate-predict-" + savetime + ".csv"
#        df_predict_climate.to_csv(path, index=False)
######################### 여기까지 삭제

        return df_predict_climate, hhset
