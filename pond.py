import syslog
import weewx
from weewx.wxengine import StdService

class PondService(StdService):
    def __init__(self, engine, config_dict):
        super(PondService, self).__init__(engine, config_dict)      
        d = config_dict.get('PondService', {})
        self.filename = d.get('filename', '/var/lib/bridge-data/pressure')
        syslog.syslog(syslog.LOG_INFO, "pond: using %s" % self.filename)
        self.bind(weewx.NEW_ARCHIVE_RECORD, self.read_file)

    def read_file(self, event):
	data= {}
        try:
            with open(self.filename) as f:
		for line in f:
            		event.record['pressure'] = float(line)
            		syslog.syslog(syslog.LOG_DEBUG, "pond: found value of %s" % line)
        except Exception as e:
            syslog.syslog(syslog.LOG_ERR, "pond: cannot read value: %s" % e)
