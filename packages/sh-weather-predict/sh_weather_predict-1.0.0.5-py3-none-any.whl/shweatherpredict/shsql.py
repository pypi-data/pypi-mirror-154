###################################
## filename : shsql.py
###################################

import pandas as pd
import pymssql as sql

#데이터베이스 연결 설정
class ShSqlDbSetup:
    # DB Server
    __dbServer = 'localhost'
    # Database Name
    __dbName = 'sunghan'
    # UserName
    __userName = 'sunghan'
    # Password
    __pswd = 'Sunghan!2345'
    
    def __init__(self):
        pass
        
    # DB Connection
    def dbConnect(self):
        return sql.connect(self.__dbServer, self.__userName, self.__pswd, self.__dbName)

    # DB Close
    def dbClose(self, conn):
        if(conn != None):
            conn.close()
    
    # 사이트 코드 체크
    def siteCodeCheck(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 1 SITECODE FROM T_SITE_INFORMATION WHERE OperationYN = 'Y'")
        
        siteCode = ''
        for row in cursor:
            siteCode = row[0]
            
        return siteCode

# 원시데이터 로딩 및 예측결과 데이터 저장    
class ShWeatherData(ShSqlDbSetup):
    def __init__(self):
        pass
        
    # 검색조건에 대한 데이터를 읽어옴
    # 기후 실황정보(온도, 습도, 일사량, 고도, 청명도)를 읽어오는 Query
    def selectWeather(self, conn, prevYear):
        query = 'SELECT CONVERT(CHAR(19), CHARTTIMESTAMP, 120) AS date, REALTEMP as temp, REALREH as reh'
        query += ', ROUND(REALSOLARRADQ,4) AS solarradq, ROUND(REALALTITUDE,4) as altitude, ROUND(REALCLEARNESS,4) as clearness'
        #실 적용시 사용
        query += ' FROM T_1HOUR_WEATHER_REAL_INFO'
        query += ' WHERE CHARTTIMESTAMP BETWEEN DATEADD(YEAR, ' + str(-prevYear) + ', DATEADD(HOUR, -1, GETDATE())) '
        query += ' AND DATEADD(HOUR, -1, GETDATE())'
        query += ' ORDER BY date'

        # 읽어온 데이터를 DataFrame에 저장
        total_df = pd.read_sql(query, conn, parse_dates='date')

        return total_df
    
    # 예측 결과데이터 저장
    def saveWeather(self, conn, siteCode, hhset, current_day, df_predict_climate):
        # 기후정보 1시간 단위 예보 테이블에 데이터 저장
        cursor = conn.cursor()
        for k in range(hhset):
            #timestmp = df_predict_climate['date'][0].strftime('%Y-%m-%d %H:%M:%S')
            #예측 시간 정보
            foreDate = df_predict_climate['date'][0].strftime('%Y%m%d')
            foreHour = df_predict_climate['date'][0].strftime('%H00')
            #시각별 예측 정보
            timestmp = (current_day + pd.DateOffset(hours=k)).strftime('%Y-%m-%d %H:%M:%S')
            predDate = (current_day + pd.DateOffset(hours=k)).strftime('%Y%m%d')
            predHour = (current_day + pd.DateOffset(hours=k)).strftime('%H00')
            temp = df_predict_climate['predtemp'][k]
            reh = df_predict_climate['predreh'][k]
            solar = df_predict_climate['predsolrad'][k]

            #예측정보를 DB에 저장할 SQL 조립
            insertSql = "MERGE INTO T_1HOUR_WEATHER_PREDICT_INFO F"
            insertSql += " USING (SELECT '" + siteCode + "', '" + predDate + "', '" + predHour + "') AS S"
            insertSql += " (SITECODE, PREDICTIONDATE, PREDICTIONHOUR)"
            insertSql += " ON F.SITECODE = S.SITECODE and F.PREDICTIONDATE = S.PREDICTIONDATE and F.PREDICTIONHOUR = S.PREDICTIONHOUR"
            insertSql += " WHEN MATCHED THEN"
            insertSql += " UPDATE SET"
            insertSql += " FORECASTDATE = '" + foreDate + "'"
            insertSql += " ,FORECASTHOUR = '" + foreHour + "'"
            insertSql += " ,PREDICTIONREH = '" + str(reh) + "'"
        #    insertSql += " ,PREDICTIONCLOUDQTY = '" + str(0) + "'"
            insertSql += " ,PREDICTIONTEMP = '" + str(temp) + "'"
        #    insertSql += " ,PREDICTIONENTHALPY = '" + str(0) + "'"
            insertSql += " ,PREDICTIONSOLARRADQ = '" + str(solar) + "'"
        #    insertSql += " , PREDICTIONALTITUDE = '" + str(0) + "'"
        #    insertSql += " , PREDICTIONAZIMUTH = '" + str(0) + "'"
        #    insertSql += " , PREDICTIONCLEARNESS = '" + str(0) + "'"
            insertSql += " ,CHARTTIMESTAMP = '" + str(timestmp) + "'"
            insertSql += " , SAVETIME = getdate()"
            insertSql += " WHEN NOT MATCHED THEN"
            insertSql += " INSERT (PREDICTIONDATE,PREDICTIONHOUR,FORECASTDATE,FORECASTHOUR,PREDICTIONREH,PREDICTIONCLOUDQTY"
            insertSql += " ,PREDICTIONTEMP,PREDICTIONENTHALPY,PREDICTIONSOLARRADQ,CHARTTIMESTAMP"
            insertSql += " ,SITECODE,PREDICTIONALTITUDE,PREDICTIONAZIMUTH,PREDICTIONCLEARNESS)"
            insertSql += " VALUES('" + predDate + "', '" + predHour + "', '" + foreDate + "', '" + foreHour + "', '" + str(reh) + "'"
            insertSql += " , '" + str(0) + "', '" + str(temp) + "', '" + str(0) + "', '" + str(solar) + "', '" + str(timestmp) + "'"
            insertSql += " , '" + siteCode + "'"
            insertSql += " , '" + str(0) + "', '" + str(0) + "', '" + str(0) + "');"

            #예측정보를 예보 테이블에 저장
            cursor.execute(insertSql)

        conn.commit()

    # 실측 조도 추정에 의한 예측하기위한 데이터 로딩
    def transSolarData(self, conn):
        # charttimestamp에는 분단위 데이터가 없어서 -8이 아니라 -9를 해줌
        query = "SELECT CONVERT(CHAR(19), CHARTTIMESTAMP, 120) AS date, REALREH AS reh"
        query += ", TRANSSOLARRADQ AS transsolarradq, REALALTITUDE AS altitude, REALSOLARRADQ AS realsolarradq"
        #실 적용시 사용
        query += ' FROM T_1HOUR_WEATHER_REAL_INFO'
        query += " WHERE CHARTTIMESTAMP BETWEEN DATEADD(DAY, -14, DATEADD(HOUR, -9, GETDATE())) "
        query += " AND DATEADD(HOUR, 0, GETDATE())"
        query += " AND ANNOUNCEHOUR BETWEEN '0800' AND '1800'"
        query += " ORDER BY date"

        # 읽어온 데이터를 DataFrame에 저장
        total_df = pd.read_sql(query, conn, parse_dates='date')

        return total_df

    # 실측조도 추정에 따라 조정된 일사량을 REALSOLARRADQ로 Update
    def updateSolar(self, conn, siteCode, curr_day, solar):
        cursor = conn.cursor()

        #실 적용시 사용
        updateSql = "UPDATE T_1HOUR_WEATHER_REAL_INFO SET REALSOLARRADQ = '" + str(solar) + "'"
        updateSql += " , SAVETIME = getdate()"
        updateSql += " WHERE SITECODE = '" + siteCode + "'"
        updateSql += " AND ANNOUNCEDATE = CONVERT(CHAR(8), CONVERT(DATETIME, '" + str(curr_day) + "', 120), 112)"
        updateSql += " AND ANNOUNCEHOUR = CONVERT(CHAR(2), CONVERT(DATETIME, '" + str(curr_day) + "', 120), 108) + '00'"
        updateSql += " AND ANNOUNCEHOUR BETWEEN '0800' AND '1800'"
        
        cursor.execute(updateSql)
        conn.commit()
