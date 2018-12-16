from flask_paginate import get_page_parameter
from flask import request
import settings


def get_page():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * settings.PER_PAGE
    end = start + settings.PER_PAGE
    return page, start, end
