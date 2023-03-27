

'''

 知识点
	0.requests
	1.json. json格式数据，json格式字符串。
	2.正则. 分组
	3.datetime时间处理. 字符串，时间格式数据。

	4.github aciton.  cron 定时 https://blog.csdn.net/Ximerr/article/details/123501772

'''


import requests
import re
import json
import datetime
import mail


def get_data():
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
	url = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback=jQuery112305885166561803776_1645008522500&sortColumns=PUBLIC_START_DATE&sortTypes=-1&pageSize=50&pageNumber=1&reportName=RPT_BOND_CB_LIST&columns=ALL&quoteColumns=f2~01~CONVERT_STOCK_CODE~CONVERT_STOCK_PRICE%2Cf235~10~SECURITY_CODE~TRANSFER_PRICE%2Cf236~10~SECURITY_CODE~TRANSFER_VALUE%2Cf2~10~SECURITY_CODE~CURRENT_BOND_PRICE%2Cf237~10~SECURITY_CODE~TRANSFER_PREMIUM_RATIO%2Cf239~10~SECURITY_CODE~RESALE_TRIG_PRICE%2Cf240~10~SECURITY_CODE~REDEEM_TRIG_PRICE%2Cf23~01~CONVERT_STOCK_CODE~PBV_RATIO&source=WEB&client=WEB"
	r = requests.get(url,headers = headers, verify=False)

	print(r.status_code)

	if r.status_code != 200:
		# myLog.logErr("requests failed"+r.status_code)
		return False
	# print(r.text)
	#r.text 为jQuery1123007102200144612669_1676974358788(jsondataxxx);
	#截取返回结果中的json数据。
	pattern = re.compile('.*?\((.*)\);', re.S)
	items = re.findall(pattern, r.text)
	# print(items)

	try:
		jsondata=json.loads(items[0])
		data = jsondata['result']['data']

		result = ""
		today = datetime.datetime.today()
		# print(today)
		# print(type(today))
		for i in data:
			PUBLIC_START_DATE = i['PUBLIC_START_DATE']
			print(PUBLIC_START_DATE)
			d1 = datetime.datetime.strptime(PUBLIC_START_DATE, "%Y-%m-%d %H:%M:%S")
			# d1 = d1 + datetime.timedelta(hours=22)
			# print(d1)
			# print(type(d1))
			# if d1 > today:
			# 	continue
			# if d1 < today:
			# 	break

			if d1.month > today.month:
				continue

			if d1.month < today.month:
				break

			if d1.day > today.day:
				continue

			if d1.day < today.day:
				break

			# 只处理当天的可转债
			result += i['SECUCODE'] +' ' + i['SECURITY_NAME_ABBR'] + ' '+ PUBLIC_START_DATE +'\n'
		print(result)
		if result != '':
			mail.sendEmailByArgs('今日可转债打新 提醒',result)
	except Exception as e:
		pass
		# myLog.logErr(e)


if __name__ == '__main__':
	get_data()