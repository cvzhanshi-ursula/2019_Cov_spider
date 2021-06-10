# encoding: utf-8
from flask import Flask,render_template
from pyecharts.charts import Map,Line,Bar,Pie,Bar3D,Page
from pyecharts import  options as opts
import requests,json
import pymysql
from pyecharts.globals import ThemeType
from spider import JDBC
app = Flask(__name__)

#连接数据库
def lian_jie_db():
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

#关闭数据库连接
def close(conn,cursor):
    conn.close()
    cursor.close()

#翻译
def traslate(data):#将世界各国的中文名转化为英文
    countries = {
        "Somalia": "索马里",
        "Liechtenstein": "列支敦士登",
        "Morocco": "摩洛哥",
        "W. Sahara": "西撒哈拉",
        "Serbia": "塞尔维亚",
        "Afghanistan": "阿富汗",
        "Angola": "安哥拉",
        "Albania": "阿尔巴尼亚",
        "Andorra": "安道尔共和国",
        "United Arab Emirates": "阿拉伯联合酋长国",
        "Argentina": "阿根廷",
        "Armenia": "亚美尼亚",
        "Australia": "澳大利亚",
        "Austria": "奥地利",
        "Azerbaijan": "阿塞拜疆",
        "Burundi": "布隆迪",
        "Belgium": "比利时",
        "Benin": "贝宁",
        "Burkina Faso": "布基纳法索",
        "Bangladesh": "孟加拉国",
        "Bulgaria": "保加利亚",
        "Bahrain": "巴林",
        "Bahamas": "巴哈马",
        "Bosnia and Herz.": "波斯尼亚和黑塞哥维那",
        "Belarus": "白俄罗斯",
        "Belize": "伯利兹",
        "Bermuda": "百慕大",
        "Bolivia": "玻利维亚",
        "Brazil": "巴西",
        "Barbados": "巴巴多斯",
        "Brunei": "文莱",
        "Bhutan": "不丹",
        "Botswana": "博茨瓦纳",
        "Central African Rep.": "中非",
        "Canada": "加拿大",
        "Switzerland": "瑞士",
        "Chile": "智利",
        "China": "中国",
        "Côte d'Ivoire": "科特迪瓦",
        "Cameroon": "喀麦隆",
        "Dem. Rep. Congo": "刚果民主共和国",
        "Congo": "刚果",
        "Colombia": "哥伦比亚",
        "Cape Verde": "佛得角",
        "Costa Rica": "哥斯达黎加",
        "Cuba": "古巴",
        "N. Cyprus": "北塞浦路斯",
        "Cyprus": "塞浦路斯",
        "Czech Rep.": "捷克",
        "Germany": "德国",
        "Djibouti": "吉布提",
        "Denmark": "丹麦",
        "Dominican Rep.": "多米尼加",
        "Algeria": "阿尔及利亚",
        "Ecuador": "厄瓜多尔",
        "Egypt": "埃及",
        "Eritrea": "厄立特里亚",
        "Spain": "西班牙",
        "Estonia": "爱沙尼亚",
        "Ethiopia": "埃塞俄比亚",
        "Finland": "芬兰",
        "Fiji": "斐济",
        "France": "法国",
        "Gabon": "加蓬",
        "United Kingdom": "英国",
        "Georgia": "格鲁吉亚",
        "Ghana": "加纳",
        "Guinea": "几内亚",
        "Gambia": "冈比亚",
        "Guinea-Bissau": "几内亚比绍",
        "Eq. Guinea": "赤道几内亚",
        "Greece": "希腊",
        "Grenada": "格林纳达",
        "Greenland": "格陵兰",
        "Guatemala": "危地马拉",
        "Guam": "关岛",
        "Guyana": "圭亚那",
        "Honduras": "洪都拉斯",
        "Croatia": "克罗地亚",
        "Haiti": "海地",
        "Hungary": "匈牙利",
        "Indonesia": "印度尼西亚",
        "India": "印度",
        "Br. Indian Ocean Ter.": "英属印度洋领土",
        "Ireland": "爱尔兰",
        "Iran": "伊朗",
        "Iraq": "伊拉克",
        "Iceland": "冰岛",
        "Israel": "以色列",
        "Italy": "意大利",
        "Jamaica": "牙买加",
        "Jordan": "约旦",
        "Japan": "日本本土",
        "Siachen Glacier": "锡亚琴冰川",
        "Kazakhstan": "哈萨克斯坦",
        "Kenya": "肯尼亚",
        "Kyrgyzstan": "吉尔吉斯坦",
        "Cambodia": "柬埔寨",
        "Korea": "韩国",
        "Kuwait": "科威特",
        "Lao PDR": "老挝",
        "Lebanon": "黎巴嫩",
        "Liberia": "利比里亚",
        "Libya": "利比亚",
        "Sri Lanka": "斯里兰卡",
        "Lesotho": "莱索托",
        "Lithuania": "立陶宛",
        "Luxembourg": "卢森堡",
        "Latvia": "拉脱维亚",
        "Moldova": "摩尔多瓦",
        "Madagascar": "马达加斯加",
        "Mexico": "墨西哥",
        "Macedonia": "马其顿",
        "Mali": "马里",
        "Malta": "马耳他",
        "Myanmar": "缅甸",
        "Montenegro": "黑山",
        "Mongolia": "蒙古",
        "Mozambique": "莫桑比克",
        "Mauritania": "毛里塔尼亚",
        "Mauritius": "毛里求斯",
        "Malawi": "马拉维",
        "Malaysia": "马来西亚",
        "Namibia": "纳米比亚",
        "New Caledonia": "新喀里多尼亚",
        "Niger": "尼日尔",
        "Nigeria": "尼日利亚",
        "Nicaragua": "尼加拉瓜",
        "Netherlands": "荷兰",
        "Norway": "挪威",
        "Nepal": "尼泊尔",
        "New Zealand": "新西兰",
        "Oman": "阿曼",
        "Pakistan": "巴基斯坦",
        "Panama": "巴拿马",
        "Peru": "秘鲁",
        "Philippines": "菲律宾",
        "Papua New Guinea": "巴布亚新几内亚",
        "Poland": "波兰",
        "Puerto Rico": "波多黎各",
        "Dem. Rep. Korea": "朝鲜",
        "Portugal": "葡萄牙",
        "Paraguay": "巴拉圭",
        "Palestine": "巴勒斯坦",
        "Qatar": "卡塔尔",
        "Romania": "罗马尼亚",
        "Russia": "俄罗斯",
        "Rwanda": "卢旺达",
        "Saudi Arabia": "沙特阿拉伯",
        "Sudan": "苏丹",
        "S. Sudan": "南苏丹",
        "Senegal": "塞内加尔",
        "Singapore": "新加坡",
        "Solomon Is.": "所罗门群岛",
        "Sierra Leone": "塞拉利昂",
        "El Salvador": "萨尔瓦多",
        "Suriname": "苏里南",
        "Slovakia": "斯洛伐克",
        "Slovenia": "斯洛文尼亚",
        "Sweden": "瑞典",
        "Swaziland": "斯威士兰",
        "Seychelles": "塞舌尔",
        "Syria": "叙利亚",
        "Chad": "乍得",
        "Togo": "多哥",
        "Thailand": "泰国",
        "Tajikistan": "塔吉克斯坦",
        "Turkmenistan": "土库曼斯坦",
        "Timor-Leste": "东帝汶",
        "Tonga": "汤加",
        "Trinidad and Tobago": "特立尼达和多巴哥",
        "Tunisia": "突尼斯",
        "Turkey": "土耳其",
        "Tanzania": "坦桑尼亚",
        "Uganda": "乌干达",
        "Ukraine": "乌克兰",
        "Uruguay": "乌拉圭",
        "United States": "美国",
        "Uzbekistan": "乌兹别克斯坦",
        "Venezuela": "委内瑞拉",
        "Vietnam": "越南",
        "Vanuatu": "瓦努阿图",
        "Yemen": "也门",
        "South Africa": "南非",
        "Zambia": "赞比亚",
        "Zimbabwe": "津巴布韦",
        "Aland": "奥兰群岛",
        "American Samoa": "美属萨摩亚",
        "Fr. S. Antarctic Lands": "南极洲",
        "Antigua and Barb.": "安提瓜和巴布达",
        "Comoros": "科摩罗",
        "Curaçao": "库拉索岛",
        "Cayman Is.": "开曼群岛",
        "Dominica": "多米尼加",
        "Falkland Is.": "马尔维纳斯群岛（福克兰）",
        "Faeroe Is.": "法罗群岛",
        "Micronesia": "密克罗尼西亚",
        "Heard I. and McDonald Is.": "赫德岛和麦克唐纳群岛",
        "Isle of Man": "曼岛",
        "Jersey": "泽西岛",
        "Kiribati": "基里巴斯",
        "Saint Lucia": "圣卢西亚",
        "N. Mariana Is.": "北马里亚纳群岛",
        "Montserrat": "蒙特塞拉特",
        "Niue": "纽埃",
        "Palau": "帕劳",
        "Fr. Polynesia": "法属波利尼西亚",
        "S. Geo. and S. Sandw. Is.": "南乔治亚岛和南桑威奇群岛",
        "Saint Helena": "圣赫勒拿",
        "St. Pierre and Miquelon": "圣皮埃尔和密克隆群岛",
        "São Tomé and Principe": "圣多美和普林西比",
        "Turks and Caicos Is.": "特克斯和凯科斯群岛",
        "St. Vin. and Gren.": "圣文森特和格林纳丁斯",
        "U.S. Virgin Is.": "美属维尔京群岛",
        "Samoa": "萨摩亚"
    }
    c2e ={}
    for k,v in countries.items():
        c2e[v]=k
    list_data = []
    for i in data:
        list_data.append(list(i))
    #print(list_data)
    for i in range(0,len(list_data)):
        if list_data[i][0] in c2e.keys():
            list_data[i][0] = c2e[list_data[i][0]]
            pass
    return list_data


