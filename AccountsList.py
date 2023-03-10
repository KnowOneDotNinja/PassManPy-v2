# *****************************************************************************
# Author:           Mike Winebarger
# Date:             February 14, 2023,
# Description:      Class definition and methods for account list objects
# Input:            Various
# Output:           Various
# *****************************************************************************

from Database import Database


class AccountsList:
    """Class definition for Account List objects -
    These are containers for accounts of a similar type"""
    __accounts = []
    __name = ""

    def __init__(self, name, sec_factor, *args):
        self._id = name
        self.__name = self._id
        self.__sec_factor = sec_factor
        self.__accounts = list(args)

    def __str__(self):
        return f"{self.get_list_name()}"

    def __repr__(self):
        return f"{self.get_list_name()}"

    def __iter__(self):
        return iter(self.__accounts)

    def __contains__(self, item):
        return item in self.__accounts

    def __add__(self, other):
        """This method adds '+' functionality for account lists"""

        sec = max(self.get_sec_factor(), other.get_sec_factor())
        new = AccountsList(f"{self.get_list_name()}" + "/" + f"{other.get_list_name()}", sec)

        for account in self.__accounts:
            if account not in new:
                new.add_account(account)

        for account in other.__accounts:
            if account not in new:
                new.add_account(account)

        return new

    def add_account(self, *args):
        for acc in args:
            self.__accounts.append(acc)

    def remove(self, account):
        self.__accounts.remove(account)

    def get_list_id(self):
        return self.__name

    def get_list_name(self):
        return self.__name

    def get_sec_factor(self):
        return self.__sec_factor

    def get_key(self):
        return self.__name.lower()

    def to_dict(self):
        """This method converts AccountList objects to dictionaries for uploading to database"""

        return {
            "_id": self.get_list_id(),
            "name": self.get_list_name(),
            "sec_factor": self.get_sec_factor(),
            "accounts": [account.get_key() for account in self.__accounts]
        }

    @staticmethod
    def fetch_data():
        # Retrieve data from database
        return Database.get_data()

    @staticmethod
    def upload(new_list):
        # Upload Account List to database
        Database.upload_new_list(new_list)

    @staticmethod
    def remove_list(acc_list):
        # Remove Account List from database
        Database.remove_list(acc_list)
