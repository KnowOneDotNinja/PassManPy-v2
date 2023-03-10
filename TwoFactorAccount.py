# *****************************************************************************
# Author:           Mike Winebarger
# Date:             January 26, 2023,
# Description:      Class definition for TFA account objects
# Input:            None
# Output:           None
# *****************************************************************************

from Account import Account


class TFA(Account):
    """Class definition for two-factor accounts"""

    def __init__(self, site, url, uname, pwd, tlc, typ, info):
        super().__init__(site, url, uname, pwd, tlc)
        self.__site = site
        self.__url = url
        self.__uname = uname
        self.__tlc = tlc
        self.__pwd = pwd
        self.__type = typ
        self.__info = info

    def get_tfa_typ(self):
        return self.__type

    def get_tfa_info(self):
        return self.__info

    def to_dict(self):
        """This method converts TFA objects to dictionaries for uploading to database"""

        return {
            "_id": self.get_account_id(),
            "type": "Account",
            "site": self.get_account_name(),
            "url": self.get_account_url(),
            "uname": self.get_account_uname(),
            "pwd": self.__pwd,
            "tlc": self.__tlc,
            "typ": self.get_tfa_typ(),
            "info": self.get_tfa_info()
        }
