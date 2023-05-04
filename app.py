from flask import Flask, request
app = Flask(__name__)
from utils import check_ip
import requests
import pymysql
from flask_cors import CORS
CORS(app,resources=r'/*')

conn = pymysql.connect(
    host='localhost',
    user='root',
    password='YRQ21163x!',
    db='LQText16K',
)

def get_ip(ip_str):
    import re
    result = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", ip_str)
    if result:
        return result[0]
    else:
        print("re cannot find ipNo.2 IPv6")
        string_IPv6="1050:0:0:0:5:600:300c:326b"
        if re.match(r"^(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}$", string_IPv6, re.I):
            print("IPv6 vaild")
        else:
            print("IPv6 invaild")
        result = re.findall(r"(?<![:.\w])(?:[A-F0-9]{1,4}:){7}[A-F0-9]{1,4}(?![:.\w])", string_IPv6, re.I)
        return result[0]
    
'''
# ip_str = request.remote_addr
# ip_str = requests.get('http://myip.ipip.net', timeout=6).text
# ip_str = get_ip(ip_str)
'''
@app.route('/',methods=['POST'])
def index():
    ip_str = request.json.split('=')[-1]
    print(ip_str)
    
    sql_str = f'''
             -- 查询id是否在ip_record表中
        SELECT 
            COUNT(*) AS id_count -- 统计id出现的次数
        FROM 
            ip_record
        WHERE 
            ip = '{ip_str}'; -- 替换为需要查询的id值
    '''
    cur.execute(sql_str)
    # 获取结果
    result = cur.fetchall()
    # 打印结果
    count = None
    for x in result:
        count = x[0]
    if count == 0:
        addr,longitude,latitude = check_ip(ip_str)
        sql_str = f'''
        INSERT INTO ip_record ( ip, addr,count,longitude,latitude)
        VALUES ( '{ip_str}', '{addr}',1,'{longitude}','{latitude}');
        '''
        cur.execute(sql_str)
        conn.commit()
        return 'Fisrt Time!'
    else:
        sql_str = f'''
        UPDATE ip_record SET  modify_time = CURRENT_TIMESTAMP, count = count + 1 WHERE ip = '{ip_str}';
        '''
        cur.execute(sql_str)
        conn.commit()
        return 'UPDATE FINISH!'
    
    
if __name__ == '__main__':
    cur = conn.cursor()
    app.run()
