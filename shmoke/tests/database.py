import unittest

import requests

import enchant


class DatabaseTestCase(unittest.TestCase):
    def test_database_system(self):
        db = enchant.database("123456789123456789")
        test = self.assertTrue(db.new())
        test2 = self.assertTrue(db.set("message_log", True))
        test3 = self.assertTrue(db.set("mod_log", True))
        test4 = self.assertTrue(db.set("profanity_filter", True))
        test5 = self.assertTrue(db.set("spam_filter", True))
        test6 = self.assertTrue(db.set("prefix", "!"))
        test7 = self.assertTrue(db.delete())
        return f"{test}, {test2}, {test3}, {test4}, {test5}, {test6}, {test7}"
