import sys
import re
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trrc.utils import AnkiConnectInfo
import pytest

@pytest.mark.parametrize("ip, ip_answer",
                         [('localhost', 'localhost'),
                          ('192.1.1.123', '192.1.1.123'),
                          ('http://192.1.1.123', '192.1.1.123'),
                          ('https://192.1.1.123', '192.1.1.123')],)
@pytest.mark.parametrize("port",
                         [123],)
@pytest.mark.parametrize("apikey",
                         ['password'],)
def test_get_default_get_ankiconnect_url(ip: str, ip_answer, port, apikey):

    protocol = 'https' if ip.startswith('https://') else 'http'

    ankiconnect_info = AnkiConnectInfo(ip, port, apikey)
    assert ankiconnect_info.ip == ip_answer
    assert ankiconnect_info.port == port
    assert ankiconnect_info.protocol == protocol
    assert ankiconnect_info.url == f'{protocol}://{ip_answer}:{port}'
    assert ankiconnect_info.apikey == apikey
