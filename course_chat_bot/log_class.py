import datetime
from telegram import Update
import pymongo


class Logger:
    def __init__(self):
        self.log = []
        self.client = pymongo.MongoClient()

    def log_func(self, func):
        def inner(*args, **kwargs):
            """For showing time"""
            now = datetime.datetime.now()
            func(*args, **kwargs)
            info = dict()
            bd = self.client.mongo_bd
            collection = bd.students
            info["username"] = args[0].effective_user.first_name
            try:
                info["username"] += " " + args[0].effective_user.last_name
            except BaseException:
                pass
            info["nickname"] = args[0].effective_user.username
            info["funcname"] = func.__name__
            info["message"] = args[0].message.text
            info["date"] = str(now)
            collection.insert_one(info)
            pass
        return inner

    def bd_write(self):
        pass

    def last_5_history(self, update: Update):
        """Echo the user history."""
        """message is the answer for a user"""
        message = ''
        """File with the name of user"""
        try:
            collection = self.client.mongo_bd.students
        except BaseException:
            return 'Error occurred'
        count = 0
        for line in collection.find().sort('_id', pymongo.DESCENDING):
            if line['nickname'] == update.effective_user.username:
                if count < 5:
                    count += 1
                    message += line['message'] + '\n'
                else:
                    break
        return f'History:\n{message}'
