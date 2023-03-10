# *****************************************************************************
# Author:           Mike Winebarger
# Date:             February 14, 2023,
# Description:      Main UI class - Handles all user interaction events
# Input:            Various
# Output:           Various
# Notes:            I considered building a list selector, but I liked using
#                   custom prompts
# *****************************************************************************

import datetime
from TwoFactorAccount import TFA
from Account import Account
from AccountsList import AccountsList
import input_validation as validate


class PassManUI:
    """Main UI class"""

    __accounts = None
    __account_lists = []

    @staticmethod
    def print_menu():
        """This method prints the main menu options"""

        print("\nSelect from the following choices:\n")
        print("1) Display All Account Lists")
        print("2) Create New Account List")
        print("3) Delete Account List")
        print("4) Print an Account List")
        print("5) Display All Accounts")
        print("6) Create New Account & Add to List")
        print("7) Remove Account From a List")
        print("8) Change Password for an Account")
        print("9) Join Two Account Lists")
        print("0) Exit")

    @staticmethod
    def find_account(acc_list):
        """This method takes an account list and finds and returns an account using site and username"""

        # Display available accounts
        choices = [f"{acc.get_account_name()}: {acc.get_account_uname()}" for acc in acc_list] + ["Back"]
        print(choices)

        # Validate user choice
        account = validate.select_item(choices=choices, prompt="Which account (Site: Username): ").lower()

        if account == "Back":
            return None
        else:
            for acc in acc_list:
                if account == f"{acc.get_account_name().lower()}: {acc.get_account_uname().lower()}":
                    return acc

            return None

    @staticmethod
    def change_passwd():
        """This method allows the user to change the password for a selected account"""

        account = PassManUI.find_account(PassManUI.__accounts)

        if account is not None:
            pwd = validate.password()

            account.set_account_pwd(pwd)
            Account.upload(account)

            print(f"\nPassword for '{account}' has been changed")
            input("\nPress <Enter> to continue: ")

    @staticmethod
    def remove_account():
        """This method allows a user to remove an account from a list"""

        # Display available lists
        print(list(item.get_list_name() for item in PassManUI.__account_lists) + ["Back"])

        # Validate user choice
        lst = validate.select_item(choices=[item.get_list_name() for item in PassManUI.__account_lists] + ["Back"],
                                   prompt="Choose a list to remove an account from: ").lower().capitalize()

        if lst != "Back":

            # For each list in the list of account lists
            for acc_list in PassManUI.__account_lists:
                if acc_list.get_list_name().lower() == lst.lower():

                    # Returns 'None' or a valid account
                    account = PassManUI.find_account(acc_list)

                    if account is not None and account in acc_list:
                        # Remove account from list
                        acc_list.remove(account)
                        AccountsList.upload(acc_list)

                        print(f"\n{account} removed from {acc_list}")
                        input("\nPress <Enter> to continue: ")

    @staticmethod
    def add_new_account():
        """This method allows a user to create a new account and add it to an existing list - I opted
        to not run a check for duplicates as multiple logins may be used for the same site"""

        # Display available lists
        print(list(item.get_list_name() for item in PassManUI.__account_lists) + ["Back"])

        # Validate user choice
        name = validate.select_item(choices=[item.get_list_name() for item in PassManUI.__account_lists] + ["Back"],
                                    prompt="Choose a list to add new account to: ").lower().capitalize()

        # Add new account to chosen list
        if name != "Back":
            for chosen_list in PassManUI.__account_lists:
                if chosen_list.get_list_name().lower() == name.lower():
                    account = PassManUI.create_account()

                    if account is not None:
                        chosen_list.add_account(account)
                        PassManUI.__accounts.append(account)

                        # Update database
                        AccountsList.upload(chosen_list)
                        AccountsList.upload(PassManUI.__accounts)

                        print(f"\nNew account for {account.get_account_name()} was added to list '{name}'")
                        input("\nPress <Enter> to continue: ")

    @staticmethod
    def create_account():
        """This method handles the creation of a new account object"""

        error_str = "can not be empty"

        # Get and validate all data from user
        site = validate.input_string(prompt="\nEnter a site name for the new account: ",
                                     error=f"Name {error_str}").lower().capitalize()
        url = validate.input_string(prompt="Enter the URL of the site: ", error=f"URL {error_str}").lower()
        uname = validate.input_string(prompt="Enter the username: ", error=f"Username {error_str}")
        pwd = validate.input_string(prompt="Enter the password: ", error=f"Password {error_str}")
        tlc = str(datetime.date.today())

        # Check for two-factor account
        is_tfa = validate.y_or_n(prompt="\nDoes this account require two-factor authentication (Yes/No): ")

        if is_tfa:
            typ = validate.input_string(prompt="\nEnter the method of authentication (phone app, pin): ")
            info = validate.input_string(prompt="Enter the information needed to authenticate "
                                                "(pin #, biometric, etc.): ")

            # Check for duplicate lists
            for account in PassManUI.__accounts:
                if site == account.get_account_name() and uname == account.get_account_uname():
                    print(f"ERROR: '{site}: {uname}' combination already exists")
                    input("\nPress <Enter> to continue: ")
                    return

            # Create TFA Account
            account = TFA(site, url, uname, pwd, tlc, typ, info)

            # Upload to database
            TFA.upload(account)

        else:
            # Check for duplicate lists
            for account in PassManUI.__accounts:
                if site == account.get_account_name() and uname == account.get_account_uname():
                    print(f"ERROR: '{site}: {uname} combination already exists")
                    input("\nPress <Enter> to continue: ")
                    return

            # Create standard account
            account = Account(site, url, uname, pwd, tlc)

            # Upload to database
            Account.upload(account)

        return account

    @staticmethod
    def create_list():
        """This method allows the user to create a new account list"""

        # Get and validate data from user
        name = validate.input_string(prompt="Name of new list: ").lower().capitalize()
        sec = validate.input_number(prompt="Set security level (1-10): ", ge=1, le=10)

        # Check for duplicate lists
        for account_list in PassManUI.__account_lists:
            if name == account_list.get_list_name():
                print(f"ERROR: List '{name}' already exists")
                input("\nPress <Enter> to continue: ")
                return

        # Add new list to list of lists
        new_list = AccountsList(name, sec)
        PassManUI.__account_lists.append(new_list)

        # Update database
        AccountsList.upload(new_list)

        print(f"\nCreated new list '{name}' with security level {sec}")
        input("\nPress <Enter> to continue: ")

    @staticmethod
    def delete_list():
        """This method allows a user to delete an account list"""

        # Display available lists
        print(list(item.get_list_name() for item in PassManUI.__account_lists) + ["Back"])

        # Validate user choice
        name = validate.select_item(choices=[item.get_list_name() for item in PassManUI.__account_lists] + ["Back"],
                                    prompt="Choose a list to delete: ").lower().capitalize()

        # Delete selected list
        if name != "Back":
            for acc_list in PassManUI.__account_lists:
                if acc_list.get_list_name().lower() == name.lower():
                    PassManUI.__account_lists.remove(acc_list)
                    AccountsList.remove_list(acc_list)

            print(f"\nDeleted '{name}' account list")

            input("\nPress <Enter> to continue: ")

    @staticmethod
    def join():
        """This method allows the user to join two lists, rejecting duplicate account entries"""

        # Display available lists
        print("Lists available for joining:")
        print(list(item.get_list_name() for item in PassManUI.__account_lists) + ["Back"])

        # Validate  first user choice
        name1 = validate.select_item(choices=[item.get_list_name() for item in PassManUI.__account_lists] + ["Back"],
                                     prompt="\nChoose first list: ").lower().capitalize()

        if name1 != "Back":
            for item1 in PassManUI.__account_lists:
                if item1.get_list_name() == name1:

                    # Validate second user choice
                    name2 = validate.select_item(choices=[item.get_list_name() for item in PassManUI.__account_lists],
                                                 prompt="Choose second list: ").lower().capitalize()

                    for item2 in PassManUI.__account_lists:
                        if item2.get_list_name() == name2:

                            # Join the lists
                            joined = item1 + item2

                            # Add joined list to lists and database
                            PassManUI.__account_lists.append(joined)
                            AccountsList.upload(joined)

                            print(f"\nJoined {item1} with {item2}, creating {joined} "
                                  f"with security level {joined.get_sec_factor()}")
                            input("\nPress <Enter> to continue: ")

    @staticmethod
    def print_account_list(account_list):
        """This method takes an account list object and prints its contents"""

        print(account_list.get_list_name(), ": ")
        for account in account_list:
            print(">> ", account)

    @staticmethod
    def print_lists():
        """This method displays all account lists"""

        print("These are the current account lists:")

        for lst in PassManUI.__account_lists:
            print(lst)

        input("\nPress <Enter> to continue: ")

    @staticmethod
    def print_accounts():
        """This method displays all saved accounts"""

        # Print all saved accounts
        acc_list = PassManUI.__accounts

        for acc in acc_list:
            print(f"{acc}")

        input("\nPress <Enter> to continue: ")

    @staticmethod
    def print_list():
        """This method allows a user to display the accounts in an account list"""

        # Display available lists
        print(list(item.get_list_name() for item in PassManUI.__account_lists))

        # Validate user choice
        name = validate.select_item(choices=[item.get_list_name() for item in PassManUI.__account_lists],
                                    prompt="Choose a list to display: ").lower().capitalize()

        # Display contents of selected list
        for item in PassManUI.__account_lists:
            if item.get_list_name().lower() == name.lower():
                PassManUI.print_account_list(item)

        input("\nPress <Enter> to continue: ")

    @staticmethod
    def run():
        """Run the UI"""

        PassManUI.__accounts, PassManUI.__account_lists = AccountsList.fetch_data()

        while True:
            PassManUI.print_menu()

            # Get and validate menu choice
            choice = validate.select_item(choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                                          prompt=">> ")
            if choice == "1":
                PassManUI.print_lists()
            elif choice == "2":
                PassManUI.create_list()
            elif choice == "3":
                PassManUI.delete_list()
            elif choice == "4":
                PassManUI.print_list()
            elif choice == "5":
                PassManUI.print_accounts()
            elif choice == "6":
                PassManUI.add_new_account()
            elif choice == "7":
                PassManUI.remove_account()
            elif choice == "8":
                PassManUI.change_passwd()
            elif choice == "9":
                PassManUI.join()
            elif choice == "0":
                print("Thank you for using Password Manager!")
                break


if __name__ == '__main__':
    PassManUI().run()
