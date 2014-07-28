from flask.ext.babelex import Domain
from os import environ
from os.path import join

trans_dir = join(environ["OPENSHIFT_REPO_DIR"],"translations")
messages_domain = Domain(trans_dir,domain="messages")
parts_domain = Domain(trans_dir,domain="parts")

def gettext_parts(msgid):
	return parts_domain.gettext(msgid)
