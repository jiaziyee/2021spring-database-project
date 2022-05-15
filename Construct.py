import psycopg2

conn = psycopg2.connect(database="Project", user="postgres", password="010504", host="127.0.0.1", port="5432")

cur = conn.cursor()
sql = '''DROP TABLE IF EXISTS Application,my_User,Department;'''
cur.execute(sql)
print("Initialized")

cur = conn.cursor()
sql = '''CREATE TABLE Department(
                 dep_id CHAR(2) PRIMARY KEY NOT NULL UNIQUE,
                 dep_name VARCHAR(5) NOT NULL
                 );'''
cur.execute(sql)


cur = conn.cursor()
sql = '''CREATE TABLE my_User(
                 user_id CHAR(4) PRIMARY KEY NOT NULL UNIQUE,
                 user_dep_id CHAR(2) NOT NULL REFERENCES Department(dep_id) ON UPDATE CASCADE,
                 user_password VARCHAR(4) NOT NULL
                 );'''
cur.execute(sql)


cur = conn.cursor()
sql = '''CREATE TABLE Application(
                 app_id VARCHAR(4) PRIMARY KEY NOT NULL UNIQUE,
                 state VARCHAR(10) NOT NULL CHECK(state in ('pending','passed','refused','cancelled')),
                 app_creator_id CHAR(4) REFERENCES my_User(user_id) ON UPDATE CASCADE NOT NULL,
                 out_time TIMESTAMP NOT NULL,
                 in_time TIMESTAMP NOT NULL,
                 comment VARCHAR(100),
                 app_commenter_id CHAR(4) REFERENCES my_User(user_id)
                 );'''
cur.execute(sql)


conn.commit()


cur = conn.cursor()
sql = '''INSERT INTO Department(dep_id,dep_name)
            VALUES ('01','工业工程系'),
                   ('02','自动化系');
                   '''
cur.execute(sql)

cur = conn.cursor()
sql = '''INSERT INTO my_user(user_id,user_dep_id,user_password)
            VALUES ('0001','01','0000'),
                   ('0002','02','0000'),
                   ('1001','01','0000'),
                   ('1002','01','0000'),
                   ('1003','02','0000');
                   '''
cur.execute(sql)

cur = conn.cursor()
sql = '''INSERT INTO Application(app_id,state,app_creator_id,out_time,in_time,app_commenter_id)
            VALUES ('1','passed','1001','2021-06-25 12:00:00','2021-06-25 17:00:00','0001'),
                   ('2','passed','1001','2021-06-26 13:00:00','2021-06-26 19:00:00','0001'),
                   ('3','passed','1001','2021-06-27 13:00:00','2021-06-27 14:00:00','0001');
                   '''
cur.execute(sql)

cur = conn.cursor()
sql = '''INSERT INTO Application(app_id,state,app_creator_id,out_time,in_time)
            VALUES ('4','pending','1002','2021-06-25 14:00:00','2021-06-26 19:00:00'),
                   ('5','pending','1003','2021-06-21 12:00:00','2021-06-21 14:00:00'),
                   ('6', 'pending', '1003', '2021-06-02 12:00:00', '2021-06-03 12:00:00');
                   '''
cur.execute(sql)


conn.commit()
conn.close()