#中国地图
def china_total_data(): #中国地图,中国总确诊数量
    conn,cursor = lian_jie_db()
    #准备sql ---查询国内到今天为止的累计情况
    sql = 'select 累计确诊,累计治愈,累计死亡,现有确诊,本土确诊,无症状感染者,境外输入 from china_total'
    cursor.execute(sql)
    # print(cursor.fetchall()[0])
    china_Total_data_confirm,china_Total_data_heal,china_Total_data_dead,\
    china_Total_data_nowConfirm,china_Total_data_localConfirm,china_Total_data_noInfect,china_Total_data_importedCase = cursor.fetchall()[0]
    # 准备sql ---查询各个省所有的累计情况
    sql = 'select 省份,累计确诊 from province_total'
    data = cursor.execute(sql)
    #print(cursor.fetchall())
    data = cursor.fetchall()
    close(conn,cursor)
    # 使用pyecharts可视化数据
    c = (
        Map() # 数据格式: [['省名',数据],['省名',数据],['省名',数据]]
            .add("各个省累计确诊数量", data, "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="全国疫情监控",pos_left="5%",pos_top="5%",
                                      subtitle="截止至今:累计确诊:%s,累计治愈:%s,累计死亡:%s,\n现有确诊:%s,本土确诊:%s,无症状感染者:%s"%(
                                          china_Total_data_confirm,china_Total_data_heal,china_Total_data_dead,
                                          china_Total_data_nowConfirm,china_Total_data_localConfirm,china_Total_data_noInfect)),
            visualmap_opts=opts.VisualMapOpts(max_=1500),
        )
        .render('templates/map_china.html')
    )
    return c
    pass

