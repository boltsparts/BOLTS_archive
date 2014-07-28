from flask import Blueprint, render_template, abort, redirect, request, g
from os.path import exists,join
from os import listdir
from yaml import load
import markdown
import datetime
import re
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed
from ..cache import cache
from ..translation import languages

blog = Blueprint("blog",__name__,template_folder="templates",static_folder="static",url_prefix='/<any(%s):lang_code>/blog' % ",".join(languages))

@blog.url_defaults
def add_language_code(endpoint, values):
	values.setdefault('lang_code',g.lang_code)

@blog.url_value_preprocessor
def pull_language_code(endpoint, values):
	g.lang_code = values.pop('lang_code')

class Posts:
	def __init__(self,path):
		self.urls = {}
		self.slugs = {}
		self.posts = []

		for filename in listdir(path):
			if filename.startswith('.'):
				continue
			post = {}

			parts = filename.split('-')
			year = int(parts[0])
			month = int(parts[1])
			day = int(parts[2])
			post["slug"] = '.'.join('-'.join(parts[3:]).split('.')[:-1])
			post["url_values"] = {"year" : year, "month" : month, "day" : day, "slug" : post["slug"]}

			with open(join(path,filename)) as fid:
				header, content = fid.read().split('\n---\n')
				header = load(header)
				post["content"] = content
				post["teaser"] = content.split('<!-- more -->')[0].strip()
				post["title"] = header['title']

				if 'date' in header:
					post["date"] = header['date']
				else:
					post["date"] = datetime.datetime(year,month,day)

				if 'updated' in header:
					post["updated"] = header["updated"]
				else:
					post["updated"] = None

				if 'author' in header:
					match = re.match("([^<]*)<([^>]*)>",header["author"])
					if match is None:
						post["author"] = header["author"]
						post["email"] = ""
					else:
						post["author"] = match.group(1).strip()
						post["email"] = match.group(2).strip()
				else:
					post["author"] = "Unknown"

				if post["slug"] in self.slugs:
					raise ValueError("Nonunique slug: %s"% post["slug"])
				self.slugs[post["slug"]] = post

		self.posts = sorted(self.slugs.values(),key = lambda x: x["date"])

	def get_slug(self,slug):
		if slug in self.slugs:
			return self.slugs[slug]
		else:
			return None

	def get_posts(self):
		return self.posts

posts = Posts(join(blog.root_path,"posts"))


@blog.route("/<int:year>/<int:month>/<int:day>/<slug>")
@blog.route("/<int:year>/<int:month>/<int:day>/<slug>.html")
@cache.cached()
def post(year,month,day,slug):
	post = posts.get_slug(slug)
	if post is None:
		abort(404)
	else:
		page = {"title" : "Blog"}
		return render_template("post.html",page=page,post=post)

@blog.route("/")
@blog.route("/index.html")
@cache.cached()
def index():
	page = {"title" : "Blog"}
	return render_template("blog.html",page=page,posts=posts.get_posts()[:-6:-1])

@blog.route("/all")
@cache.cached()
def archive():
	page = {"title" : "Blog"}
	return render_template("archive.html",page=page,posts=posts.get_posts()[::-1])

@blog.route("/atom")
@blog.route("/atom.xml")
@cache.cached()
def feed():
	feed = AtomFeed("Recent Blog Entries", feed_url=request.url, url=request.url_root)

	for post in posts.get_posts()[:-21:-1]:
		feed.add(
			post["title"],
			markdown.markdown(post["content"]),
			content_type="html",
			author=post["author"],
			url=urljoin(request.url,post["url"]),
			updated=post["updated"] or post["date"],
			published=post["date"],
			summary=markdown.markdown(post["teaser"]),
			summary_type="html")
	return feed.get_response()
