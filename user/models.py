from django.db import models
import pymysql

# Create your models here.

def mysql_connect():
    con = pymysql.connect(host='localhost',
                          user='root',
                          password='sarah07605!',
                          db='sba',
                          port=3306,
                          charset='utf8',
                          autocommit=True)

    return con


# 코드 합칠때 sql_id와 sql_pwd에서 table이름 바꿔야함
def search(seq_id, seq_pwd):
    con = mysql_connect()
    cursor = con.cursor()
    sql_id = 'select * from member where m_id = %s'
    sql_pwd = 'select * from member where m_password = %s'
    cursor.execute(sql_id, seq_id)
    member_id = cursor.fetchone()
    result_id = member_id[1] if member_id is not None else ''
    cursor.execute(sql_pwd, seq_pwd)
    member_pwd = cursor.fetchone()
    result_pwd = member_pwd[2] if member_pwd is not None else ''
    con.close()
    return result_id,result_pwd

def id_info(seq_name):
    con = mysql_connect()
    cursor = con.cursor()
    sql_name = 'select * from home_member where m_name = %s'
    cursor.execute(sql_name, seq_name)
    member_name = cursor.fetchone()
    result_name = member_name[0] if member_name is not None else ''
    con.close()
    return result_name

def sign_up(member):
    con = mysql_connect()
    cursor = con.cursor()
    sql = 'insert into home_member(m_name, m_id, m_password, m_number, mail) values(%s, %s, %s, %s, %s)'
    # cursor.execute(sql, (member.m_id, member.m_password, member.m_name, member.mail, member.m_number))
    cursor.execute(sql, (member.user_id, member.user_pwd, member.user_name, member.user_email, member.user_number))

    cursor.execute(sql)
    con.commit()
    con.close()
    pass

