#create a file called "vars.py" and copy the following:
import os

shortcode = ""
username = ""

fireFoxProfile = "%APPDATA%/Mozilla/Firefox/Profiles/qc3fw8f0.default-release/cookies.sqlite"
fireFoxPath = os.path.expandvars(fireFoxProfile)
