from flask import Flask, request,render_template
app = Flask(__name__)
from flask_cors import CORS
CORS(app,resources=r'/*')
from utils import check_ip
import requests
import pymysql
conn = pymysql.connect(
    host='localhost',
    user='root',
    passwd='YRQ21163x!',
    db='LQText16K',
)


import json
from decimal import Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self,o):
        if isinstance(o,Decimal):
            return float(o)
        super(DecimalEncoder,self).default(o)

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
    


from flask_paginate import Pagination


@app.route('/dv',methods=['get'])
def data_vis():
    page = request.args.get('page', 1)
    per_page = request.args.get('per_page', 20)
    # 获取当前页码和每页显示的数量
    page = int(page)
    per_page = int(per_page)
    offset = (page - 1) * per_page
    # 查询 IP 地址和经纬度信息
    cur.execute(f'SELECT * FROM ip_record ORDER BY modify_time DESC')
    data = cur.fetchall()
    # 对查询结果进行分页处理
    pagination = Pagination(page=page, per_page=per_page, total=len(data), css_framework='bootstrap5')
    data = data[offset: offset + per_page]
    data = list(data)
    # 渲染模板并返回页面
    for col in range(len(data)):
        for item in range(len(data[col])):
            if isinstance(data[col][item],Decimal):
                data[col][item] = float(data[col][item])
    return render_template('data_visualization.html', locations=data, pagination=pagination)

    
if __name__ == '__main__':
    cur = conn.cursor()
    app.run()
