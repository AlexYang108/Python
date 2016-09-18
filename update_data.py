# -*- coding:utf-8 -*-
#!/usr/bin/python

import xlrd
import sys
import os
import codecs
import MySQLdb

#数据文件,excel格式
f1name = sys.argv[1]

#打开excel文件
f1 = xlrd.open_workbook(f1name)

#获取一个工作表
t1 = f1.sheets()[0]          #通过索引顺序获取

#获取记录数
t1nrow = t1.nrows

#连接数据库
db = MySQLdb.connect("10.32.157.38","root","alexyang34","fq_test" )

#连接游标
cursor = db.cursor()

for i in range(1,t1nrow):

	lineid = ''
	order_id = ''
	from_state = ''
	from_time = ''
	sql1 = ''
	sql2 = ''

	#从第二行开始读取数据
	lineid = str(t1.cell(i,0).value)
	order_id = str(t1.cell(i,1).value)
	from_state = str(t1.cell(i,2).value)
	from_time = str(t1.cell(i,3).value)

	#第一步，判断该订单号是否已经存在，如果不存在insert，如果已经存在update
	sql1 = "SELECT order_id FROM order_router_log WHERE order_id = '%s'" % (order_id)

	try:
		cursor.execute(sql1)

		rows = cursor.fetchall()

		if (len(rows) > 0):

			#记录已经存在，update
			sql2 = "UPDATE order_router_log  SET %s = '%s' WHERE order_id = '%s'" %(from_state, from_time, order_id)

		else:
			#记录不存在，insert
			sql2 = "INSERT INTO order_router_log (line_id, order_id, %s) VALUES('%s', '%s', '%s')" %(from_state, lineid, order_id, from_time)


		try:
			cursor.execute(sql2)

			db.commit()

		except Exception, e:

			print(e)
			db.rollback()

	except Exception, e:
		
		print(e)

#关闭db
db.close()


