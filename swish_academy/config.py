"""Insta485 development configuration."""

import pathlib

# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'

# Secret key for encrypting cookies
SECRET_KEY = b'\xffQ6\xda\x0eII8\x9eg}\x9a_\n\x15\x1e\xbd\x8dfR\xb3\x91b\xa1'
SESSION_COOKIE_NAME = 'login'

# File Upload to var/uploads/
SWISH_ACADEMY_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = SWISH_ACADEMY_ROOT/'var'/'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Database file is var/insta485.sqlite3
DATABASE_FILENAME = SWISH_ACADEMY_ROOT/'var'/'swish_academy.sqlite3'
