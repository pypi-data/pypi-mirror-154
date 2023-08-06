import datetime
from os import sep
import time
import asyncio
import uuid
from pprint import pprint

import pandas as pd
from qantio.sdk.public.client.qantio_client import QantioClient
from slugify import slugify

from qantio.sdk.public.models import DataSource, DataPoint

aws_access_key_id = 'AKIAVLHMBZ3C23U3ZPW6'
aws_secret_access_key='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'
azure_account_key = "396Erk6MVjT858PR1DD++8afBKY3ihzNvkLgmuWzsw7g1efVn+afwFbOE+ojwZ/X0fAWny3Zxh/GSwIQfXOB2w=="
file_path = 'J:\\jour\\jour.sql.restaurants.all.by.day.shop.csv'

# logger = logging.getLogger(LOGGER_NAME)

async def main():
    
    print(slugify("qsqsdqsdqsd sdfàç à9Q9 F¨", separator='.'))

    ts_id = uuid.uuid4() 
    
    qt = QantioClient(apikey="f023e2392c024f9a9cea8f0285f9e1ec").authenticate(username="percy_Senger@hauck.ca", password="bdbd46d6-e947-468e-9dcc-13f1dc49442f")
    
    df = pd.read_csv(file_path, index_col=False, header=0, sep=";")
    df_ts = DataSource.pandas_dataframe(
        df                  = df, 
        id                  = ts_id, 
        time_col            = 'date', 
        observations_cols   = ['sum_revenue', 'count_orders'], 
        dimensions_cols     = ['restaurant_name'],
        exogenous_cols      = []).resample(rule='M').rename('ldskfàç _èzeà zjf  z*fdsf')
        
        #.filter(lambda p: (p.Dimensions['dim_restaurant_name']=='THOMASSIN')).rename('jour restaurant thomassin')
    
    print(df_ts.info())
    
    validation = df_ts.validate()
    print(validation)
    exit()

    my_time_serie = qt.WithTimeSerie(ts_id).rename('jour test 45')

    ts_datapoints = []
    city = "Lyon"
    for k in range(0, 2500):

        date = datetime.datetime.today()-datetime.timedelta(days=1500) + datetime.timedelta(days=k)
        dtp = DataPoint(
            timestamp           = date, 
            observation_value   = None, 
            observation_name    = None,
            observations        = {"pressure":1024, "temperature":150},
            exogenous           = {"strike":1.5, 'open':True, 'rabouda':1},
            dimensions          = {"city":city, "depatement":"75", "age":25, "area":"IDF", "country":"FR", "continent":"EU"}
        )
        
        #ts_datapoints.append(dtp)
        my_time_serie.add_measurement(dtp)

    #my_time_serie.add_measurements(datapoints=ts_datapoints)

    print(my_time_serie.info())
    
    validation = my_time_serie.validate()
    print(validation)

    operation_result = qt.ingest(my_time_serie, 50, 4)
    for b in operation_result.BatchOperations:
        pprint(b, indent=4)
        print(10*"---")

    #qt.authenticate(username="percy_Senger@hauck.ca", password="bdbd46d6-e947-468e-9dcc-13f1dc49442f")

    my_ts = DataSource.aws_s3(
        id                  =  uuid.uuid4(),
        bucket              = 'qantio.s3.test', 
        access_key_id       = aws_access_key_id, 
        secret_access_key   = aws_secret_access_key, 
        session_token       = None,
        directory           = "",
        file                = 'jour.sql.restaurants.all.by.day.shop.csv',
        time_col            = 'date', 
        observations_cols   = ['sum_revenue', 'count_orders'], 
        dimensions_cols     = ['restaurant_name'],
        exogenous_cols      = []
    ).filter(lambda p: (p.Dimensions['dim_restaurant_name']=='THOMASSIN')).rename("Restaurant Jour Thomassin")
    #.group(["time", "dim_restaurant_area"], "obs_sum_revenue", ['sum'])
    
    logger.info(my_ts.info())
    logger.info(my_ts.validate())
    
    exit()

    sql_ts = DataSource.sql(
        id                  =  uuid.uuid4(),
        driver              = 'SQL Server',
        server              = 'jour-sql.database.windows.net',
        username            = 'jour_db_user',
        password            = 'yE4bgEXqU3FduUyKPtpG',
        database            = 'Jour_Analytics',
        query               = f"SELECT FORMAT([OrderCreateDate], 'yyyy-MM-dd') as [date], shopname as [restaurant_name], shopcity as [restaurant_city], shoparea as [restaurant_area],ROUND(SUM([Revenue]),0) as [sum_revenue] FROM [Orders] WHERE shopname<>'JOUR.FR' and shopname='THOMASSIN' GROUP BY [OrderCreateDate], shopname, shopcity, shoparea ORDER BY [OrderCreateDate] ASC, shopname ASC",
        time_col            = 'date', 
        observations_cols   = ['sum_revenue'], 
        dimensions_cols     = ['restaurant_name'],
        exogenous_cols      = []
        ).filter(lambda p: (p.timestamp>=datetime.date.today()+datetime.timedelta(days=-15)))

    ftp_ts = DataSource.ftp(
        id                  =  uuid.uuid4(),
        host                = '37.187.150.95', 
        username            = 'root', 
        password            = '00juju', 
        directory           = 'jour.fr/tests',
        file                = 'timeserie5A93E943F32541138D9FEA97A0B9F995.data.feather',
        time_col            = 'date', 
        observations_cols   = ['revenue', 'orders'], 
        dimensions_cols     = [],
        exogenous_cols      = []
        )
    logger.info(ftp_ts.info())
    
    #my_ts = my_ts.from_az_blob_loader(
    #     id                  =  uuid.uuid4(),
    #     account             = "qantiostorageclients", 
    #     account_key         = azure_account_key, 
    #     container           = "exchange",
    #     file                = 'jour.sql.restaurants.all.by.day.shop.csv',
    #     time_col            = 'date', 
    #     observations_cols   = ['sum_revenue'], 
    #     dimensions_cols     = ['restaurant_name'],
    #     exogenous_cols      = [])

    # logger.info(my_ts.info())
    
    # logger.info(my_ts.validate())
 
    # az_ts = qt.from_az_blob(
    #     id                  =  uuid.uuid4(),
    #     account             = "qantiostorageclients", 
    #     account_key         = azure_account_key, 
    #     container           = "exchange",
    #     file                = 'jour.sql.restaurants.all.by.day.shop.csv',
    #     time_col            = 'date', 
    #     observations_cols   = ['sum_revenue'], 
    #     dimensions_cols     = ['restaurant_name'],
    #     exogenous_cols      = []
    #     ).filter(lambda p: (p.Dimensions['dim_restaurant_name']=='THOMASSIN'))
    
    # logger.info(az_ts.info())
    
    # logger.info(az_ts.validate())
    
    exit()

    # logger.exception('dummy exception post auth')
    
    s3_ts = qt.from_aws_s3(
        id                  =  uuid.uuid4(),
        bucket              = 'qantio.s3.test', 
        access_key_id       = aws_access_key_id, 
        secret_access_key   = aws_secret_access_key, 
        session_token       = None,
        directory           = "",
        file                = 'jour.sql.restaurants.all.by.day.shop.csv',
        time_col            = 'date', 
        observations_cols   = ['sum_revenue'], 
        dimensions_cols     = ['restaurant_name', 'restaurant_city', 'qsd'],
        exogenous_cols      = []
        ).filter(lambda p: (p.Dimensions['dim_restaurant_name']=='thomassin'))
    
    # logger.info(s3_ts.info(validate=True)) 
    
    # ftp_ts = qt.from_ftp(
    #     id                  =  uuid.uuid4(),
    #     host                = '37.187.150.95', 
    #     username            = 'root', 
    #     password            = '00juju', 
    #     directory           = 'jour.fr/tests',
    #     file                = 'timeserie5A93E943F32541138D9FEA97A0B9F995.data.feather',
    #     time_col            = 'date', 
    #     observations_cols   = ['revenue', 'orders'], 
    #     dimensions_cols     = [],
    #     exogenous_cols      = []
    #     )
    
    # logger.debug(ftp_ts.info(validate=True))
    # logger.warning(ftp_ts.validate().Summary)

        #.filter(lambda p: (p.Dimensions['dim_restaurant_name']=='thomassin'))
    
    # #and OrderCreateDate>='{datetime.date.today()+datetime.timedelta(days=-2)}'
    # sql_ts = qt.from_sql(
    #     id                  =  uuid.uuid4(),
    #     driver              = 'SQL Server',
    #     server              = 'jour-sql.database.windows.net',
    #     username            = 'jour_db_user',
    #     password            = 'yE4bgEXqU3FduUyKPtpG',
    #     database            = 'Jour_Analytics',
    #     query               = f"SELECT FORMAT([OrderCreateDate], 'yyyy-MM-dd') as [date], shopname as [restaurant_name], shopcity as [restaurant_city], shoparea as [restaurant_area],ROUND(SUM([Revenue]),0) as [sum_revenue] FROM [Orders] WHERE shopname<>'JOUR.FR' and shopname='THOMASSIN' GROUP BY [OrderCreateDate], shopname, shopcity, shoparea ORDER BY [OrderCreateDate] ASC, shopname ASC",
    #     time_col            = 'date', 
    #     observations_cols   = ['sum_revenue'], 
    #     dimensions_cols     = ['restaurant_name'],
    #     exogenous_cols      = []
    #     ).filter(lambda p: (p.timestamp>=datetime.date.today()+datetime.timedelta(days=-15)))
    
    # ts_df = qt.from_dataframe(
    #     df                  = pd.read_csv(file_path, index_col=False, header=0, sep=";"),
    #     id                  = uuid.uuid4(),
    #     time_col            = 'date', 
    #     observations_cols   = ['sum_revenue'], 
    #     dimensions_cols     = ['restaurant_name'],
    #     exogenous_cols      = []
    #     ).filter(lambda p: (p.Dimensions['dim_restaurant_name']=='thomassin'))

    # ts_csv = qt.from_csv(
    #     id                  = uuid.uuid4(), 
    #     file_path           = 'J:\\jour\\jour.sql.restaurants.all.by.day.shop.csv', 
    #     time_col            = 'date', 
    #     observations_cols   = ['sum_revenue'], 
    #     dimensions_cols     = ['restaurant_name']
    #     ).filter(lambda p: (p.Dimensions['dim_restaurant_name']=='thomassin'))
    
    # print(f"az_ts  : {az_ts.info()}") 
    # print(f"s3_ts  : {s3_ts.info()}") 
    #print(f"ftp_ts : {ftp_ts.info()}")
    # print(f"sql_ts : {sql_ts.info()}")
    # print(f"ts_df  : {ts_df.info()}")
    #print(f"ts_csv : {ts_csv.info()}")

    # df = pd.read_csv(file_path, index_col=False, header=0, sep=";")
    # print(df.columns)
    
    # ts:TimeSerie = df.qantio.to_timeserie(
    #     id                  = ts_id, 
    #     time_col            = 'date', 
    #     observations_cols   = ['sum_revenue'], 
    #     dimensions_cols     = ['restaurant_name']
    #     ).filter(lambda p: (p.Dimensions['dim_restaurant_name']=='LA-DEFENSE')
    #     ).set_place(latitude=43.318348, longitude=5.373216)

    #print(ts.info())

    # for k in ts.DataPoints:
    #     print(f"{k.timestamp} : {k.Observations}, {k.Dimensions}, {k.GeographyPoint}")
    
    # operation_result = qt.ingest(ts, 250, 4)
    # for b in operation_result.BatchOperations:
    #     pprint(b, indent=4)
    #     print(10*"---")

    # exit()

    # qt = QantioClient(apikey="f023e2392c024f9a9cea8f0285f9e1ec")
    # qt.authenticate(username="percy_Senger@hauck.ca", password="bdbd46d6-e947-468e-9dcc-13f1dc49442f")
    # ts_id = uuid.uuid4()
    my_time_serie = qt.WithTimeSerie(ts_id)
    print(my_time_serie.dataset_identifier)

    ts_datapoints = []
    city = "pa'/f*sd/7f98sd11f1ù$^ù$^gmhjùù*$34245'(ris"
    for k in range(0, 10):

        date = datetime.datetime.now()-datetime.timedelta(100) + datetime.timedelta(days=k)
        dtp = DataPoint(
            timestamp           = date, 
            observation_value   = None, 
            observation_name    = None,
            observations        = {"pressure":1024, "temperature":150},
            exogenous           = {"strike":1.5, 'open':True, 'rabouda':1},
            dimensions          = {"city":city, "depatement":"75", "age":25, "area":"IDF", "country":"FR", "continent":"EU"}
        )
        
        ts_datapoints.append(dtp)

    other_dtp = DataPoint(
            timestamp           = datetime.datetime.now()-datetime.timedelta(200), 
            observation_value   = None, 
            observation_name    = None,
            observations        = {"pressure":1024, "temperature":256},
            exogenous           = {"strike":1.5, 'open':False, 'rabouda':1},
            dimensions          = {"city":'albertville', "depatement":75, "age":25, "area":"IDF", "country":"FR", "continent":"EU"}
        )

    my_time_serie.add_measurements(datapoints=ts_datapoints)
    my_time_serie.add_measurement(datapoint=other_dtp)

    print(my_time_serie.info())

    my_time_serie = my_time_serie.filter(lambda datapoint: (datapoint.Exogenous['exo_open']==True))
    
    print(my_time_serie.info())
    
    validation = my_time_serie.validate()
    print(validation)
    exit()

    operation_result = qt.ingest(my_time_serie, 300, 4)
    for b in operation_result.BatchOperations:
        pprint(b, indent=4)
        print(10*"---")
    
    # operation_result = await qt.ingest_async(my_time_serie, 500)
    # for b in operation_result.BatchOperations:
    #     pprint(b, indent=4)
    #     print(10*"---")

    # qt.hello()
    # print(qt.add(10, 10))
    # print(qt.whoami())

if __name__ == "__main__":
    
    s = time.perf_counter()
    asyncio.run(main())
    #main()
    #asyncio.get_event_loop().run_until_complete(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")