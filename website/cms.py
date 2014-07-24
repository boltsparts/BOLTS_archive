from flask import url_for
from jinja2 import contextfilter, Markup
from docs import STABLE
import markdown
import re
from . import html
from os.path import join

def get_subs(version):
	return {
		'doc' : lambda m: url_for('docs.document',
			version=version,
			**dict(zip(['cat','filename'],(a.strip() for a in m.group(2).split(','))))
		),
		'doc_version' : lambda m: url_for('docs.document',
			**dict(zip(['version','cat','filename'],(a.strip() for a in m.group(2).split(','))))
		),
		'blog' : lambda m: url_for('blog.post',
			**dict(zip(['year','month','day','slug'],(a.strip() for a in m.group(2).split('/'))))
		),
		'url' : lambda m: url_for(m.group(2)),
		'collection_url' : lambda m: url_for('parts.collection',id=m.group(2)),
		'standard' : lambda m: html.a(m.group(2),href=url_for('parts.standard',id=m.group(2))),
		'name' : lambda m: html.a(m.group(2),href=url_for('parts.name',id=m.group(2))),
		'standard_url' : lambda m: url_for('parts.standard',id=m.group(2)),
		'name_url' : lambda m: url_for('parts.name',id=m.group(2))
	}

def markdownsub(ctx,value,subs):
	mkd = markdown.markdown(value)
	subs = re.sub('{{\s*([^(]*)\(([^\)]*)\)\s*}}',lambda m: subs[m.group(1)](m),mkd)
	return Markup(subs)

@contextfilter
def markdown_docs(ctx,value):
	if 'page' in ctx.parent and 'version' in ctx.parent['page']:
		version = ctx.parent['page']['version']
	else:
		version = STABLE
	subs = get_subs(version)
	subs['static'] = lambda m: url_for('docs.static',filename=join(version,m.group(2)))
	return markdownsub(ctx,value,subs)

@contextfilter
def markdown_blog(ctx,value):
	if 'page' in ctx.parent and 'version' in ctx.parent['page']:
		version = ctx.parent['page']['version']
	else:
		version = str(STABLE)
	subs = get_subs(version)
	subs['static'] = lambda m: url_for('blog.static',filename=join(m.group(2)))
	return markdownsub(ctx,value,subs)
