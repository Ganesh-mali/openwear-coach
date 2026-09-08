"""Exercise the actual STDIO entry point using synthetic, temporary storage."""

import sys
import tempfile
import unittest
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPIntegrationTests(unittest.IsolatedAsyncioTestCase):
    async def test_stdio_import_read_and_reject_invalid_strength(self):
        with tempfile.TemporaryDirectory() as directory:
            parameters = StdioServerParameters(
                command=sys.executable,
                args=["-m", "openwear_coach.server"],
                env={"OPENWEAR_DB": str(Path(directory) / "test.db"), "OPENWEAR_TRANSPORT": "stdio"},
            )
            async with stdio_client(parameters) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    self.assertEqual(len(tools.tools), 9)
                    result = await session.call_tool("import_health_csv", {
                        "csv_text": "date,metric,value,unit\n2026-09-01,sleep_hours,8,h\n",
                        "source": "synthetic_test",
                    })
                    self.assertFalse(result.is_error)
                    result = await session.call_tool("get_daily_readiness", {
                        "on_date": "2026-09-01", "source": "synthetic_test",
                    })
                    self.assertFalse(result.is_error)
                    result = await session.call_tool("record_strength_session", {
                        "session_date": "2026-09-01", "session_id": "test",
                        "sets": [{"exercise": "squat", "reps": 5.5, "weight_kg": 80}],
                    })
                    self.assertTrue(result.is_error)
                    result = await session.call_tool("get_data_coverage", {})
                    self.assertEqual(result.structured_content["health"]["records"], 1)
                    self.assertEqual(result.structured_content["strength"]["sets"], 0)
