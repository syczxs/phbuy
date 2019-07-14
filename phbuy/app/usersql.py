import pymysql


def conn_mysql():
    conn = pymysql.connect(user='root', db='phbuy', password='123456',
                           host='127.0.0.1', port=3306, charset='utf8')
    return conn


def input_user(ID, user_name, pwd, user_pic):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "insert into user (user_id,user_name,pwd,user_pic) values ('%s','%s','%s','%s')" % (ID, user_name, pwd, user_pic)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def create_user_look_record(user_name):
    conn = conn_mysql()
    cursor = conn.cursor()
    user_read_history = user_name + '_look_history'
    sql = "create table %s" \
          "(ID varchar(50) not null," \
          "user_name varchar(50) not null," \
          "look_time varchar(50)," \
          "commodity varchar(50))" % (user_read_history)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def create_user_collection(user_name):
    conn = conn_mysql()
    cursor = conn.cursor()
    user_collection = user_name + '_collection'
    sql = "create table %s" \
          "(ID varchar(50) not null," \
          "user_name varchar(50) not null," \
          "collection_time varchar(50)," \
          "commodity varchar(50))" % (user_collection)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def create_user_buy_history(user_name):
    conn = conn_mysql()
    cursor = conn.cursor()
    user_buy_history = user_name + '_buy_history'
    sql = "create table %s" \
          "(ID varchar(50) not null," \
          "user_name varchar(50) not null," \
          "buy_time varchar(50)," \
          "commodity varchar(50)," \
          "commodity_state varchar(50))" % (user_buy_history)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def check_pwd(name):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select pwd from user where user_name='%s'" % (name)
    cursor.execute(sql)
    pwd_get = cursor.fetchall()
    if pwd_get == ():
        return True
    else:
        return False

def perfecting_personal_date(alipay,pay_number,user_pic,user_address,user_name):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "UPDATE user set alipay='%s',pay_number='%s',user_pic='%s',user_address='%s' where user_name='%s'"%(alipay,pay_number,user_pic,user_address,user_name)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def get_pwd(user_name):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "select pwd from user where user_name='%s'" % (user_name)
    cursor.execute(sql)
    pwd_get = cursor.fetchall()
    conn.close()
    a = pwd_get[0][0]
    return a

def select_all_user_by_username(user_name):
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from user where user_name='%s'" % (user_name)
    cursor.execute(sql)
    user_massage = cursor.fetchall()
    conn.close()
    a = user_massage[0]
    return a


