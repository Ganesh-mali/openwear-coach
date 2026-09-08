"""Static privacy/structure checks, not a substitute for iOS runtime testing."""
import importlib.util
import plistlib
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("shortcut_builder", ROOT / "shortcuts/build_shortcut.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class ShortcutTests(unittest.TestCase):
    def test_action_allowlist_and_copy_gate(self):
        actions = builder.build()["WFWorkflowActions"]
        allowed = {"alert", "gettext", "setvariable", "filter.health.quantity",
                   "repeat.each", "properties.health.quantity", "appendvariable",
                   "text.combine", "quicklook", "setclipboard"}
        for action in actions:
            self.assertIn(action["WFWorkflowActionIdentifier"].removeprefix("is.workflow.actions."), allowed)
        self.assertEqual(actions[-2]["WFWorkflowActionIdentifier"], "is.workflow.actions.alert")
        self.assertTrue(actions[-2]["WFWorkflowActionParameters"]["WFAlertActionCancelButtonShown"])
        self.assertTrue(actions[-1]["WFWorkflowActionParameters"]["WFLocalOnly"])

    def test_references_resolve_and_repeats_balance(self):
        actions = builder.build()["WFWorkflowActions"]
        seen, groups = set(), []
        def inspect(value):
            if isinstance(value, dict):
                if value.get("Type") == "ActionOutput":
                    self.assertIn(value["OutputUUID"], seen)
                for item in value.values(): inspect(item)
            elif isinstance(value, list):
                for item in value: inspect(item)
        for action in actions:
            params = action["WFWorkflowActionParameters"]
            inspect(params)
            self.assertNotIn(params["UUID"], seen)
            seen.add(params["UUID"])
            if action["WFWorkflowActionIdentifier"].endswith("repeat.each"):
                if params["WFControlFlowMode"] == 0:
                    groups.append(params["GroupingIdentifier"])
                else:
                    self.assertEqual(groups.pop(), params["GroupingIdentifier"])
        self.assertEqual(groups, [])

    def test_generated_source_matches_builder(self):
        actual = plistlib.loads((ROOT / "shortcuts/OpenWear Check-in.unsigned.plist").read_bytes())
        self.assertEqual(actual, builder.build())
        self.assertIn("NOT complete daily coverage", builder.HEADER)
