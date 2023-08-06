import pymysql
import csv
import configparser
from google.cloud import secretmanager
from datetime import datetime
from airflow.models import Variable
import os


def extract_sql(configpath=None,
                hostname=None,
                database=None,
                table=None,
                in_airflow=True):

    parser = configparser.ConfigParser()
    parser.read(configpath)
    username = parser.get('mysql_config', 'username')
    secret_id = parser.get('mysql_config', 'secret_id')
    project_id = parser.get('gcp_config', 'project_id')

    client = secretmanager.SecretManagerServiceClient()
    name = f'projects/{project_id}/secrets/{secret_id}/versions/latest'
    response = client.access_secret_version(name=name)
    password = response.payload.data.decode('UTF-8')

    conn = pymysql.connect(host=hostname,
                           user=username,
                           password=password,
                           db=database,
                           port=3306)

    curr_date = datetime.now().strftime('%Y-%m-%d')
    filename = f'{table}-extract-{curr_date}.csv'
    data_folder = Variable.get('data_folder') if in_airflow else './'
    data_path = f'{data_folder}/{database}/{table}'

    if not os.path.exists(data_path):
        os.makedirs(data_path)

    with open(f'{data_path}/{filename}', 'w') as fp:
        csv_w = csv.writer(fp, delimiter='|')
        begin_time = datetime.now()
        batch = 200000
        checkpoint = 0
        print('starting loop')

        while True:
            loop_time = datetime.now()
            m_query = f"SELECT * FROM {table} ORDER BY id ASC LIMIT {checkpoint}, {batch}"
            m_cursor = conn.cursor()
            m_cursor.execute(m_query)
            results = m_cursor.fetchall()

            if checkpoint == 0:
                field_names = [i[0] for i in m_cursor.description]
                csv_w.writerow(field_names)

            if not results:
                print('breaking')
                break

            csv_w.writerows(results)
            checkpoint += batch
            print(f'checkpoint: {checkpoint}')

            query_time = datetime.now()
            time_taken = query_time - loop_time
            print(f'time taken to query: {time_taken}')

        write_time = datetime.now() - begin_time
        print(f'time taken to write: {write_time}')

    m_cursor.close()
    conn.close()
