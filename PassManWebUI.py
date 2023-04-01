# *****************************************************************************
# Author:           Mike Winebarger
# Date:             February 22, 2023,
# Description:      Main UI class for web implementation of PassMan
# Input:            Various
# Output:           Various
# Notes:            Need functionality for adding account
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
    def find_account_list(account_list_name):
        """This method takes a list name and returns a list object"""

        for account_list in WebUI.__account_lists:
            if account_list.get_key() == account_list_name.lower():
                return account_list

        return None

    @staticmethod
    def find_account(account_name, account_list):
        """This method takes an account name and list name
        and returns an account object"""

        for account in account_list:
            if account_name.lower() == account.get_key().lower():
                return account

        return None

    @staticmethod
    @__app.route("/")
    @__app.route("/home")
    @__app.route("/index")
    @__app.route("/default")
    @__app.route("/index.html")
    @__app.route("/default.html")
    def redirect_to_menu():
        """This method redirects common homepage URLs to /menu"""

        return redirect(url_for("homepage"))

    @staticmethod
    @__app.route("/menu")
    def homepage():
        """This method defines the homepage and its menu options"""

        # Build choice map
        choices = {
            "/print-lists": "Display All Account Lists",
            "/get-info-for-create-list": "Create New Account List",
            "/select-list-to-delete": "Delete Account List",
            "/select-list-to-print": "Print an Account List",
            "/print-all-accounts": "Display All Accounts",
            "/select-list-for-account-removal": "Remove Account From a List",
            "/get-data-for-update": "Change Password for an Account",
            "/select-lists-to-join": "Join Two Account Lists"
        }

        # Display menu
        return render_template("menu.html", choices=choices)

    @staticmethod
    @__app.route("/print-lists")
    def print_lists():
        """This method displays a list of all account lists"""

        return render_template(
            "print_lists.html",
            account_lists=WebUI.__account_lists
        )

    @staticmethod
    @__app.route("/select-list-to-print")
    def select_list_to_print():
        """This method directs the user to a data acquisition form"""

        return render_template(
            "print_list_form.html",
            account_lists=WebUI.__account_lists
        )

    @staticmethod
    @__app.route("/print-account-list")
    def print_account_list():
        """This method displays all accounts saved in a particular account list"""

        # Get list name from form
        account_list_name = request.args["account_list_name"]

        # If found, display the accounts in the list
        for acc_list in WebUI.__account_lists:
            if acc_list.get_key() == account_list_name.lower():

                return render_template(
                    "print_account_list.html",
                    account_list=acc_list
                )

        # If not found, display error page
        return render_template(
            "error.html",
            error_message=f"There is no list named '{account_list_name}' :("
        )

    @staticmethod
    @__app.route("/print-all-accounts")
    def print_all_accounts():
        """This method displays all saved accounts"""

        return render_template(
            "print_all_accounts.html",
            all_accounts=WebUI.__accounts
        )

    @staticmethod
    @__app.route("/get-info-for-create-list")
    def get_info_for_create_list():
        """This method directs the user to a data acquisition form"""

        return render_template("create_list_form.html")

    @staticmethod
    @__app.route("/create-list")
    def create_list():
        """This method allows the user to create a new account list"""

        # Get name and info from form
        name = request.args["list_name"]
        sec = int(request.args["sec_factor"])

        # Check for duplicate lists
        for acc_list in WebUI.__account_lists:
            if name.lower() == acc_list.get_key():

                return render_template(
                    "error.html",
                    error_message=f"List '{name}' already exists :("
                )

        # Update data
        new_list = AccountsList(name, sec)
        WebUI.__account_lists.append(new_list)
        AccountsList.upload(new_list)

        # Display success page
        return render_template(
            "create_list_success.html",
            list_name=name, sec_factor=sec
        )

    @staticmethod
    @__app.route("/select-list-to-delete")
    def select_list_to_delete():
        """This method directs the user to a data acquisition form"""

        return render_template(
            "delete_list_form.html",
            account_lists=WebUI.__account_lists
        )

    @staticmethod
    @__app.route("/delete-list")
    def delete_list():
        """This method allows a user to delete an account list"""

        # Get list name from form
        name = request.args["list_name"]

        # If found, remove account
        for acc_list in WebUI.__account_lists:
            if acc_list.get_list_name().lower() == name.lower():

                WebUI.__account_lists.remove(acc_list)
                AccountsList.remove_list(acc_list)

        # Display success page
        return render_template("delete_list_success.html", list_name=name)

    @staticmethod
    @__app.route("/select-list-for-account-removal")
    def select_list_for_account_removal():
        """This method directs the user to a data acquisition form"""

        return render_template(
            "select_list_form.html",
            account_lists=WebUI.__account_lists
        )

    @staticmethod
    @__app.route("/select-account-to-remove")
    def select_account_to_remove():
        """This method directs the user to a data acquisition form"""

        # Get name and find account list object
        list_name = request.args["list_name"]
        account_list = WebUI.find_account_list(list_name)

        # If list not found, display error
        if account_list is None:
            return render_template(
                "error.html",
                error_message=f"There is no list named '{list_name}' :("
            )

        # Send account list to a form to select account
        return render_template(
            "remove_account_form.html",
            account_list=account_list
        )

    @staticmethod
    @__app.route("/select-lists-to-join")
    def select_lists_to_join():
        """This method directs the user to a data acquisition form"""

        return render_template(
            "join_lists_form.html",
            account_lists=WebUI.__account_lists
        )

    @staticmethod
    @__app.route("/join-lists")
    def join_lists():
        """This method joins two selected lists"""

        # Get names and list objects
        list1_name = request.args["list1_name"]
        list2_name = request.args["list2_name"]
        list1 = WebUI.find_account_list(list1_name)
        list2 = WebUI.find_account_list(list2_name)

        # If list not found, display error page
        if list1 is None:
            return render_template(
                "error.html",
                error_message=f"There is no list named '{list1_name}' :("
            )

        if list2 is None:
            return render_template(
                "error.html",
                error_message=f"There is no list named '{list2_name}' :("
            )

        # Join the lists
        joined = list1 + list2

        # Add joined list to lists and database
        WebUI.__account_lists.append(joined)
        AccountsList.upload(joined)

        # Display success page
        return render_template(
            "join_lists_success.html",
            l1=list1_name,
            l2=list2_name,
            name=joined.get_list_name()
        )

    @staticmethod
    @__app.route("/remove-account")
    def remove_account():
        """This method removes a selected account from a selected list"""

        # Get names and objects
        list_name = request.args["list_name"]
        account_name = request.args["account_name"]
        account_list = WebUI.find_account_list(list_name)
        account = WebUI.find_account(account_name, account_list)

        # If not found, display error
        if account_list is None:
            return render_template(
                "error.html",
                error_message=f"There is no list named '{list_name}' :("
            )

        if account is None:
            return render_template(
                "error.html",
                error_message=f"There is no account named '{account_name}' :("
            )

        # Remove account
        account_list.remove(account)
        AccountsList.upload(account_list)

        # Display success page
        return render_template(
            "remove_account_success.html",
            account=account,
            account_list_name=list_name
        )

    @staticmethod
    @__app.route("/get-data-for-update")
    def get_data_for_update():
        """This method directs the user to a data acquisition form"""

        return render_template(
            "update_password_form.html",
            accounts=WebUI.__accounts
        )

    @staticmethod
    @__app.route("/update-password", methods=["POST"])
    def update_password():
        """This method updates the password for a selected account"""

        # Get info
        pwd = request.form["pwd"]
        account_name = request.form["account_name"]

        # If found, set password and update account
        for account in WebUI.__accounts:
            if account_name == account.get_key():

                account.set_account_pwd(pwd)
                Account.upload(account)

                # Display success page
                return render_template(
                    "update_password_success.html",
                    account=account_name
                )

        # If not found, display error page
        return render_template(
            "error.html",
            error_message=f"There is no account named {account_name} :("
        )

    @staticmethod
    def run():
        """This method runs the UI and populates the class variables"""

        # Get data and run app
        WebUI.__accounts, WebUI.__account_lists = AccountsList.fetch_data()
        WebUI.__app.run(port=8000)


if __name__ == "__main__":
    app = WebUI()
    app.run()
