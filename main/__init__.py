import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

# import redis
# from flask_session import Session

# -- ---------------------------------------------------------------------------------
# -- Script Name : Ldap Authentication with FLask
# -- Author      : *******
# -- Date        : *******
# -- ---------------------------------------------------------------------------------
# -- Description : Authenticate users with Flask
# -- ---------------------------------------------------------------------------------
# -- Version History
# -- ===============
# --
# -- Who      		    version     Date      Description. 3
# -- ===       		    =======     ======    ======================
# -- XXXXXXXX             1.0       Jan 21    Initial Version.
# -- ---------------------------------------------------------------------------------


current_path = os.environ['PATH']
print(current_path)

# -- ---------------------------------------------------------------------------------
# -- Function    : Initiate the App C:\Users\p784138\AWS\Non-Prod\
# -- ---------------------------------------------------------------------------------

root_dir = os.path.abspath('.')
template_dir = root_dir + "/template"

app = Flask(__name__,
            template_folder=template_dir,
            root_path=root_dir
            )

bootstrap = Bootstrap(app)
app.config.from_object('settings')
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
# Bootstrap(app)

csrf = CSRFProtect(app)

print('Inside __init__py')
