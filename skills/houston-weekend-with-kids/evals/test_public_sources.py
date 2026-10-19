"""Deterministic source-boundary tests; all content below is synthetic public fixture data."""

import argparse
from contextlib import redirect_stdout
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch


SPEC = importlib.util.spec_from_file_location("public_sources", Path(__file__).resolve().parents[1] / "scripts" / "public_sources.py")
SOURCES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCES)


class PublicSourcesTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="houston-public-fixture-")
        self.root = Path(self.temporary.name).resolve()
        self.source = {"id": "space-guide", "url": "https://spacecenter.org/visitor-information/guide/", "publisher": "Synthetic fixture", "title": "Fixture planning page", "markers": ["hours", "Tram"]}
        self.catalog = self.root / "assets" / "source-catalog.json"
        self.catalog.parent.mkdir()
        self.catalog.write_text(json.dumps({"sources": [self.source]}), encoding="utf-8")
        self.patches = [patch.object(SOURCES, "ROOT", self.root), patch.object(SOURCES, "CORPUS", self.root / "corpus"), patch.object(SOURCES, "CATALOG", self.catalog), patch.object(SOURCES.time, "sleep")]
        for item in self.patches:
            item.start()
        self.addCleanup(self.temporary.cleanup)
        for item in self.patches:
            self.addCleanup(item.stop)

    def args(self, **overrides):
        return argparse.Namespace(source=None, refresh=True, check=False, dry_run=False, verbose=False, quiet=False, **overrides)

    def save_fixture(self):
        with patch.object(SOURCES, "fetch", return_value=(b"<html>synthetic original</html>", b"synthetic searchable text\n", self.source["url"])):
            result, code = SOURCES.run_operation(self.args())
        self.assertEqual(code, 0)
        self.assertTrue(result["ok"])

    def test_unknown_id_does_not_echo_or_act(self):
        with patch.object(SOURCES, "fetch") as fetch:
            args = self.args()
            args.source = ["unapproved-input"]
            result, code = SOURCES.run_operation(args)
        self.assertEqual(code, 2)
        self.assertNotIn("unapproved-input", json.dumps(result))
        fetch.assert_not_called()
        self.assertFalse((self.root / "corpus").exists())

    def test_dry_run_makes_no_network_or_files(self):
        args = self.args()
        args.dry_run = True
        with patch.object(SOURCES, "fetch") as fetch:
            result, code = SOURCES.run_operation(args)
        self.assertEqual(code, 0)
        self.assertFalse(result["network"])
        fetch.assert_not_called()
        self.assertFalse((self.root / "corpus").exists())

    def test_local_check_detects_changed_original_without_mutation(self):
        self.save_fixture()
        original = self.root / "corpus" / "sources" / "space-guide.html"
        original.write_bytes(b"intentionally altered fixture")
        inventory = self.root / "corpus" / "inventory.json"
        before = inventory.read_bytes()
        args = self.args()
        args.refresh, args.check = False, True
        with patch.object(SOURCES, "fetch") as fetch:
            result, code = SOURCES.run_operation(args)
        self.assertEqual(code, 1)
        self.assertEqual(result["sources"][0]["status"], "failed")
        self.assertEqual(before, inventory.read_bytes())
        fetch.assert_not_called()

    def test_failed_refresh_retains_good_bytes_and_marks_failure(self):
        self.save_fixture()
        original = self.root / "corpus" / "sources" / "space-guide.html"
        before = original.read_bytes()
        with patch.object(SOURCES, "fetch", side_effect=SOURCES.SourceError("HTTP 503; retry later.")):
            result, code = SOURCES.run_operation(self.args())
        self.assertEqual(code, 1)
        self.assertFalse(result["ok"])
        self.assertEqual(original.read_bytes(), before)
        inventory = json.loads((self.root / "corpus" / "inventory.json").read_text())
        self.assertEqual(inventory["sources"]["space-guide"]["status"], "failed")
        with patch.object(SOURCES, "fetch", return_value=(before, b"synthetic searchable text\n", self.source["url"])):
            recovered, code = SOURCES.run_operation(self.args())
        self.assertEqual(code, 0)
        self.assertTrue(recovered["ok"])

    def test_repeated_refresh_uses_same_owned_paths(self):
        self.save_fixture()
        before = sorted(path.relative_to(self.root) for path in self.root.rglob("*") if path.is_file())
        self.save_fixture()
        self.assertEqual(before, sorted(path.relative_to(self.root) for path in self.root.rglob("*") if path.is_file()))

    def test_url_boundary_rejects_query_credentials_port_and_other_host(self):
        urls = ["https://spacecenter.org/?private=value", "https://user:pass@spacecenter.org/", "https://spacecenter.org:444/", "https://example.com/", "http://spacecenter.org/", "https://spacecenter.org/#fragment"]
        for url in urls:
            with self.subTest(url=url), self.assertRaises(SOURCES.SourceError):
                SOURCES.validate_url(url)
        with self.assertRaises(SOURCES.SourceError):
            SOURCES.validate_url("https://www.cmhouston.org/plan-a-visit", "spacecenter.org")

    def test_atomic_write_rejects_path_outside_owned_root(self):
        with tempfile.TemporaryDirectory(prefix="houston-outside-fixture-") as outside:
            path = Path(outside) / "unowned.txt"
            with self.assertRaises(SOURCES.SourceError):
                SOURCES.atomic_write(path, b"fixture")
            self.assertFalse(path.exists())

    def test_visible_text_excludes_scripts_and_preserves_cells(self):
        parser = SOURCES.PageText()
        parser.feed("<html><script>untrusted fixture script</script><main><h1>Hours</h1><table><tr><td>Sunday</td><td>9–5</td></tr></table></main></html>")
        text = parser.text()
        self.assertNotIn("untrusted", text)
        self.assertIn("Sunday\n9–5", text)

    def test_missing_inventory_is_failure_without_network(self):
        args = self.args()
        args.refresh, args.check = False, True
        with patch.object(SOURCES, "fetch") as fetch:
            result, code = SOURCES.run_operation(args)
        self.assertEqual(code, 1)
        self.assertFalse(result["ok"])
        fetch.assert_not_called()

    def test_json_mode_contains_one_object_without_banner(self):
        stream = io.StringIO()
        with patch.object(SOURCES.sys, "argv", ["public_sources.py", "--refresh", "--dry-run", "--json", "--no-input"]), redirect_stdout(stream):
            code = SOURCES.main()
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(stream.getvalue())["ok"])
        self.assertNotIn("\033", stream.getvalue())

    def test_competing_subset_refresh_refuses_without_lost_metadata(self):
        self.save_fixture()
        second = {**self.source, "id": "second-source"}
        self.catalog.write_text(json.dumps({"sources": [self.source, second]}), encoding="utf-8")
        inventory = self.root / "corpus" / "inventory.json"
        before = inventory.read_bytes()
        args = self.args()
        args.source = ["second-source"]
        with SOURCES.refresh_lock():
            lock = self.root / "corpus" / ".refresh.lock"
            self.assertTrue(lock.exists())
            with patch.object(SOURCES, "fetch") as fetch:
                with self.assertRaisesRegex(SOURCES.SourceError, "Another refresh"):
                    SOURCES.run_operation(args)
            fetch.assert_not_called()
            self.assertEqual(inventory.read_bytes(), before)
            self.assertTrue(lock.exists())
        self.assertFalse(lock.exists())
        with patch.object(SOURCES, "fetch", return_value=(b"<html>second synthetic original</html>", b"second synthetic text\n", second["url"])):
            result, code = SOURCES.run_operation(args)
        self.assertEqual(code, 0)
        entries = json.loads(inventory.read_text())["sources"]
        self.assertEqual(set(entries), {"space-guide", "second-source"})
        self.assertTrue(result["ok"])

    def test_check_preview_and_help_do_not_take_or_change_existing_lock(self):
        self.save_fixture()
        lock = self.root / "corpus" / ".refresh.lock"
        lock.write_bytes(b"synthetic existing owner")
        args = self.args()
        args.refresh, args.check = False, True
        self.assertEqual(SOURCES.run_operation(args)[1], 0)
        args.refresh, args.check, args.dry_run = True, False, True
        self.assertEqual(SOURCES.run_operation(args)[1], 0)
        with patch.object(SOURCES, "refresh_lock") as locked, redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as exit_result:
            SOURCES.build_parser().parse_args(["--help"])
        self.assertEqual(exit_result.exception.code, 0)
        locked.assert_not_called()
        self.assertEqual(lock.read_bytes(), b"synthetic existing owner")

    def test_owned_lock_cleaned_after_interrupt(self):
        with patch.object(SOURCES, "fetch", side_effect=KeyboardInterrupt):
            with self.assertRaises(KeyboardInterrupt):
                SOURCES.run_operation(self.args())
        self.assertFalse((self.root / "corpus" / ".refresh.lock").exists())

    def test_main_reports_lock_contention_without_exposing_lock_contents(self):
        lock = self.root / "corpus" / ".refresh.lock"
        lock.parent.mkdir()
        lock.write_bytes(b"synthetic other writer")
        output = io.StringIO()
        with patch.object(SOURCES.sys, "argv", ["public_sources.py", "--refresh", "--json", "--no-input"]), redirect_stdout(output), patch.object(SOURCES, "fetch") as fetch:
            code = SOURCES.main()
        self.assertEqual(code, 1)
        self.assertIn("corpus lock", json.loads(output.getvalue())["error"]["message"])
        self.assertNotIn("synthetic other writer", output.getvalue())
        self.assertTrue(lock.exists())
        fetch.assert_not_called()

    def test_lock_replacement_is_preserved(self):
        with SOURCES.refresh_lock():
            lock = self.root / "corpus" / ".refresh.lock"
            lock.unlink()
            lock.write_bytes(b"synthetic replacement owner")
        self.assertEqual(lock.read_bytes(), b"synthetic replacement owner")


if __name__ == "__main__":
    unittest.main()
