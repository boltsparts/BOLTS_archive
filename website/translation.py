from flask.ext.babelex import Domain
from os import environ,listdir
from os.path import join

trans_dir = join(environ["OPENSHIFT_REPO_DIR"],"translations")
messages_domain = Domain(trans_dir,domain="messages")
parts_domain = Domain(trans_dir,domain="parts")
docs_domain = Domain(trans_dir,domain="docs")

languages = listdir(trans_dir) + ['en']

def gettext_parts(msgid):
	return parts_domain.gettext(msgid)

def gettext_docs(msgid):
	return docs_domain.gettext(msgid)
