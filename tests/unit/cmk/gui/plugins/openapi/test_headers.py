#!/usr/bin/env python3
# Copyright (C) 2023 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from webtest import TestResponse  # type: ignore[import]

from tests.unit.cmk.gui.conftest import WebTestAppForCMK

import cmk.utils.version as cmk_version


def _get_version(app: WebTestAppForCMK, status: int = 200) -> TestResponse:
    return app.call_method(
        "get",
        "/NO_SITE/check_mk/api/1.0/version",
        headers={
            "Accept": "application/json",
        },
        status=status,
    )


def test_headers_exposed(
    aut_user_auth_wsgi_app: WebTestAppForCMK,
) -> None:
    resp = _get_version(
        aut_user_auth_wsgi_app,
    )
    assert resp.headers["x-checkmk-edition"] == cmk_version.edition().short
    assert resp.headers["x-checkmk-version"] == cmk_version.__version__


def test_headers_not_exposed_for_unauthorized_users(wsgi_app: WebTestAppForCMK) -> None:
    resp = _get_version(
        wsgi_app,
        status=401,
    )
    assert "x-checkmk-edition" not in resp.headers
    assert "x-checkmk-version" not in resp.headers
