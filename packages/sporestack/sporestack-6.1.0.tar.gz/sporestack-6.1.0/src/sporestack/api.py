"""

SporeStack API request/response models

"""


from typing import List, Optional

from pydantic import BaseModel

from .models import Flavor, NetworkInterface, Payment

LATEST_API_VERSION = 3


class TokenAdd:
    url = "/token/{token}/add"
    method = "POST"

    class Request(BaseModel):
        currency: str
        dollars: int
        affiliate_token: Optional[str] = None

    class Response(BaseModel):
        token: str
        payment: Payment


class TokenBalance:
    url = "/token/{token}/balance"
    method = "GET"

    class Response(BaseModel):
        token: str
        cents: int
        usd: str


class ServerLaunch:
    url = "/server/{machine_id}/launch"
    method = "POST"

    class Request(BaseModel):
        machine_id: str
        days: int
        flavor: str
        ssh_key: str
        operating_system: str
        currency: Optional[str] = None
        """Currency only needs to be set if not paying with a token."""
        region: Optional[str] = None
        """null is automatic, otherwise a string region slug."""
        organization: Optional[str] = None
        """Deprecated and ignored, don't use this."""
        token: Optional[str] = None
        """Token to draw from when launching the server."""
        quote: bool = False
        """Don't launch, get a quote on how muchi t would cost"""
        affiliate_token: Optional[str] = None
        affiliate_amount: None = None
        """Deprecated field"""
        settlement_token: Optional[str] = None
        """Deprecated field. Use token instead."""
        hostname: str = ""
        """Hostname to refer to your server by."""

    class Response(BaseModel):
        payment: Payment
        """Deprecated, not needed when paying with token."""
        expiration: int
        machine_id: str
        flavor: str
        """Deprecated, use ServerInfo instead."""
        network_interfaces: List[NetworkInterface] = []
        """Deprecated, use ipv4/ipv6 from ServerInfo instead."""
        created_at: int = 0
        region: Optional[str] = None
        """Deprecated, use ServerInfo instead."""
        latest_api_version: int = LATEST_API_VERSION
        created: bool = False
        paid: bool = False
        """Deprecated, not needed when paying with token."""
        warning: Optional[str] = None
        txid: Optional[str] = None
        """Deprecated."""


class ServerTopup:
    url = "/server/{machine_id}/topup"
    method = "POST"

    class Request(BaseModel):
        machine_id: str
        days: int
        token: Optional[str] = None
        quote: bool = False
        currency: Optional[str] = None
        """Currency only needs to be set if not paying with a token."""
        affiliate_token: Optional[str] = None
        affiliate_amount: None = None
        """Deprecated field"""
        settlement_token: Optional[str] = None
        """Deprecated field. Use token instead."""

    class Response(BaseModel):
        machine_id: str
        payment: Payment
        """Deprecated, not needed when paying with token."""
        expiration: int
        paid: bool = False
        """Deprecated, not needed when paying with token."""
        warning: Optional[str] = None
        txid: Optional[str] = None
        """Deprecated."""
        latest_api_version: int = LATEST_API_VERSION


class ServerInfo:
    url = "/server/{machine_id}/info"
    method = "GET"

    class Response(BaseModel):
        created_at: int
        expiration: int
        running: bool
        machine_id: str
        ipv4: str
        ipv6: str
        region: str
        flavor: Flavor
        deleted: bool
        network_interfaces: List[NetworkInterface]
        """Deprecated, use ipv4/ipv6 instead."""
        operating_system: str
        hostname: str


class ServerStart:
    url = "/server/{machine_id}/start"
    method = "POST"


class ServerStop:
    url = "/server/{machine_id}/stop"
    method = "POST"


class ServerDelete:
    url = "/server/{machine_id}/delete"
    method = "POST"


class ServerRebuild:
    url = "/server/{machine_id}/rebuild"
    method = "POST"


class ServersLaunchedFromToken:
    url = "/token/{token}/servers"
    method = "GET"

    class Response(BaseModel):
        servers: List[ServerInfo.Response]


class Flavors:
    url = "/flavors"
    method = "GET"

    class Response(BaseModel):
        flavors: dict[str, Flavor]
