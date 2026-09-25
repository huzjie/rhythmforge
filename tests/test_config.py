# -*- coding: utf-8 -*-
import os
import tempfile
import unittest

from rhythmforge.config import load_config, default_config
from rhythmforge.utils.yamlish import parse_yaml


class TestConfig(unittest.TestCase):
    def test_default(self):
        cfg = default_config()
        self.assertEqual(cfg.backend.kind, "mock")

    def test_yaml_parse(self):
        data = parse_yaml("backend:\n  skill: 0.7\nengine:\n  mode: sample\n")
        self.assertEqual(data["backend"]["skill"], 0.7)
        self.assertEqual(data["engine"]["mode"], "sample")

    def test_load_yaml_file(self):
        fd, path = tempfile.mkstemp(suffix=".yaml")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            f.write("backend:\n  skill: 0.9\n")
        cfg = load_config(path)
        os.remove(path)
        self.assertEqual(cfg.backend.skill, 0.9)

    def test_load_json_file(self):
        fd, path = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        with open(path, "w", encoding="utf-8") as f:
            f.write('{"backend": {"kind": "mock", "skill": 0.3}}')
        cfg = load_config(path)
        os.remove(path)
        self.assertEqual(cfg.backend.skill, 0.3)


if __name__ == "__main__":
    unittest.main()
