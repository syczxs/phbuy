import pymysql


def conn_mysql():
    conn = pymysql.connect(user='root', db='phbuy', password='123456',
                           host='127.0.0.1', port=3306, charset='utf8')
    return conn


def add_commodity(commodity_id, commodity_name, commodity_price, commodity_type, commodity_introduce,
                  commodity_head_pic,commodity_number):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "insert into commodity(commodity_id,commodity_name,commodiy_price,commodity_type,commodity_introduce,commodity_head_pic,commodity_number) " \
          "values ('%s','%s',%s,'%s','%s','%s','%s')" % (
    commodity_id, commodity_name, commodity_price, commodity_type, commodity_introduce,
    commodity_head_pic,commodity_number)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def commodity_all(commodity_id):
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from commodity where commodity_id='%s'" % (commodity_id)
    cursor.execute(sql)
    commodity_all= cursor.fetchall()
    conn.close()
    return commodity_all[0]

def all_commodity_all():
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from commodity "
    cursor.execute(sql)
    commodity_all = cursor.fetchall()
    conn.close()
    return commodity_all

def update_commodity_number(commodity_id,commodity_number):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "update commodity set commodity_number='%s' where commodity_id='%s'"%(commodity_number,commodity_id)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def add_commodity_number(commodity_id,commodity_number):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "update commodity set commodity_number=commodity_number+'%s' where commodity_id='%s'" % (commodity_number, commodity_id)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def set_commodity_discount(commodity_id,discount):
    conn = conn_mysql()
    cursor = conn.cursor()
    sql = "update commodity set commodity_discount=%s where commodity_id='%s'" % (
    discount, commodity_id)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


def add_buy_history(ID,user_name,buy_time,commodity_name,commodity_states):
    user_names=user_name+'_buy_history'
    conn = conn_mysql()
    print(user_names)
    cursor = conn.cursor()
    sql = "insert into %s(ID,user_name,buy_time,commodity,commodity_state) " \
          "values ('%s','%s','%s','%s','%s')" % (user_names,ID,user_name,buy_time,commodity_name,commodity_states)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def select_buy_history(user_name):
    user_names = user_name + '_buy_history'
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from %s where user_name='%s'" % (user_names,user_name)
    cursor.execute(sql)
    commodity_all = cursor.fetchall()
    conn.close()
    return commodity_all


def add_look_history(user_id,user_name,look_time,commodity_name):
    user_names=user_name+'_look_history'
    conn = conn_mysql()
    print(user_names)
    cursor = conn.cursor()
    sql = "insert into %s(ID,user_name,look_time,commodity) " \
          "values ('%s','%s','%s','%s')" % (user_names,user_id,user_name,look_time,commodity_name)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def select_look_history(user_name):
    user_names = user_name + '_look_history'
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from %s where user_name='%s'" % (user_names,user_name)
    cursor.execute(sql)
    commodity_all = cursor.fetchall()
    conn.close()
    return commodity_all

def name_commodity_massage(commodity_name):
    name = '%' + commodity_name + '%'
    conn = conn_mysql()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = "select * from commodity where commodity_name like '%s'" % (name)
    cursor.execute(sql)
    allmassage_user_information = cursor.fetchall()
    conn.close()
    return allmassage_user_information