#各省柱状图
def provinces_total_data():#柱状图,各个省累计数据
    conn,cursor = lian_jie_db()
    sql = 'select 省份,累计确诊,治愈人数,死亡人数 from province_total'
    cursor.execute(sql)
    data = cursor.fetchall()
    close(conn,cursor)
    c = ( #bar = Bar({'theme':ThemeType.LIGHT})
        Bar()
            .add_xaxis([i[0] for i in data if i[0] != '湖北'])
            .add_yaxis("累计确诊", [i[1] for i in data if i[0] != '湖北'])
            .add_yaxis("治愈人数", [i[2] for i in data if i[0] != '湖北'])
            .add_yaxis("死亡人数", [i[3] for i in data if i[0] != '湖北'])
            .set_global_opts(title_opts=opts.TitleOpts(title="各省累计情况(除湖北以外)",pos_left="5%",pos_top="0%"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0,interval=0)),
                             datazoom_opts=opts.DataZoomOpts(range_start=10, range_end=100),)
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                    opts.MarkPointItem(type_="average", name="平均值"),
                ]
            ),
        )
        .render('templates/provinces_total.html')
    )
    return c
    pass


# 各省治愈率和死亡率对比 柱状图
def provinces_rate_data():
    conn, cursor = lian_jie_db()
    sql = 'select 省份,治愈率,死亡率 from province_total'
    cursor.execute(sql)
    data = cursor.fetchall()
    close(conn, cursor)
    c = (  # bar = Bar({'theme':ThemeType.LIGHT})
        Bar(init_opts=opts.InitOpts(width='1300px',theme=ThemeType.LIGHT))
            .add_xaxis([i[0] for i in data])
            .add_yaxis("治愈率%", [i[1] for i in data])
            .add_yaxis("死亡率%", [i[2] for i in data])
            .set_global_opts(title_opts=opts.TitleOpts(title="各省治愈情况", pos_left="5%", pos_top="0%"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0,interval=0)),
                             datazoom_opts=opts.DataZoomOpts(range_start=10, range_end=100),)
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                    opts.MarkPointItem(type_="average", name="平均值"),
                ]
            ),
        )
            .render('templates/dead_heal.html')
    )
    return c
    pass


