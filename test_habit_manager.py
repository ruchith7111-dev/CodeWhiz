"""Unit tests for CodeWhiz core operations and storage. Run: python -m unittest -v"""
import os
import tempfile
import unittest

import habit_manager as hm
import reports
from data_store import load_data, save_data, empty_store


class TestHabitManager(unittest.TestCase):
    def setUp(self):
        self.data = empty_store()

    def test_add_assigns_sequential_ids(self):
        a = hm.add_entry(self.data, "Python", "DSA", 1.5, "lists")
        b = hm.add_entry(self.data, "Java", "Web", 2)
        self.assertEqual((a["id"], b["id"]), (1, 2))
        self.assertEqual(self.data["next_id"], 3)
        self.assertEqual(b["hours"], 2.0)

    def test_add_rejects_negative_hours(self):
        with self.assertRaises(ValueError):
            hm.add_entry(self.data, "Python", "DSA", -1)

    def test_update_changes_fields(self):
        hm.add_entry(self.data, "Python", "DSA", 1)
        self.assertTrue(hm.update_entry(self.data, 1, hours=3, notes="revised"))
        entry = hm.get_entry(self.data, 1)
        self.assertEqual(entry["hours"], 3.0)
        self.assertEqual(entry["notes"], "revised")

    def test_update_skips_blank_values(self):
        hm.add_entry(self.data, "Python", "DSA", 1, "keep")
        hm.update_entry(self.data, 1, language="", notes="")
        entry = hm.get_entry(self.data, 1)
        self.assertEqual(entry["language"], "Python")
        self.assertEqual(entry["notes"], "keep")

    def test_update_missing_returns_false(self):
        self.assertFalse(hm.update_entry(self.data, 99, hours=2))

    def test_delete(self):
        hm.add_entry(self.data, "Python", "DSA", 1)
        self.assertTrue(hm.delete_entry(self.data, 1))
        self.assertFalse(hm.delete_entry(self.data, 1))
        self.assertEqual(self.data["entries"], [])

    def test_filter_by_category_and_language(self):
        hm.add_entry(self.data, "Python", "DSA", 1)
        hm.add_entry(self.data, "java", "Web", 1)
        hm.add_entry(self.data, "Python", "Web", 1)
        self.assertEqual(len(hm.filter_entries(self.data, category="Web")), 2)
        self.assertEqual(len(hm.filter_entries(self.data, language="PYTHON")), 2)
        self.assertEqual(len(hm.filter_entries(self.data, category="Web", language="java")), 1)


class TestReports(unittest.TestCase):
    def test_summary_totals(self):
        data = empty_store()
        hm.add_entry(data, "Python", "DSA", 3)
        hm.add_entry(data, "Python", "DSA", 2.5)
        hm.add_entry(data, "Java", "Web", 2)
        total, per_cat = reports.summary(data["entries"])
        self.assertEqual(total, 7.5)
        self.assertEqual(per_cat, {"DSA": 5.5, "Web": 2.0})


class TestStorage(unittest.TestCase):
    def test_round_trip(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "data.json")
            data = empty_store()
            hm.add_entry(data, "Python", "DSA", 1.25, "round trip")
            save_data(data, path)
            loaded = load_data(path)
            self.assertEqual(loaded["entries"], data["entries"])
            self.assertEqual(loaded["next_id"], 2)

    def test_missing_file_gives_empty_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(load_data(os.path.join(tmp, "none.json")), empty_store())

    def test_corrupted_file_gives_empty_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "bad.json")
            with open(path, "w", encoding="utf-8") as f:
                f.write("{not json")
            self.assertEqual(load_data(path), empty_store())


if __name__ == "__main__":
    unittest.main()
