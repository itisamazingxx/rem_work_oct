import os
import yaml
import pandas as pd
from utils.mysqlite import MySqlite

def get_data(file_name):
    try:
        file_path = os.path.join("data", file_name)
        return pd.read_excel(file_path)
    except Exception as e:
        print(f"Error while reading the file '{file_name}'")
        print(e)
        return None

def load_config(file_keyword):
    """加载 YAML 配置文件"""
    if 'centene' in file_keyword.lower():
        config_file = './config/centene_config.yaml'
    elif 'emblem' in file_keyword.lower():
        config_file = './config/emblem_config.yaml'
    elif 'healthfirst' in file_keyword.lower():
        config_file = './config/healthfirst_config.yaml'
    else:
        raise ValueError("The file name does not contain a valid keyword")

    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)
    return config['mappings']

def save_data_sqlite(df):
    my_sqlite = MySqlite()
    df.to_sql('rem_table', my_sqlite.conn, if_exists='append', index=False)

def parse_data(file_name):
    file_keyword = file_name.split(' ')[0].lower()
    config_mappings = load_config(file_keyword)
    df = get_data(file_name)
    df.fillna('<NA>', inplace=True)

    columns = ['Primary_Key', 'Earner_Name', 'Earner_ID', 'Agent_Name', 'Agent_ID', 'Commission_Amount', 'Commission_Period', 'Carrier_Name', 'Enrollment_Type', 'Plan_Name', 'Member_Name', 
               'Member_ID', 'Effective_Date', 'Cycle_Year', 'Earner_Type']
    mapped_df = pd.DataFrame(columns=columns)
    mapped_df['Primary_Key'] = ''
    
    for target_col, source_cols in config_mappings.items():
        if target_col == 'Carrier_Name': 
            if 'centene' in file_keyword: 
                mapped_df['Carrier_Name'] = 'centene'
            elif 'emblem' in file_keyword: 
                mapped_df['Carrier_Name'] = 'emblem'
            elif 'healthfirst' in file_keyword: 
                mapped_df['Carrier_Name'] = 'healthfirst'

        if isinstance(source_cols, list): 
            mapped_df[target_col] = df[source_cols[0]].astype(str) + ' ' + df[source_cols[1]].astype(str)
            mapped_df['Primary_Key'] = mapped_df['Primary_Key'] + ' ' + str(mapped_df[target_col])
        else:
            if source_cols in df.columns:
                mapped_df[target_col] = df[source_cols]
                mapped_df['Primary_Key'] = mapped_df['Primary_Key'] + ' ' + str(mapped_df[target_col])
        
    mapped_df['Primary_Key'] = mapped_df.apply(lambda row: ' '.join(row.dropna().astype(str)), axis=1)
    mapped_df['Earner_Type'] = mapped_df.apply(lambda row: 'FMO' if 'delta care' in str(row['Earner_Name']).lower() else 'Agent', axis=1)

    # 如果Earner_Type = agent/broker -> producer_name = agent_name
    # 如果Earner_Type = FMO -> producer_name = earner_name
    # def normalize_agent_name(name):
    #     parts = str(name).split()  
    #     if len(parts) > 1:
    #         return f"{parts[0]} {parts[-1]}"
    #     return name
    
    if 'Commission_Period' in mapped_df.columns:
        mapped_df['Commission_Period'] = pd.to_datetime(mapped_df['Commission_Period'], errors='coerce').dt.strftime('%Y-%m-%d')
    if 'Effective_Date' in mapped_df.columns:
        mapped_df['Effective_Date'] = pd.to_datetime(mapped_df['Effective_Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    mapped_df.fillna('<NA>', inplace=True)
    mapped_df.drop_duplicates(inplace=True)
    
    return mapped_df

def export_data():
    my_sqlite = MySqlite()
    sql = 'SELECT * FROM rem_table'
    result = my_sqlite.db_query(sql)
    try:
        if result:
            df = pd.DataFrame(result)
            df.to_csv('./database/normalized.csv', index=False)
        return True
    except Exception as e:
        print("Error while exporting data to normalized.csv")
        print(e)
        return False
    
def find_top(params):
    if params == '1':
        sql = """
            SELECT Carrier_Name AS Name, SUM(Commission_Amount) AS total_commission
            FROM rem_table
            GROUP BY Carrier_Name
            ORDER BY total_commission DESC
            LIMIT 10"""
    elif params == '2':
        sql = """
            SELECT Agent_Name AS Name, SUM(Commission_Amount) AS total_commission
            FROM rem_table
            GROUP BY Agent_Name
            ORDER BY total_commission DESC
            LIMIT 10"""
    elif params == '3':
        sql = """
            SELECT Plan_Name AS Name, SUM(Commission_Amount) AS total_commission
            FROM rem_table
            GROUP BY Plan_Name
            ORDER BY total_commission DESC
            LIMIT 10"""
    my_sqlite = MySqlite()
    result = my_sqlite.db_query(sql)
    return result