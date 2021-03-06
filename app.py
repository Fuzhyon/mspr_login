import pyotp
from flask import *
from flask import render_template, request
from ldap3 import Server, Connection, ALL

from forms.LoginForm import *
from main import app
from main import csrf
from pwnedapi import Password

def global_ldap_authentication_func(user_name, user_pwd):
    """
      Function: global_ldap_authentication
       Purpose: Make a connection to encrypted LDAP server.
       :params: ** Mandatory Positional Parameters
                1. user_name - LDAP user Name
                2. user_pwd - LDAP User Password
       :return: None
    """
    passwd = Password(user_pwd)

    # fetch the username and password
    ldap_user_name = user_name.strip()
    ldap_user_pwd = user_pwd.strip()



    # ldap server hostname and port
    ldsp_server = f"ldap://localhost:389"

    # dn
    root_dn = "dc=example,dc=org"

    # user
    user = f'cn={ldap_user_name},{root_dn}'

    print(user)
    server = Server(ldsp_server, get_info=ALL)

    connection = Connection(server,
                            user=user,
                            password=ldap_user_pwd)
    if not connection.bind():
        print(f" *** Cannot bind to ldap server: {connection.last_error} ")
        l_success_msg = f' ** Failed Authentication: {connection.last_error}'
    elif passwd.is_pwned():
        print(f"Your password has been pwned {passwd.pwned_count} times.")
        l_success_msg = 'badmdp'
    else:
        print(f" *** Successful bind to ldap server")
        l_success_msg = 'Success'

    return l_success_msg


@app.route('/login', methods=['GET', 'POST'])
def index():
    # initiate the form..
    form = LoginValidation(request.form)

    if request.method in 'POST':
        login_id = form.user_name_pid.data
        login_password = form.user_pid_Password.data

        # create a directory to hold the Logs
        login_msg = global_ldap_authentication_func(login_id, login_password)

        # validate the connection
        if login_msg == "Success":
            success_message = f"*** Authentication Success "
            return redirect(url_for("login_2fa"))
        elif login_msg == "badmdp":
            return render_template("flash.html", error_message=str("Mauvais mot de passe"))
        else:
            error_message = f"*** Authentication Failed - {login_msg}"
            return render_template("error.html", error_message=str(error_message))

    return render_template('login.html', form=form)

@app.route('/redirect', methods=['GET', 'POST'])
@csrf.exempt
def redirect_otp():
    secret = pyotp.random_base32()
    return render_template("includes/login_2fa.html", secret=secret)
# 2FA page route
@app.route("/login/2fa/")
@csrf.exempt
def login_2fa():
    # generating random secret key for authentication
    secret = pyotp.random_base32()
    return render_template("includes/login_2fa.html", secret=secret)


# 2FA form route
@app.route("/login/2fa/", methods=['GET', 'POST'])
@csrf.exempt
def login_2fa_form():
    # getting secret key used by user
    secret = request.form.get("secret")
    # getting OTP provided by user
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(str(otp)):
        # inform users if OTP is valid
        flash("The TOTP 2FA token is valid", "success")
        return redirect(url_for("login_2fa"))
    else:
        # inform users if OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("login_2fa"))


if __name__ == '__main__':
    app.run(debug=True)
