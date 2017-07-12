# coding=utf-8
from flask import Flask, render_template, request
import MySQLdb as mysql
import json

db = mysql.connect(user="root", passwd="my-secret-pw", db="memory", host="127.0.0.1")
db.autocommit(True)
cur = db.cursor()

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

tmp_time = 0

@app.route('/data')
def data():
	global tmp_time
	if tmp_time>0:
		sql = 'select * from memory where time>%s' % (tmp_time/1000)
	else:
		sql = 'select * from memory'
	cur.execute(sql)
	arr = []
	for i in cur.fetchall():
		arr.append([i[1]*1000,i[0]])
	if len(arr)>0:
		tmp_time = arr[-1][0]
	return json.dumps(arr)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=9092, debug=True)