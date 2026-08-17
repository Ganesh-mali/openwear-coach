from __future__ import annotations

import unittest

from openwear_coach.security import (
    require_local_transport,
    require_loopback_host,
    require_tcp_port,
)


class ServerSecurityTests(unittest.TestCase):
    def test_accepts_ipv4_loopback(self) -> None:
        self.assertEqual(require_loopback_host("127.0.0.1"), "127.0.0.1")

    def test_accepts_ipv6_loopback(self) -> None:
        self.assertEqual(require_loopback_host("::1"), "::1")

    def test_rejects_lan_and_wildcard_addresses(self) -> None:
        for host in ("0.0.0.0", "192.168.1.10", "::"):
            with self.subTest(host=host), self.assertRaises(ValueError):
                require_loopback_host(host)

    def test_rejects_hostnames(self) -> None:
        with self.assertRaises(ValueError):
            require_loopback_host("localhost")

    def test_accepts_unprivileged_port(self) -> None:
        self.assertEqual(require_tcp_port("8000"), 8000)

    def test_rejects_invalid_or_privileged_ports(self) -> None:
        for port in ("not-a-port", "0", "80", "65536"):
            with self.subTest(port=port), self.assertRaises(ValueError):
                require_tcp_port(port)

    def test_accepts_only_supported_local_transports(self) -> None:
        self.assertEqual(require_local_transport("stdio"), "stdio")
        self.assertEqual(require_local_transport("streamable-http"), "streamable-http")
        for transport in ("sse", "websocket", ""):
            with self.subTest(transport=transport), self.assertRaises(ValueError):
                require_local_transport(transport)


if __name__ == "__main__":
    unittest.main()
