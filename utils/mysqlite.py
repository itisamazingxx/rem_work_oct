import os
import sqlite3


# 全局配置
sqldb_file = './database/mysqlite.db'

class MySqlite():
    def __init__(self):
        sqldb_exist = True
        if not os.path.exists(sqldb_file):
            sqldb_exist = False

        self.conn = sqlite3.connect(sqldb_file, check_same_thread=False)
        self.cur = self.conn.cursor()
        
        if not sqldb_exist:
            self.create_table()

    def db_modify(self, sql, *args):
        self.cur.execute(sql, *args)
        self.conn.commit()

    def db_query(self, sql, *args):
        self.cur.execute(sql, *args)
        col_names = [description[0] for description in self.cur.description]
        results = self.cur.fetchall()
        return [dict(zip(col_names, row)) for row in results]

    def db_query_one(self, sql, *args):
        self.cur.execute(sql, *args)
        results = self.cur.fetchone()
        return results

    def db_insert(self, sql, *args):
        self.cur.executemany(sql, *args)
        self.conn.commit()

    def db_close(self):
        self.cur.close()
        self.conn.close()

    def create_table(self):
        sql = '''
            create table if not exists rem_table(
                Primary_Key Text primary key,
                Earner_Name VARCHAR,
                Earner_ID VARCHAR,
                Agent_Name VARCHAR,
                Agent_ID VARCHAR,
                Commission_Amount float,
                Commission_Period VARCHAR,
                Carrier_Name VARCHAR,
                Enrollment_Type VARCHAR,
                Plan_Name VARCHAR,
                Member_Name VARCHAR,
                Member_ID VARCHAR,
                Effective_Date VARCHAR,
                Cycle_Year VARCHAR,
                Earner_Type VARCHAR
            )
        '''
        self.db_modify(sql=sql)


    