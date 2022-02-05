#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest


# common fixtures

@pytest.fixture
def start_coord() -> int:
    return 123


@pytest.fixture
def end_coord() -> int:
    return 456


@pytest.fixture
def chromosome_entry() -> str:
    return "X"


@pytest.fixture
def genome_build_entry() -> int:
    return 38
