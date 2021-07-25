import unittest
import enchant


class DatabaseTestCase(unittest.TestCase):
    def test_something(self):
        db = enchant.database("862786056834121798")
        self.assertTrue(db.new())
        self.assertTrue(db.set("message_log", True))
        self.assertTrue(db.set("mod_log", True))
        self.assertTrue(db.set("profanity_filter", True))
        self.assertTrue(db.set("spam_filter", True))
        self.assertTrue(db.set("prefix", "!"))
        self.assertTrue(db.delete())


unittest.main()
