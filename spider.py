# encoding: utf-8
#爬虫代码
import requests,json
import pymysql
import time

class JDBC:
    def __init__(self):
        self.update()
        pass
    #连接数据库
    def lian_jie_db(self):
        # 数据库配置信息
        # 连接ip
        DBHOST = 'localhost'
        # username
        DBUSER = 'root'
        # password
        DBPASS = 'lian0911'
        # 存入的数据库表
        DBNAME = 'demopy'
        try:
            conn = pymysql.connect(host=DBHOST, user=DBUSER, password=DBPASS, database=DBNAME)
            cursor = conn.cursor()
            print('连接成功')
        except pymysql.Error as e:
            print("由于某种原因操作数据库出现错误!" + str(e))
            conn.rollback()  # 数据回滚，恢复数据到修改之前
        return conn,cursor

    def close(self,conn,cursor):
        conn.close()
        cursor.close()

    # 国外城市数据
    def foreign_city_data(self):
        # 发送请求:
        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign&callback=&_=%d'%int(time.time()*1000)
        try:
            resp= requests.get(url=url)
        except:
            pass
        data = json.loads(resp.json()['data'])
        # print(data)
        foreignList_data = data['foreignList']
        # 连接数据库
        conn, cursor = self.lian_jie_db()
        # 准备sql
        sql = ''
        for i in foreignList_data:
            if 'children' in i:
                # print(i['name'], end=':')
                nowConfirm = i['nowConfirm']  # 现确诊人数
                for j in i['children']:
                    # {'name': '德克萨斯', 'date': '01.19', 'nameMap': 'Texas', 'isUpdated': True, 'confirmAdd': 0,
                    # 'confirmAddCut': 0, 'confirm': 2143599, 'suspect': 0, 'dead': 32930, 'heal': 1727909}
                    name = j['name']  # 城市
                    date = j['date']  # 更新日期
                    nameMap = j['nameMap']  # 地图名称
                    confirmAdd = j['confirmAdd']  # 确诊增加人数
                    confirmAddCut = j['confirmAddCut']  # 死亡增加人数
                    confirm = j['confirm']  # 确诊人数
                    suspect = j['suspect']  # 疑似人数
                    dead = j['dead']  # 死亡人数
                    heal = j['heal']  # 治愈人数
                    # print(i['name'],name,date,nameMap,confirmAdd,confirmAddCut,confirm,suspect,dead,heal,nowConfirm)
                    sql = 'insert into foreign_city_total VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                    cursor.execute(sql,
                                   args=[i['name'], name, date, nameMap, confirmAdd, confirmAddCut, confirm, suspect,
                                         dead, heal, nowConfirm])
        conn.commit()
        self.close(conn, cursor)
        pass
        pass

    #国内今日累计数据
    def china_total_data(self):
        #发送请求:
        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
        try:
            resp = requests.get(url=url)
        except:
            pass
        data = json.loads(resp.json()['data'])
        lastUpdateTime = data['lastUpdateTime']
        china_Total_data = data['chinaTotal']
        china_Total_data_confirm = china_Total_data['confirm'] #累计确诊
        china_Total_data_heal = china_Total_data['heal'] #累计治愈
        china_Total_data_dead = china_Total_data['dead'] #累计死亡
        china_Total_data_nowConfirm = china_Total_data['nowConfirm']  #现有确诊
        china_Total_data_localConfirm = china_Total_data['localConfirm'] #本土确诊
        china_Total_data_noInfect = china_Total_data['noInfect'] #无症状感染者
        china_Total_data_importedCase = china_Total_data['importedCase'] #境外输入
        # 连接数据库
        conn,cursor = self.lian_jie_db()
        # 准备sql
        sql = 'insert into china_total VALUES(%s,%s,%s,%s,%s,%s,%s)'
        cursor.execute(sql,args =[china_Total_data_confirm,china_Total_data_heal,china_Total_data_dead,
                                  china_Total_data_nowConfirm,china_Total_data_localConfirm,china_Total_data_noInfect,china_Total_data_importedCase] )
        conn.commit()
        self.close(conn,cursor)
        pass


    # 各个省今日&累计数据
    def provinces_total_data(self):
        # 发送请求:
        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
        try:
            resp = requests.get(url=url)
        except:
            pass
        # 其中data中的目标数据,并非是一个字典,而是一个长的像字典的字符串---JSON串  相当与JSON中嵌套了一个JSON
        data = json.loads(resp.json()['data'])
        # 获得国内累计所以数据
        areaTree_Total_data = data['areaTree'][0]['children']
        # 连接数据库
        conn, cursor = self.lian_jie_db()
        # 准备sql
        sql = ''

        for province in areaTree_Total_data:
            #省的名字
            province_name = province['name']

            # 省今日疫情情况
            province_today_total = province['today']
            confirm_today = province_today_total['confirm'] #今日确诊
            confirmCuts = province_today_total['confirmCuts'] #今日确诊死亡人数
            wzz_add = province_today_total['wzz_add'] #今日无症状增加
            sql = 'insert into province_today VALUES(%s,%s,%s,%s)'
            cursor.execute(sql,args=[province_name,confirm_today,confirmCuts,wzz_add])

            #省总计疫情情况
            province_total = province['total']
            nowConfirm = province_total['nowConfirm'] #现确诊
            confirm_total = province_total['confirm'] #累计确诊
            suspect = province_total['suspect'] #疑似人数
            dead = province_total['dead'] #死亡人数
            deadRate = province_total['deadRate'] #死亡率 确诊人数/死亡人数
            heal = province_total['heal'] #治愈人数
            healRate = province_total['healRate'] #治愈率  确诊人数/治愈人数
            wzz = province_total['wzz'] #无症状感染者
            sql = 'insert into province_total VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, args=[province_name, nowConfirm, confirm_total, suspect, dead, deadRate, heal, healRate, wzz])
        conn.commit()
        self.close(conn, cursor)
        pass


    #各个市累计数据
    def cities_total_data(self):
        # 发送请求:
        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5&callback=&_=%d'%int(time.time()*1000)
        try:
            resp = requests.get(url=url)
        except:
            pass
        data = json.loads(resp.json()['data'])
        # 获得国内累计所以数据
        areaTree_Total_data = data['areaTree'][0]['children']
        # 连接数据库
        conn, cursor = self.lian_jie_db()
        # 准备sql
        sql = ''

        for province in areaTree_Total_data:
            # 省的名字
            province_name = province['name'] #省份
            for city in province['children']:
                name = city['name'] #城市
                city_total = city['total']
                nowConfirm = city_total['nowConfirm'] #现确诊
                confirm = city_total['confirm'] #累计确诊
                suspect = city_total['suspect'] #疑似人数
                dead = city_total['dead'] #死亡人数
                deadRate = city_total['deadRate'] # 死亡率 确诊人数/死亡人数
                heal = city_total['heal'] # 治愈人数
                healRate = city_total['healRate'] # 治愈率  确诊人数/治愈人数
                wzz = city_total['wzz'] # 无症状感染者
                sql = 'insert into city_total VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                cursor.execute(sql, args=[province_name,name,nowConfirm,confirm,suspect,dead,deadRate,heal,healRate,wzz])
        conn.commit()
        self.close(conn, cursor)
        pass



    #国外数据
    def foreign_data(self):
        # 发送请求:
        url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign&callback=&_=%d'%int(time.time()*1000)
        try:
            resp = requests.get(url=url)
        except:
            pass
        data = json.loads(resp.json()['data'])
        #print(data)
        foreignList_data = data['foreignList']
        # 连接数据库
        conn, cursor = self.lian_jie_db()
        # 准备sql
        sql = ''
        for i in foreignList_data:
            name = i['name'] #国家名字
            continent = i['continent'] #continent 大陆
            times = i['y'] + '.' + i['date'] #更新时间
            confirmAdd = i['confirmAdd'] #确诊增加人数
            confirmAddCut = i['confirmAddCut'] #死亡增加人数
            confirm = i['confirm'] #确诊人数
            suspect = i['suspect'] #疑似人数
            dead = i['dead'] #死亡人数
            heal = i['heal'] #治愈人数
            nowConfirm = i['nowConfirm'] #现确诊人数
            sql = 'insert into foreign_country_total VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, args=[name,continent,times,confirmAdd,confirmAddCut,confirm,suspect,dead,heal,nowConfirm])
        conn.commit()
        self.close(conn, cursor)
        pass

    # 中国近几月数据
    def china_daily_data(self):
        # https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare
        url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=chinaDayList,chinaDayAddList,nowConfirmStatis,provinceCompare'
        try:
            response = requests.get(url=url)
        except:
            pass
        # print(response.text)
        data = json.loads(response.text)['data']
        data = data['chinaDayAddList']
        # 连接数据库
        conn, cursor = self.lian_jie_db()
        # 准备sql
        sql = ''

        for i in data:
            # {'y': '2020', 'confirm': 60, 'dead': 0, 'heal': 18, 'localConfirmadd': 3, 'deadRate': '0.0',
            # 'date': '11.21', 'suspect': 0, 'importedCase': 14, 'infect': 11, 'localinfectionadd': 0, 'healRate': '30.0'}
            date = i['y'] + '.' + i['date']  # 日期
            confirm = i['confirm']  # 确诊人数
            dead = i['dead']  # 死亡人数
            deadRate = i['deadRate']  # 死亡率
            heal = i['heal']  # 治愈人数
            healRate = i['healRate']  # 治愈率
            localConfirmadd = i['localConfirmadd']  # 当地确诊人数
            localinfectionadd = i['localinfectionadd']  # 当地感染人数增加
            infect = i['infect']  # 感染人数
            suspect = i['suspect']  # 疑似人数
            importedCase = i['importedCase']  # 境外输入
            sql = 'insert into china_daily_data VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            cursor.execute(sql, args=[date, confirm, dead, deadRate, heal, healRate, localConfirmadd, localinfectionadd,
                                      infect, suspect, importedCase])
        conn.commit()
        self.close(conn, cursor)

    def update(self):
        conn,cursor = self.lian_jie_db()
        tables = ['china_total','city_total','foreign_city_total','foreign_country_total','province_today','province_total','china_daily_data']
        for table in tables:
            sql = 'truncate ' + table
            cursor.execute(sql)
        print("已成功初始化数据库表！")

        self.china_total_data()
        self.provinces_total_data()
        self.cities_total_data()
        self.foreign_data()
        self.foreign_city_data()
        self.china_daily_data()
        print("数据爬取成功，已存入数据库")
        conn.commit()
        self.close(conn, cursor)






