import unittest
from unittest import mock
from course_chat_bot.log_class import Logger
import datetime
import pymongo
import mongomock

logger = Logger()


@logger.log_func
def simple_action(update):
    return None


class TestLoggerLogFunc(unittest.TestCase):

    def setUp(self):
        self.update = mock.MagicMock()
        self.update.message.text = 'testing'
        self.update.effective_user.first_name = 'Jack'
        self.update.effective_user.username = "Jack nickname"
        self.update.effective_user.last_name = None
        pymongo.MongoClient = mongomock.MongoClient
        logger.client = mongomock.MongoClient()
        self.client = pymongo.MongoClient()
        self.collection = logger.client.logger.client.mongo_bd.students

    def test_log_func(self):
        count_doc = self.collection.count_documents({})
        simple_action(self.update)
        for line in self.collection.find():
            print(line)
        self.assertEqual(count_doc + 1, self.collection.count_documents({}))

    def test_log_func_order(self):
        self.collection.delete_many({'nickname': self.
                                    update.effective_user.username})
        simple_action(self.update)
        self.update.message.text = 'last'
        simple_action(self.update)
        for line in self.collection.find().sort(
                '_id', pymongo.DESCENDING).limit(1):
            print(line)
            last = line
        self.assertEqual(last['message'], 'last')

    def test_log_func_func_name(self):
        simple_action(self.update)
        for line in self.collection.find().sort(
                '_id', pymongo.DESCENDING).limit(1):
            last = line
        self.assertEqual(last['funcname'], 'simple_action')

    def test_log_func_date(self):
        simple_action(self.update)
        line = list(self.collection.find().sort(
                '_id', pymongo.DESCENDING).limit(1))[0]
        self.assertEqual(line['date'][:4],
                         str(datetime.datetime.now().year))

    def test_log_func_except(self):
        self.assertRaises(BaseException, simple_action(self.update))

    def test_history_1(self):
        self.collection.delete_many({'nickname': self.
                                    update.effective_user.username})
        simple_action(self.update)
        simple_action(self.update)
        simple_action(self.update)
        simple_action(self.update)
        simple_action(self.update)
        self.assertEqual(logger.last_5_history(self.update)
                         .split('\n')[1], 'testing')

    def test_history_2(self):
        self.collection.delete_many({'nickname': self.
                                    update.effective_user.username})
        simple_action(self.update)
        self.assertEqual(len(logger.last_5_history(self.update)
                             .split()), 2)

    def test_history_3(self):
        simple_action(self.update)
        self.update_tyler = mock.MagicMock()
        self.update_tyler.message.text = 'nothing'
        self.update_tyler.effective_user.username = 'Tyler Durden'
        self.update_tyler.effective_user.first_name = 'Tyler'
        self.update_tyler.effective_user.last_name = None
        self.collection.delete_many({'nickname': self.
                                    update_tyler.effective_user.username})
        simple_action(self.update_tyler)
        simple_action(self.update_tyler)
        simple_action(self.update_tyler)
        self.assertEqual(len(logger.last_5_history(self.
                                                   update_tyler).split()), 4)

    def test_history_4(self):
        simple_action(self.update)
        self.update_tyler = mock.MagicMock()
        self.update_tyler.message.text = 'nothing'
        self.update_tyler.effective_user.username = 'Tyler Durden'
        self.update_tyler.effective_user.first_name = 'Tyler'
        self.update_tyler.effective_user.last_name = None
        self.collection.delete_many({'nickname': self.
                                    update_tyler.effective_user.username})
        simple_action(self.update_tyler)
        simple_action(self.update_tyler)
        simple_action(self.update_tyler)
        self.assertEqual(len(logger.last_5_history(
            self.update_tyler).split()), 4)

    def test_history_5(self):
        logger.log = []
        simple_action(self.update)
        self.update.effective_user.username = 'Tyler Durden'


if __name__ == '__main__':
    unittest.main()
