import boto3
from boto3.s3.transfer import S3Transfer
from boto.s3.connection import S3Connection, Bucket, Key
import logging
import numpy as np
import pandas as pd
import pdb
import psycopg2

logger=logging.getLogger(__name__)

tableName = ''
lakeUser = ''
lakePassword = ''

peProdRedshiftAccessKey = ''
peProdRedshiftSecretAccessKey = ''
bucketName = ''
schemaName = ''
lakeDBName = ''
lakeHost = ''
lakePort = 5439

lakeConnection = psycopg2.connect(dbname=lakeDBName,
                                  host=lakeHost,
                                  port=lakePort,
                                  user=lakeUser,
                                  password=lakePassword)

isFirstRun=False

def remove_delimiters (delimiters, s):
    new_s = str(s)
    for i in delimiters: 
        new_s = new_s.replace(i, ' ')
    return ' '.join(new_s.split())

def push_file(fileName):
    output=pd.read_csv(fileName,parse_dates=['create_time'])
    push_to_s3(output=output,fileName=fileName)
    if isFirstRun:
#         try:
#             drop()
#         except:
#             pass
        create()
    push_to_redshift()
    
def push_to_s3(output=None,fileName=None):
    client = boto3.client('s3', aws_access_key_id=peProdRedshiftAccessKey,
                          aws_secret_access_key=peProdRedshiftSecretAccessKey)
    transfer = S3Transfer(client)
    transfer.upload_file(fileName, 'pe-prod-redshift',
                         'adhoc_upload_files'+'/'+'Pred_SA_{}.csv'.format(output.create_time.max().date().strftime('%Y-%m-%d')))
    logger.info("File copied.")

def push_to_redshift():
    lakeCursor = lakeConnection.cursor()
    logger.info(schemaName+"""."""+tableName)
    logger.warning("Deleting Table")
    lakeCursor.execute("DELETE "+schemaName+"""."""+tableName+";")
    lakeCursor.execute("COMMIT;")
    lakeCursor.execute("END;")
    logger.warning("Reinitializing tables")
    lakeInsertQuery = """
    COPY """ + schemaName + """.""" + tableName + """
    FROM
        's3://pe-prod-redshift/adhoc_upload_files/Pred_SA_'
        credentials 'aws_access_key_id="""+peProdRedshiftAccessKey+""";aws_secret_access_key="""+peProdRedshiftSecretAccessKey+"""'
        IGNOREHEADER 1 delimiter ',' region 'ap-southeast-1'
;
    """
    lakeCursor = lakeConnection.cursor()
    logger.info(lakeInsertQuery)
    lakeCursor.execute(lakeInsertQuery)
    lakeCursor.execute("COMMIT;")
    lakeCursor.execute("END;")
    logger.info("Data copied.")

    
def create():
#                id,order_id,text,create_time,total_length,capitals,caps_vs_length,num_words,num_unique_words,words_vs_unique,Sentiment_Output,Department_Output
#
    lakeCreateTable="""
         CREATE TABLE """ + schemaName + """.""" + tableName + """ 
        (
           "id" varchar(256) NOT NULL,
           "order_id" varchar(256) NOT NULL,
           "text" varchar(65535),
           "create_time" datetime NOT NULL,
           "total_length" numeric(18,0),
           "capitals" numeric(18,8),
           "caps_vs_length" numeric(18,8),
           "num_words" numeric(18,8),
           "num_unique_words" numeric(18,8),
           "words_vs_unique" numeric(18,8),
           "Sentiment_Output" varchar(256) NOT NULL,
           "Department_Output" varchar(256) NOT NULL,
           PRIMARY KEY(order_id,create_time)
        );"""
    
    lakeCursor = lakeConnection.cursor()
    lakeCursor.execute("BEGIN;")
    lakeCursor.execute(lakeCreateTable)
    lakeCursor.execute("COMMIT;")
    logger.warning("Table created.")
    
def drop():
    lakeDropTable="""
         DROP TABLE """ + schemaName + """.""" + tableName + """ ;"""
    lakeCursor = lakeConnection.cursor()
    lakeCursor.execute("BEGIN;")
    lakeCursor.execute(lakeDropTable)
    lakeCursor.execute("COMMIT;")
    lakeCursor.execute("END;")
    logger.warning("Table Dropped.")
    
