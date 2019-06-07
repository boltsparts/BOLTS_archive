from flask_babelex import Domain
from os import environ,listdir
from flask import safe_join
from os.path import split
import backends

trans_dir = safe_join(split(split(backends.__file__)[0])[0], "translations")
messages_domain = Domain(trans_dir,domain="messages")
parts_domain = Domain(trans_dir,domain="parts")
docs_domain = Domain(trans_dir,domain="docs")

languages = listdir(trans_dir) + ['en']

def gettext_parts(msgid):
	return parts_domain.gettext(msgid)

def gettext_docs(msgid):
	return docs_domain.gettext(msgid)
