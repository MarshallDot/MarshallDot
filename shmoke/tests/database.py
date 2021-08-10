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

    def test_engine(self):
        reponse = requests.models.Response()
        reponse.status_code = 200
        test = self.assertIn(f"{reponse.status_code}",
                             str(requests.post("http://localhost:6006/", json={"id": "123456789123456789"})
                                 .status_code))
        test2 = self.assertIn(f"{reponse.status_code}",
                              str(requests.put("http://localhost:6006/", json={"id": "123456789123456789", "name": "message_log", "value": True})
                                  .status_code))
        test3 = self.assertIn(f"{reponse.status_code}",
                              str(requests.put("http://localhost:6006/", json={"id": "123456789123456789", "name": "mod_log", "value": True})
                                  .status_code))
        test4 = self.assertIn(f"{reponse.status_code}",
                              str(requests.put("http://localhost:6006/", json={"id": "123456789123456789", "name": "profanity_filter", "value": True})
                                  .status_code))
        test5 = self.assertIn(f"{reponse.status_code}",
                              str(requests.put("http://localhost:6006/", json={"id": "123456789123456789", "name": "spam_filter", "value": True})
                                  .status_code))
        test6 = self.assertIn(f"{reponse.status_code}",
                              str(requests.put("http://localhost:6006/", json={"id": "123456789123456789", "name": "prefix", "value": "!"})
                                  .status_code))
        test7 = self.assertIn(f"{reponse.status_code}",
                              str(requests.delete("http://localhost:6006/", json={"id": "123456789123456789"})
                                  .status_code))
