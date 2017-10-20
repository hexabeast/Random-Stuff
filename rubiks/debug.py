import warnings
warnings.filterwarnings("ignore")
import sys

oldstdout = sys.stdout

class NullWriter(object):
	def write(self, arg):
		pass
nullwrite = NullWriter()

def stopPrinting():
	global oldstdout, nullwrite
	oldstdout = sys.stdout
	sys.stdout = nullwrite
	
def startPrinting():
	global oldstdout, nullwrite
	sys.stdout = oldstdout
	