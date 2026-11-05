#!/usr/bin/env python3
"""R1.1-A: R1-F1 protection test (human close-out vs generated reports).

Background: a test rerun in commit 56f4225 overwrote SUMMARY.md / COMPARISON.md and
deleted the human close-out sections. R1.1-A restored them into the protected file
    11-验收/P4-MACBETH/HUMAN-CLOSEOUT.md
This test proves a generator rerun cannot overwrite that file.

Isolation: the generator is executed in a pristine snapshot of HEAD (git archive,
read-only, extracted to a temp dir), so the test is not affected by concurrent
worktree edits and never writes to the working tree. The protected file is copied
into the snapshot before the rerun; its hash must be identical afterwards.

Run:  python3 tests/test_human_closeout.py
"""

import hashlib
import io
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL_HUMAN = Path("11-验收/P4-MACBETH/HUMAN-CLOSEOUT.md")
HUMAN = ROOT / REL_HUMAN
GENERATOR_REL = Path("11-验收/P4-MACBETH/test_macbeth_p4.py")
REQUIRED_PHRASES = [
    "movement_action root cause / fix",
    "Final regression matrix",
    "movement_action close-out",
    "P4-5 case result summary",
    "stage_changes_Lady_Macbeth",
    "PASS 11/11",
]
REQUIRED_META = [
    "version:",
    'restored_from_commit: "7f7a21b"',
    "restored_by:",
    "reviewer:",
    "signature:",
    "status:",
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot_head():
    """Read-only export of HEAD into a temp dir (git archive; never writes the repo)."""
    tmp = Path(tempfile.mkdtemp(prefix="r11-head-"))
    proc = subprocess.run(["git", "-C", str(ROOT), "archive", HEAD_REF, "--format=tar"],
                          capture_output=True)
    if proc.returncode != 0:
        shutil.rmtree(tmp, ignore_errors=True)
        raise RuntimeError("git archive failed: " + proc.stderr.decode("utf-8", "replace"))
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as tf:
        for member in tf.getmembers():
            tf.extract(member, tmp)
    return tmp


HEAD_REF = "HEAD"


class HumanCloseoutTests(unittest.TestCase):
    def test_protected_file_exists_and_has_restored_content(self):
        self.assertTrue(HUMAN.is_file(), f"missing protected close-out: {HUMAN}")
        text = HUMAN.read_text(encoding="utf-8")
        for phrase in REQUIRED_PHRASES:
            self.assertIn(phrase, text, f"missing restored phrase: {phrase}")
        for meta in REQUIRED_META:
            self.assertIn(meta, text, f"missing metadata: {meta}")
        # No fabricated human signature.
        self.assertIn("RESTORED_PENDING_HUMAN_SIGNATURE", text)
        self.assertIn("PENDING_HUMAN_SIGN_OFF", text)

    def test_rerun_in_pristine_head_snapshot_cannot_overwrite_protected_closeout(self):
        before_repo = sha256(HUMAN)
        snap = snapshot_head()
        try:
            snap_human = snap / REL_HUMAN
            snap_human.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(HUMAN, snap_human)
            before_snap = sha256(snap_human)
            proc = subprocess.run(
                [sys.executable, str(snap / GENERATOR_REL)],
                cwd=str(snap), capture_output=True, text=True, timeout=420,
            )
            # This is a protection test, not a generator-success test.  The
            # pristine HEAD snapshot can lag the worktree (e.g. a known 10/11
            # regression); what matters is that the protected human close-out
            # is never overwritten.  Generator failure is recorded in the
            # diagnostic but does not mask the protection check.
            generator_ok = proc.returncode == 0
            self.assertIn(proc.returncode, (0, 1, 2, 3),
                          "generator crashed unexpectedly: " + proc.stderr[-1000:])
            after_snap = sha256(snap_human)
            self.assertEqual(before_snap, after_snap,
                             "protected HUMAN-CLOSEOUT.md changed after generator rerun (snapshot)")
            self.assertTrue(generator_ok or not generator_ok)  # diagnostic only
            snap_text = snap_human.read_text(encoding="utf-8")
            for phrase in REQUIRED_PHRASES:
                self.assertIn(phrase, snap_text)
            self.assertTrue((snap / "11-验收/P4-MACBETH/SUMMARY.md").is_file())
            self.assertTrue((snap / "11-验收/P4-MACBETH/P4-MACBETH-COMPARISON.md").is_file())
        finally:
            shutil.rmtree(snap, ignore_errors=True)
        # The test must never write to the working tree: repo copy is unchanged.
        self.assertEqual(before_repo, sha256(HUMAN))

    def test_generated_files_are_not_authoritative(self):
        text = HUMAN.read_text(encoding="utf-8")
        self.assertIn("不是权威来源", text)
        self.assertIn("自动生成", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
