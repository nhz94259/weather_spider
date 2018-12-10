# -*- coding: utf-8 -*-

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import json
import os

class WeatherSpiderPipeline(object):

    def process_item(self, item, spider):
        # 获取当前工作目录
        base_dir = os.getcwd()
        datafile = base_dir+'\spiders\data\data.txt';
        fp = open(datafile, 'a')

        # 从内存以追加的方式打开文件，并写入对应的数据
        with open(datafile, 'a') as f:
            f.write(item['date'] + '\t')
            f.write(item['temperature'] + '\t')
            f.write(item['weather'] + '\t')
            f.write(item['wind'] + '\t')
            f.write('\n')
        return item

class data2mysql(object):
    def process_item(self, item, spider):
        # 将item里的数据拿出来
        date = item['date']
        temperature = item['temperature']
        weather = item['weather']
        wind = item['wind']

        # 和本地的scrapyDB数据库建立连接
        connection = pymysql.connect(
            host='127.0.0.1',  # 连接的是本地数据库
            user='root',  # 自己的mysql用户名
            passwd='zxczxc123',  # 自己的密码
            db='timmo',  # 数据库的名字
            charset='utf8mb4',  # 默认的编码方式：
            cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # 创建更新值的sql语句
                sql = """INSERT INTO WEATHER(date,temperature,weather,wind)
                        VALUES (%s, %s, %s, %s)"""
                # 执行sql语句
                # excute 的第二个参数可以将sql缺省语句补全，一般以元组的格式
                cursor.execute(
                    sql, (date, temperature, weather, wind))
            # 提交本次插入的记录
            connection.commit()
        finally:
            # 关闭连接
            connection.close()
        return item
