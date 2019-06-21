from flask import Blueprint, render_template, abort, redirect, request, g, url_for, safe_join
from os.path import exists
import sys
if sys.version_info.major < 3:
	from urlparse import urljoin
else:
	from urllib.parse import urljoin
from werkzeug.contrib.atom import AtomFeed
from backends.website.translation import languages
from backends.website.utils import Posts
from backends.website.cms import markdown_blog

blog = Blueprint("blog",__name__,template_folder="templates",static_folder="static",url_prefix='/<any(%s):lang_code>/blog' % ",".join(languages))

@blog.url_defaults
def add_language_code(endpoint, values):
	if hasattr(g,'lang_code'):
		values.setdefault('lang_code',g.lang_code)
	else:
		values.setdefault('lang_code','en')

@blog.url_value_preprocessor
def pull_language_code(endpoint, values):
	g.lang_code = values.pop('lang_code')


posts = Posts(safe_join(blog.root_path,"posts"))

@blog.route("/<int:year>/<int:month>/<int:day>/<slug>")
@blog.route("/<int:year>/<int:month>/<int:day>/<slug>.html")
def post(year,month,day,slug):
	post = posts.get_slug(slug)
	if post is None:
		abort(404)
	else:
		page = {"title" : "Blog"}
		return render_template("blog/post.html",page=page,post=post)

@blog.route("/")
@blog.route("/index.html")
def index():
	page = {"title" : "Blog"}
	return render_template("blog/index.html",page=page,posts=posts.get_posts()[:-6:-1])

@blog.route("/all")
@blog.route("/archive.html")
def archive():
	page = {"title" : "Blog"}
	return render_template("blog/archive.html",page=page,posts=posts.get_posts()[::-1])

@blog.route("/atom")
@blog.route("/atom.xml")
def feed():
	feed = AtomFeed("Recent Blog Entries", feed_url=request.url, url=request.url_root)

	for post in posts.get_posts()[:-21:-1]:
		feed.add(
			post["title"],
			post["content"],
			content_type="html",
			author=post["author"],
			url=urljoin(request.url,url_for('blog.post',**post["url_values"])),
			updated=post["updated"] or post["date"],
			published=post["date"],
			summary=markdown_blog(post["teaser"]),
			summary_type="html")
	return feed.get_response()
