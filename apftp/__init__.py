# environment variables
import os 

FTP_USER = os.environ.get('AP_FTP_USER', None)
FTP_PASS = os.environ.get('AP_FTP_PASS', None)
FTP_URL = os.environ.get('AP_FTP_URL', 'electionsonline.ap.org')
TMP_DIR = os.environ.get('AP_FTP_TMP_DIR', '/tmp')