from __future__ import annotations

import pytest
from app.utils.url_security import assert_safe_url


@pytest.mark.parametrize("url", ["http://localhost/video.mp4", "http://127.0.0.1/a.mp4"])
def test_url_security_blocks_private_hosts(url: str) -> None:
    with pytest.raises(ValueError):
        assert_safe_url(url)
