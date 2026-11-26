"""Covers ultlib.audio through the CLI: the sound credits log and the local mix."""
import json
import shutil
import subprocess
import unittest

from _harness import UltCase

HAS_FFMPEG = bool(shutil.which("ffmpeg") and shutil.which("ffprobe"))


class TestAudioCredits(UltCase):
    def test_add_then_check_flags_non_commercial_and_unlogged(self):
        self.assertEqual(self.ult("audio", "credits", "add", "bed.mp3", "--source", "https://x.test/bed",
                                  "--licence", "CC BY-NC 4.0", "--author", "Ana").code, 0)
        self.assertEqual(self.ult("audio", "credits", "add", "vo.mp3", "--source", "ElevenLabs",
                                  "--licence", "ElevenLabs paid plan").code, 0)
        self.assertEqual(self.ult("audio", "credits", "add", "vo.mp3", "--source", "x", "--licence", "CC0").code, 1)
        self.write("media/audio/vo.mp3", "x")
        self.write("media/audio/whoosh.wav", "x")
        r = self.ult("audio", "credits", "check", "--dir", "media/audio", "--json")
        self.assertEqual(r.code, 1, r.all)
        data = json.loads(r.out)
        self.assertEqual(data["rows"], 2)
        texts = [p["text"] for p in data["problems"]]
        self.assertTrue(any("bed.mp3: 'CC BY-NC 4.0' reads as non-commercial" in t for t in texts), texts)
        self.assertTrue(any("credit owed to Ana" in t for t in texts), texts)
        self.assertTrue(any("whoosh.wav: used but not in" in t for t in texts), texts)
        self.assertFalse(any(t.startswith("vo.mp3") for t in texts), texts)

    def test_reads_older_table_and_paid_ad_use(self):
        self.write("brand/sound-credits.md", "# Credits\n\n| File | Source URL | Author | Licence | Credit needed | Used in |\n"
                   "|---|---|---|---|---|---|\n| whoosh.ogg | https://k.test | Kenney | CC0 | no | launch |\n"
                   "| song.mp3 | https://lib.test | Lib | personal licence | no | ad |\n")
        r = self.ult("audio", "credits", "check", "--use", "paid-ad")
        self.assertEqual(r.code, 1, r.all)
        self.assertIn("2 rows", r.out)
        self.assertIn("song.mp3: 'personal licence' may not cover paid", r.out)
        self.assertNotIn("whoosh.ogg", r.out)

    def test_empty_log_says_how_to_start(self):
        r = self.ult("audio", "credits", "check")
        self.assertEqual(r.code, 0)
        self.assertIn("ult audio credits add", r.out)


@unittest.skipUnless(HAS_FFMPEG, "needs ffmpeg")
class TestAudioMix(UltCase):
    def _gen(self, name, src):
        subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "lavfi", "-i", src, str(self.root / name)],
                       check=True)

    def test_mix_hits_target_loudness(self):
        self._gen("vo.wav", "sine=f=300:d=3,volume=0.5")
        self._gen("mu.wav", "anoisesrc=d=2:a=0.3")
        r = self.ult("audio", "mix", "vo.wav", "mu.wav", "--out", "out/mix.m4a", "--loop", timeout=300)
        self.assertEqual(r.code, 0, r.all)
        self.assertIn("-> pass", r.out)
        self.assertTrue((self.root / "out" / "mix.m4a").is_file())
        self.assertFalse((self.root / "out" / "mix-premix.wav").exists())

    def test_missing_input(self):
        self.assertEqual(self.ult("audio", "mix", "no.wav", "no2.wav", "--out", "x.m4a").code, 2)


if __name__ == "__main__":
    unittest.main()
