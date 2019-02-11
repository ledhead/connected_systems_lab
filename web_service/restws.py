# sudo apt-get install python-pip
# sudo pip install web.py
# sudo pip install -U https://github.com/google/google-visualization-python/zipball/master
# run as: http://localhost:8080/motionlog/<datetime_interval>
import web
from datetime import datetime
from log_parser import LogParser

urls = (
    '/motionlog/(.*)', 'get_motionlog'
)

app = web.application(urls, globals())

class GetMotionLog:
	def GET(self, t_interval):
		web.header('Access-Control-Allow-Origin', '*')
		#web.header('Access-Control-Allow-Credentials', 'true')
		url = 'http://192.168.20.251/axis-cgi/systemlog.cgi'
		username = 'root'
		password = 'pass'
		parser = LogParser(url, username, password)
		dt = parser.parse_log(t_interval)
		return dt

if __name__ == "__main__":
    app.run()