#中国现确诊 饼状图
def provinces_nowConfirm_data():
    conn, cursor = lian_jie_db()
    sql = 'select 省份,现确诊 from province_total'
    cursor.execute(sql)
    data = cursor.fetchall()
    close(conn, cursor)
    c = (
        Pie()
            .add(
            "",
            data,
            radius=["20%", "50%"],
            center=["50%", "60%"],
            # rosetype="area",
            #label_opts=opts.LabelOpts(is_show=False),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="各省现确诊人数",pos_left="5%",pos_top="0%"),
                             # legend_opts=opts.LegendOpts(is_show=False),
                             legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="5%"),
                             )
            .render('templates/provinces_nowConfirm.html')
    )
    return c
    pass


#中国近期分析 折线图
def china_daily_data():
    conn, cursor = lian_jie_db()
    sql = 'select 日期,确诊人数,治愈人数,境外人数 from china_daily_data'
    cursor.execute(sql)
    data = cursor.fetchall()
    close(conn, cursor)
    #data = [i for i in data if i[0:5] == '2021']


    data = [i for i in data if i[0][0:4] == '2021']
    print(data)
    c = (
        Line()
            .add_xaxis([i[0][5:] for i in data])
            .add_yaxis("确诊人数", [i[1] for i in data], is_smooth=True)
            .add_yaxis("治愈人数", [i[2] for i in data], is_smooth=True)
            .add_yaxis("境外人数", [i[3] for i in data], is_smooth=True)
            .set_global_opts(title_opts=opts.TitleOpts(title="中国近日数据",pos_left="6%"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0, interval=0)),
                             datazoom_opts=opts.DataZoomOpts(range_start=10, range_end=100),)  # 坐标轴进行缩放
            .render("templates/china_daily.html")
    )
    return c
    pass



#省份今日
def provinces_today_data():#柱状图
    conn, cursor = lian_jie_db()
    sql = 'select 省份,今日确诊 from province_today where 今日确诊 > 0'
    cursor.execute(sql)
    data = cursor.fetchall()
    close(conn, cursor)
    c = (
        Bar(init_opts=opts.InitOpts())
            .add_xaxis([i[0] for i in data])
            .add_yaxis("今日确诊", [i[1] for i in data])
            .set_global_opts(title_opts=opts.TitleOpts(title="各省今日累计情况",pos_left="7%",pos_top="0%",
                                                       subtitle="未显示即没有新增"),
                             xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=0)),
                             datazoom_opts=[opts.DataZoomOpts()],)
            .set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            markpoint_opts=opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
                    opts.MarkPointItem(type_="average", name="平均值"),
                ]
            ),
        )
        .render('templates/provinces_today.html')
    )
    pass
# 一个省的现确诊人数
def province_one_data_now(province_name):
    conn, cursor = lian_jie_db()
    sql = 'select 城市,现确诊 from city_total where 省份 = "%s"'%(province_name)
    cursor.execute(sql)
    list_data = cursor.fetchall()
    close(conn, cursor)
    data = []
    for i in range(0, len(list_data)):
        data.append((list_data[i][0] + '市', list_data[i][1]))
    c = (
        Map()
            .add("现在确诊", data, province_name)
            .set_global_opts(
            title_opts=opts.TitleOpts(title=province_name+"现在疫情情况"), visualmap_opts=opts.VisualMapOpts()
        )
            .render("city_map.html")
    )
    pass
    return c

