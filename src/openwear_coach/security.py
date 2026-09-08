"""Security checks for the local OpenWear Coach transport."""

from __future__ import annotations

from ipaddress import ip_address


def require_loopback_host(value: str) -> str:
    """Return a normalized loopback IP or reject network exposure.

    OpenWear's local server has no network authentication yet. Hostnames are
    intentionally rejected so a hosts-file or DNS change cannot widen the
    listener beyond the local machine.
    """

    candidate = value.strip()
    try:
        address = ip_address(candidate)
    except ValueError as exc:
        raise ValueError(
            "OPENWEAR_HOST must be a numeric loopback address such as 127.0.0.1"
        ) from exc
    if not address.is_loopback:
        raise ValueError(
            "OpenWear refuses non-loopback serving without authentication"
        )
    return address.compressed


def require_tcp_port(value: str) -> int:
    """Parse a valid, non-privileged TCP port."""

    try:
        port = int(value)
    except ValueError as exc:
        raise ValueError("OPENWEAR_PORT must be an integer") from exc
    if not 1024 <= port <= 65535:
        raise ValueError("OPENWEAR_PORT must be between 1024 and 65535")
    return port


def require_local_transport(value: str) -> str:
    """Allow only the two local transports supported by this application."""

    transport = value.strip().lower()
    if transport not in {"stdio", "streamable-http"}:
        raise ValueError("OPENWEAR_TRANSPORT must be stdio or streamable-http")
    return transport
