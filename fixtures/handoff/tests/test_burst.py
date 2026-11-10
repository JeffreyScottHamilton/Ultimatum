import unittest

from ratelimit import Limiter
from ratelimit.config import Config
from tests.test_bucket import Clock


class BurstOverrideTests(unittest.TestCase):
    def test_default_burst_when_no_override(self):
        lim = Limiter(rate=1, burst=3, clock=Clock())
        self.assertEqual([lim.allow("a") for _ in range(4)], [True, True, True, False])

    def test_override_does_not_affect_other_keys(self):
        cfg = Config(rate=1, burst=2, burst_overrides={"vip": 5})
        lim = Limiter(config=cfg, clock=Clock())
        self.assertEqual([lim.allow("normal") for _ in range(3)], [True, True, False])

    def test_burst_override_applies(self):
        cfg = Config(rate=1, burst=2, burst_overrides={"vip": 5})
        lim = Limiter(config=cfg, clock=Clock())
        self.assertEqual([lim.allow("vip") for _ in range(6)], [True] * 5 + [False])
