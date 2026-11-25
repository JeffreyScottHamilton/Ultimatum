import unittest

from taskboard import db, notify, queries, session


class BasicTests(unittest.TestCase):
    def test_list_sorted(self):
        db.add_task("p", "b", "ann", "2030-01-02")
        db.add_task("p", "a", "bob", "2030-01-01")
        self.assertEqual([t["title"] for t in queries.list_tasks("p", sort="title")], ["a", "b"])
        self.assertEqual(queries.list_tasks("p", sort="id; DROP TABLE tasks")[0]["title"], "b")

    def test_session_roundtrip(self):
        self.assertEqual(session.load_session(session.dump_session({"u": "ann"})), {"u": "ann"})

    def test_sign(self):
        self.assertTrue(notify.verify("x", notify.sign("x")))


if __name__ == "__main__":
    unittest.main()
