"""
Github Apps API wrapper
This is a wrapper for the Github Apps API. It provides a simple interface to
make requests to the API and return the results as a dictionary.
:copyright: (c) 2022 by the authors and contributors (see AUTHORS).
:license: MIT, see LICENSE for more details.
"""
__title__ = 'githubapps'
__author__ = 'RTa-technology'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022 by the authors and contributors (see AUTHORS)'
__version__ = '1.0.0'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .adapter import Authentication, RequestsAuth, AiohttpAuth

from .errors import (BadRequest, Forbidden, HTTPException, InternalServerError,
                     NotFound, PayloadTooLarge, QuotaExceeded,
                     ServiceUnavailable, TooManyRequests, URITooLong)

__all__ = ['Authentication', 'RequestsAuth', 'AiohttpAuth']