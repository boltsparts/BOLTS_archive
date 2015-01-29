from flask import url_for
from jinja2 import contextfilter, Markup
from docs import STABLE
import markdown
import re
import website.html
from os.path import join

def get_subs(version):
	lang_code = "en"
	return {
		'doc' : lambda m: url_for('docs.document',
			version=version,
			lang_code=lang_code,
			**dict(zip(['cat','filename'],(a.strip() for a in m.group(2).split(','))))
		),
		'doc_version' : lambda m: url_for('docs.document',
			lang_code=lang_code,
			**dict(zip(['version','cat','filename'],(a.strip() for a in m.group(2).split(','))))
		),
		'blog' : lambda m: url_for('blog.post',
			lang_code=lang_code,
			**dict(zip(['year','month','day','slug'],(a.strip() for a in m.group(2).split('/'))))
		),
		'url' : lambda m: url_for(m.group(2),lang_code = lang_code),
		'collection_url' : lambda m: url_for('parts.collection',id=m.group(2),lang_code=lang_code),
		'standard' : lambda m: website.html.a(m.group(2),href=url_for('parts.standard',id=m.group(2),lang_code = lang_code)),
		'name' : lambda m: website.html.a(m.group(2),href=url_for('parts.name',id=m.group(2),lang_code = lang_code)),
		'body' : lambda m: website.html.a(m.group(2),href=url_for('parts.body',id=m.group(2),lang_code = lang_code)),
		'standard_url' : lambda m: url_for('parts.standard',id=m.group(2),lang_code = lang_code),
		'name_url' : lambda m: url_for('parts.name',id=m.group(2,lang_code = lang_code)),
		'body_url' : lambda m: url_for('parts.body',id=m.group(2),lang_code = lang_code)
	}

def markdownsub(value,subs):
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
	subs['spec'] = lambda m: url_for('docs.specification') + ("#%s" % m.group(2))
	return markdownsub(value,subs)

def markdown_blog(value):
	subs = get_subs(str(STABLE))
	subs['static'] = lambda m: url_for('blog.static',filename=join(m.group(2)))
	return markdownsub(value,subs)
