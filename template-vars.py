#create a file called "vars.py" and copy the following code:
import os
import glob

shortcode = ""
username = ""

firefox_profiles = os.path.expandvars("%APPDATA%/Mozilla/Firefox/Profiles/")
profile_name = os.path.join(firefox_profiles, "*.default-release")
full_path = glob.glob(profile_name)

if not full_path:
    raise Exception("No Firefox profile found.")

fireFoxProfile = full_path[0]
fireFoxPath = os.path.join(fireFoxProfile, "cookies.sqlite")
