#!/usr/bin/env python3
# Tests repository-level automation that keeps review-with-multi-debate synced from its standalone upstream.

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SUBMODULE = "review-with-multi-debate"
SYNC_SCRIPT = REPO_ROOT / "scripts" / "sync_review_with_multi_debate_submodule.sh"
SYNC_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "sync-review-with-multi-debate.yml"


def gitmodules_value(key: str) -> str:
    result = subprocess.run(
        ["git", "config", "-f", ".gitmodules", "--get", key],
        cwd=REPO_ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip()


class SubmoduleSyncConfigTest(unittest.TestCase):
    def test_review_submodule_tracks_main_branch(self) -> None:
        self.assertEqual(
            gitmodules_value(f"submodule.{SUBMODULE}.url"),
            "https://github.com/linmou/review-with-multi-debate.git",
        )
        self.assertEqual(gitmodules_value(f"submodule.{SUBMODULE}.branch"), "main")

    def test_sync_script_updates_only_review_submodule(self) -> None:
        script = SYNC_SCRIPT.read_text(encoding="utf-8")

        self.assertTrue(script.startswith("#!/usr/bin/env bash\n"))
        self.assertIn("# Purpose:", script.splitlines()[1])
        self.assertIn(f"git submodule update --init {SUBMODULE}", script)
        self.assertIn(f"git submodule update --remote --merge {SUBMODULE}", script)
        self.assertNotIn("git submodule update --remote --merge\n", script)

    def test_github_workflow_commits_review_pointer_update(self) -> None:
        workflow = SYNC_WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("schedule:", workflow)
        self.assertIn("contents: write", workflow)
        self.assertIn("scripts/sync_review_with_multi_debate_submodule.sh", workflow)
        self.assertIn(f"git diff --quiet -- {SUBMODULE}", workflow)
        self.assertIn(f"git add {SUBMODULE}", workflow)
        self.assertNotIn("git add .", workflow)


if __name__ == "__main__":
    unittest.main()
