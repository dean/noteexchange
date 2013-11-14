activate_this = '/var/www/tbkexch/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
sys.path.insert(0, '/var/www/tbkexch')
from tbkexch import app as application
