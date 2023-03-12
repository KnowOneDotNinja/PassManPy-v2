# *****************************************************************************
# Author:           Mike Winebarger
# Date:             February 14, 2023,
# Description:      Class definition and methods for MongoDB database
# Input:            Various
# Output:           Various
# *****************************************************************************

import urllib.parse
import pymongo


class Database:
    """Class definition for main database class"""

    __client = None
    __db = None
    __accounts = None
    __account_lists = None

    @classmethod
    def __connect(cls):
        """This method handles connecting to the database"""

        # Set connection string
        mongo_uri = "mongodb+srv://dbuser:" + urllib.parse.quote("gMxP@CpLuRz9yjj") + \
                    "@cluster0.ranxsrq.mongodb.net/?retryWrites=true/"

        # Set client and link database and collections
        if cls.__client is None:
            cls.__client = pymongo.MongoClient(mongo_uri)
            cls.__db = cls.__client.LoginAccounts
            cls.__accounts = cls.__db.Accounts
            cls.__account_lists = cls.__db.AccountLists

    @classmethod
    def reset_data(cls):
        """This method rebuilds the data sets"""

        # Connect to database
        cls.__connect()

        # Establish individual accounts
        red1 = {
            "_id": "Reddit: dudeguy",
            "type": "Account",
            "site": "Reddit",
            "url": "www.reddit.com",
            "uname": "dudeguy",
            "pwd": "passwerd",
            "tlc": "2023-02-05"
        }

        red2 = {
            "_id": "Reddit: budpal",
            "type": "Account",
            "site": "Reddit",
            "url": "www.reddit.com",
            "uname": "budpal",
            "pwd": "passwerd",
            "tlc": "2022-10-17"
        }

        fb = {
            "_id": "Facebook: budpal",
            "type": "TFA",
            "site": "Facebook",
            "url": "www.facebook.com",
            "uname": "budpal",
            "pwd": "passwerd",
            "tlc": "2023-02-05",
            "typ": "phone alert",
            "info": "confirmation"
        }

        bank1 = {
            "_id": "Bank 1: dudeguy",
            "type": "TFA",
            "site": "Bank 1",
            "url": "www.bank1.com",
            "uname": "dudeguy",
            "pwd": "passwerd",
            "tlc": "2023-02-05",
            "typ": "phone app",
            "info": "biometric"
        }

        bank2 = {
            "_id": "Bank 2: dudeguy",
            "type": "TFA",
            "site": "Bank 2",
            "url": "www.bank2.com",
            "uname": "dudeguy",
            "pwd": "passwerd",
            "tlc": "2023-02-05",
            "typ": "phone app",
            "info": "biometric"
        }

        # Add all accounts to a list
        all_accounts = [red1, red2, fb, bank1, bank2]

        # Clear data for clean collections
        cls.__db.Accounts.drop()
        cls.__db.AccountLists.drop()

        # Reassign variables
        cls.__accounts = cls.__db.Accounts
        cls.__account_lists = cls.__db.AccountLists

        # Populate all accounts to collection
        cls.__accounts.insert_many(all_accounts)

        # Create account lists, populate them and add them to account_lists
        cls.__account_lists.insert_one({
            "_id": "All",
            "name": "All",
            "sec_factor": 10,
            "accounts": [account["_id"] for account in all_accounts]
        })

        cls.__account_lists.insert_one({
            "_id": "Social",
            "name": "Social",
            "sec_factor": 6,
            "accounts": [account["_id"] for account in [red1, red2, fb]]
        })

        cls.__account_lists.insert_one({
            "_id": "Financial",
            "sec_factor": 10,
            "name": "Financial",
            "accounts": [account["_id"] for account in [bank1, bank2]]
        })

    @classmethod
    def get_data(cls):
        """This method retrieves data from the database"""

        from Account import Account
        from TwoFactorAccount import TFA
        from AccountsList import AccountsList

        account_objects = []    # All accounts?
        list_objects = []       # All lists?

        # Connect to database
        cls.__connect()

        # Convert account collection to Account/TFA objects
        accounts = cls.__accounts.find()
        for account_dictionary in accounts:
            if account_dictionary["type"] == "Account":
                account_objects.append(Account(
                    account_dictionary["site"],
                    account_dictionary["url"],
                    account_dictionary["uname"],
                    account_dictionary["pwd"],
                    account_dictionary["tlc"]
                ))
            elif account_dictionary["type"] == "TFA":
                account_objects.append(TFA(
                    account_dictionary["site"],
                    account_dictionary["url"],
                    account_dictionary["uname"],
                    account_dictionary["pwd"],
                    account_dictionary["tlc"],
                    account_dictionary["typ"],
                    account_dictionary["info"]
                ))

        # Build account map
        account_map = {}
        for account in account_objects:
            account_map[account.get_key()] = account

        # Convert lists to AccountList objects
        all_lists = cls.__account_lists.find()

        for list_dictionary in all_lists:
            account_list = AccountsList(
                list_dictionary["name"],
                list_dictionary["sec_factor"]
            )
            for account_key in list_dictionary["accounts"]:
                account_list.add_account(account_map[account_key])

            # Append each list to list of lists
            list_objects.append(account_list)

            if account_list.get_list_name() == "All Accounts":
                account_objects = account_list

        return account_objects, list_objects

    @classmethod
    def upload_new_list(cls, new_list):
        """This method uploads updated AccountList data to database"""

        cls.__connect()

        # If list does not exist, add to database, else update existing list
        cls.__account_lists.update_one({"_id": new_list.get_list_id()}, {"$set": new_list.to_dict()}, upsert=True)

    @classmethod
    def upload_new_account(cls, new_account):
        """This method uploads updated Account data to database"""

        cls.__connect()

        # If account does not exist, add to database, else update existing account
        cls.__accounts.update_one({"_id": new_account.get_key()}, {"$set": new_account.to_dict()}, upsert=True)

    @classmethod
    def remove_list(cls, acc_list):
        """This method removes a list from the database"""

        cls.__account_lists.delete_one({"_id": acc_list.get_list_id()})
