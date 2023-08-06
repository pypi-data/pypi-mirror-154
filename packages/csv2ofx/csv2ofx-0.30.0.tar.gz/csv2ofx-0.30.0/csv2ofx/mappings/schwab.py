# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab
# pylint: disable=invalid-name
"""
csv2ofx.mappings.mintapi
~~~~~~~~~~~~~~~~~~~~~~~~

Provides a mapping for transactions obtained via mint.com
"""
from operator import itemgetter

mapping = {
    "has_header": True,
    "bank": "Schwab",
    "account": "Brokerage",
    "date": itemgetter("Date"),
    "amount": itemgetter("Amount"),
    "desc": itemgetter("Description"),
}
