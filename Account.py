# *****************************************************************************
# Author:           Mike Winebarger
# Date:             January 26, 2023,
# Description:      Class definition and methods for account objects
# Input:            None
# Output:           None
# *****************************************************************************

class Account:
    """Class definition for Account objects"""

    def __init__(self, site, url, uname, pwd, tlc):
        self.__id = f"{site}: {uname}"
        self.__acc_type = "Account"
        self.__site = site.lower().capitalize()
        self.__url = url
        self.__uname = uname
        self.__pwd = pwd
        self.__tlc = tlc

    def __str__(self):
        return self.__id

    def __repr__(self):
        return self.__id

    def get_account_id(self):
        return self.__id

    def get_account_name(self):
        return self.__site

    def get_account_url(self):
        return self.__url

    def get_account_uname(self):
        return self.__uname

    def set_account_pwd(self, pwd):
        self.__pwd = pwd

    def set_account_ttc(self, ttc):
        self.__tlc = ttc

    def get_key(self):
        return self.__id

    def get_pwd(self):
        return self.__pwd

    def to_dict(self):
        """This method converts Account objects to dictionaries for uploading to database"""

        return {
            "_id": self.get_account_id(),
            "type": "Account",
            "site": self.get_account_name(),
            "url": self.get_account_url(),
            "uname": self.get_account_uname(),
            "pwd": self.__pwd,
            "tlc": self.__tlc
        }

    @staticmethod
    def upload(new_account):
        # Upload account to database
        from Database import Database

        Database.upload_new_account(new_account)
