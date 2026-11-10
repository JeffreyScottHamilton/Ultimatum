import unittest
from ratelimit.bucket import TokenBucket


class Clock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


class BucketTests(unittest.TestCase):
    def test_burst_then_deny(self):
        b = TokenBucket(1, 3, Clock())
        self.assertEqual([b.take() for _ in range(4)], [True, True, True, False])

    def test_refill(self):
        c = Clock()
        b = TokenBucket(2, 4, c)
        for _ in range(4):
            b.take()
        c.t = 1.0
        self.assertTrue(b.take(2))
        self.assertFalse(b.take())

    def test_capped(self):
        c = Clock()
        b = TokenBucket(10, 2, c)
        c.t = 100
        self.assertTrue(b.take(2))
        self.assertFalse(b.take())
