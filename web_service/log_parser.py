import urllib2
from datetime import datetime, time
import json

class LogParser:
	"""
	Parses the system log of the camera to find events related to motion detection.
	The events are stored in JSON format.
	"""

    def __init__(self, url, username, password):
        self.log = self.get_log(url, username, password)

    def get_log(self, url, username, password):
		"""connect to camera and read log"""
        mgr = urllib2.HTTPPasswordMgrWithDefaultRealm()
        mgr.add_password(None, url, username, password)        
        opener = urllib2.build_opener(urllib2.HTTPDigestAuthHandler(mgr))
        urllib2.install_opener(opener)
        return urllib2.urlopen(url).readlines()

    def get_datetime(self, dt_string):
		"""convert date/time string of format yyyy-mm-ddThh:mm:ss to datetime object"""
        dt_object = datetime.strptime(dt_string, '%Y-%m-%dT%H:%M:%S')
        return dt_object

    def parse_log(self, t_interval):
		"""parse log"""
        t_interval = t_interval.split("_")
        interval_start = self.get_datetime(t_interval[0])
        interval_end = self.get_datetime(t_interval[1])
        prev = t_interval[0]
        end = t_interval[1]
        data = []
        for line in self.log:
            line.strip()
            if line.find("logger: Motion") > 0: # entry that belongs to motion log
    	        current = line[:19] # current time
            if self.get_datetime(current) > interval_start: # check if current time falls within the   interval
                motion = not (line[67:].strip() == "Motion detected") # the motion event up to this point is the opposite of what we observe now
            if self.get_datetime(current) < interval_end: # check if current time falls within the interval
                data.append({"Start":prev, "End":current, "Motion":motion}) # add current period			
                prev = current
            else:
                data.append({"Start":prev, "End":end, "Motion":motion}) # add last period and stop
            break
        json_data = json.dumps(data, indent=4) # write JSON
        print (json)
        return json_data

# used for testing
parser = LogParser('http://192.168.20.247/axis-cgi/systemlog.cgi', 'root', 'pass')
dt = parser.parse_log('2017-11-09T10:23:40_2017-11-09T12:16:20')	
