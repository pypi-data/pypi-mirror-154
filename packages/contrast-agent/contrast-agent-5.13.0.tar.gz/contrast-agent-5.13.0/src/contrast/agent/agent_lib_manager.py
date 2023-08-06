# -*- coding: utf-8 -*-
# Copyright © 2022 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


def initialize():
    logger.debug("Initializing agent-lib")
    # TODO: PYT-2263 initialize agent-lib