# 一个省的累计确诊人数
def province_one_data(province_name):
    conn, cursor = lian_jie_db()
    sql = 'select 城市,累计确诊 from city_total where 省份 = "%s"'%(province_name)
    cursor.execute(sql)
    list_data = cursor.fetchall()
    close(conn, cursor)
    data = []
    for i in range(0, len(list_data)):
        data.append((list_data[i][0] + '市', list_data[i][1]))
    print(data)
    c = (
        Map()
            .add("累计确诊", data, province_name)
            .set_global_opts(
            title_opts=opts.TitleOpts(title=province_name+"累计确诊情况"), visualmap_opts=opts.VisualMapOpts()
        )
            .render("city_map.html")
    )
    pass
    return c

#世界地图
def foreign_country_total():
    conn, cursor = lian_jie_db()
    sql = "select 国家,现确诊人数 from foreign_country_total"
    cursor.execute(sql)
    list_data = cursor.fetchall()
    close(conn, cursor)
    data = traslate(list_data)
    print(data)
    c = (
        Map()
            .add("现确诊人数", data, "world")
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(
            title_opts=opts.TitleOpts(title="各国现确诊人数",pos_left="5%",pos_top="5%"),
            visualmap_opts=opts.VisualMapOpts(max_=10000),
        )
        .render('templates/map_world.html')
    )
    return c
    pass

#美国地图
def Mei_Guo_total():
    conn, cursor = lian_jie_db()
    sql = "select 地图名称,确诊人数 from foreign_city_total where 国家 ='美国'"
    cursor.execute(sql)
    data = cursor.fetchall()
    # print(data)
    close(conn, cursor)
    c = (
        Map()
            .add("确诊人数", data, "美国")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="美国疫情情况"),
            visualmap_opts=opts.VisualMapOpts(max_=2000000,is_piecewise=True),
        )
        #.render('templates/美国地图.html')
    )
    return c
    pass
#日本地图
def Japan_total():
    conn, cursor = lian_jie_db()
    sql = "select 地图名称,确诊人数 from foreign_city_total where 国家 ='日本本土'"
    cursor.execute(sql)
    data = cursor.fetchall()
    close(conn, cursor)
    c = (
        Map()
            .add("确诊人数", data, "日本")
            .set_global_opts(
            title_opts=opts.TitleOpts(title="日本疫情情况"),
            visualmap_opts=opts.VisualMapOpts(max_=50000,is_piecewise=True),
        )
        #.render('templates/日本地图.html')
    )
    return c
    pass

def first_():
    conn, cursor = lian_jie_db()
    sql = "select 累计确诊,累计治愈,累计死亡,现有确诊 from china_total"
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    close(conn, cursor)
    data = data[0]
    print(data)
    return data


@app.route('/')
def index():
    return render_template('index.html')
    pass
@app.route('/first')
def first():
    data = first_()
    return render_template('first.html',data = data)
@app.route('/map_china')
def map_china():
    china_total_data()  # 中国地图
    return render_template('map_china.html')
    pass

@app.route('/provinces_total')
def provinces_total():
    provinces_total_data()  # 柱状图
    return render_template('provinces_total.html')
@app.route('/provinces_today')
def provinces_today():
    provinces_today_data()  # 柱状图
    return render_template('provinces_today.html')


@app.route('/provinces_nowConfirm')
def provinces_nowConfirm():
    provinces_nowConfirm_data()  # 饼状图
    return render_template('provinces_nowConfirm.html')

@app.route('/map_world')
def map_world():
    foreign_country_total()  # 世界地图
    return render_template('map_world.html')
@app.route('/tables')
def tables():
    return render_template('tables.html')

@app.route('/tables2',methods=("GET","POST"))
def tables2():
    return render_template('tables2.html')

@app.route('/tables3',methods=("GET","POST"))
def tables3():
    return render_template('tables3.html')

@app.route('/sumdata')
def sumdata():
    return render_template('sumdata.html')



@app.route('/china_daily')
def china_daily():
    china_daily_data()  # 中国今年柱状图
    return render_template('china_daily.html')

@app.route('/dead_heal')
def dead():
    provinces_rate_data()  # 各省死亡率与治愈率柱状图
    return render_template('dead_heal.html')

if __name__ == '__main__':
    jdbc = JDBC()
    app.run()
    # provinces_today_data();
    #china_total_data()
   #first_()




