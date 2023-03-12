# *****************************************************************************
# Author:           Mike Winebarger
# Date:             February 22, 2023,
# Description:      Main UI class for web implementation
# Input:            Various
# Output:           Various
# *****************************************************************************

from flask import Flask, render_template, request, redirect, url_for
from AccountsList import AccountsList
from Account import Account


class WebUI:
    """Class definition for web UI -
    View the output on localhost:8000/"""

    __app = Flask(__name__)
    __accounts = None
    __account_lists = None

    def __init__(self):
        self.__app.secret_key = self.generate_key()

    @staticmethod
    def generate_key():
        """This method generates a cryptographically random session key"""

        import os

        return os.urandom(6)

    @staticmethod
    @__app.route("/")
    @__app.route("/home")
    @__app.route("/index")
    @__app.route("/default")
    @__app.route("/index.html")
    @__app.route("/default.html")
    def redirect_to_menu():
        return redirect(url_for("homepage"))

    @staticmethod
    @__app.route("/menu")
    def homepage():
        """This method defines the homepage and its menu options"""

        choices = {
            # URLs will be updated as features are written
            "/print-lists": "Display All Account Lists",
            "/get-info-for-create-list": "Create New Account List",
            "/select-list-to-delete": "Delete Account List",
            "/select-list-to-print": "Print an Account List",
            "/print-all-accounts": "Display All Accounts",
            "/index.html": "Remove Account From a List",
            "/get-data-for-update": "Change Password for an Account",
            "/": "Join Two Account Lists"
        }

        return render_template("menu.html", choices=choices)

    @staticmethod
    @__app.route("/print-lists")
    def print_lists():
        """This method displays a list of all account lists"""

        return render_template("print_lists.html", account_lists=WebUI.__account_lists)

    @staticmethod
    @__app.route("/select-list-to-print")
    def select_list_to_print():
        """This method displays a drop-down menu to allow the user to select an account list"""

        return render_template("print_list_form.html", account_lists=WebUI.__account_lists)

    @staticmethod
    @__app.route("/print-account-list")
    def print_account_list():
        """This method displays all accounts saved in a particular account list"""

        account_list_name = request.args["account_list_name"]

        for acc_list in WebUI.__account_lists:
            if acc_list.get_key() == account_list_name.lower():
                return render_template("print_account_list.html", account_list=acc_list)

        return render_template("error.html", error_message=f"There is no list named '{account_list_name}' :(")

    @staticmethod
    @__app.route("/print-all-accounts")
    def print_all_accounts():
        """This method displays all saved accounts"""
        return render_template("print_all_accounts.html", all_accounts=WebUI.__accounts)

    @staticmethod
    @__app.route("/get-info-for-create-list")
    def get_info_for_create_list():
        """This method directs the user to a data acquisition form"""

        return render_template("create_list_form.html")

    @staticmethod
    @__app.route("/create-list")
    def create_list():
        """This method allows the user to create a new account list"""

        name = request.args["list_name"]
        sec = request.args["sec_factor"]

        # Check for duplicate lists
        for acc_list in WebUI.__account_lists:
            if name.lower() == acc_list.get_key():
                return render_template("error.html", error_message=f"List '{name}' already exists :(")

        # Add new list to list of lists
        new_list = AccountsList(name, sec)
        WebUI.__account_lists.append(new_list)

        # Uploads new list to database
        AccountsList.upload(new_list)

        return render_template("create_list_success.html", list_name=name, sec_factor=sec)


    @staticmethod
    @__app.route("/select-list-to-delete")
    def select_list_to_delete():
        """This method directs the user to a data acquisition form"""

        return render_template("delete_list_form.html", account_lists=WebUI.__account_lists)

    @staticmethod
    @__app.route("/delete-list")
    def delete_list():
        """This method allows a user to delete an account list"""

        name = request.args["list_name"]

        for acc_list in WebUI.__account_lists:
            if acc_list.get_list_name().lower() == name.lower():
                WebUI.__account_lists.remove(acc_list)
                AccountsList.remove_list(acc_list)

        return render_template("delete_success.html", list_name=name)

    @staticmethod
    @__app.route("/get-data-for-update")
    def get_data_for_update():
        """This method directs the user to a data acquisition form"""

        return render_template("update_password_form.html", accounts=WebUI.__accounts)

    @staticmethod
    @__app.route("/update-password", methods=["POST"])
    def update_password():
        """This method updates the password for a selected account"""

        pwd = request.form["pwd"]
        account_name = request.form["account_name"]

        for account in WebUI.__accounts:
            if account_name == account.get_key():
                account.set_account_pwd(pwd)
                Account.upload(account)

                return render_template("password_success.html", account=account_name)

        return render_template("error.html", error_message=f"There is no account named {account_name} :(")

    @staticmethod
    def run():
        """This method runs the UI and populates the class variables"""

        WebUI.__accounts, WebUI.__account_lists = AccountsList.fetch_data()
        WebUI.__app.run(port=8000)


if __name__ == "__main__":
    app = WebUI()
    app.run()
