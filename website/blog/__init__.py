from flask import Blueprint, render_template, abort, redirect, request
from os.path import exists,join
from os import listdir
from yaml import load
import markdown
import datetime
import re
from urlparse import urljoin
from werkzeug.contrib.atom import AtomFeed

blog = Blueprint("blog",__name__,template_folder="templates",static_folder="static")

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
			post["url"] = "%s/%s/%s/%s" % (year,month,day,post["slug"])

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

				if post["url"] in self.urls:
					raise ValueError("Nonunique url: %s"% post["url"])
				self.urls[post["url"]] = post
				if post["slug"] in self.slugs:
					raise ValueError("Nonunique slug: %s"% post["slug"])
				self.slugs[post["slug"]] = post

		self.posts = sorted(self.urls.values(),key = lambda x: x["date"])

	def get_url(self,url):
		if url in self.urls:
			return self.urls[url]
		else:
			return None

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
def post(year,month,day,slug):
	post = posts.get_slug(slug)
	if post is None:
		abort(404)
	else:
		page = {"title" : "Blog"}
		return render_template("post.html",page=page,post=post)

@blog.route("/")
@blog.route("/index.html")
def index():
	page = {"title" : "Blog"}
	return render_template("blog.html",page=page,posts=posts.get_posts()[:-6:-1])

@blog.route("/all")
def archive():
	page = {"title" : "Blog"}
	return render_template("archive.html",page=page,posts=posts.get_posts()[::-1])

@blog.route("/atom")
@blog.route("/atom.xml")
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
