import datetime
import re
from os import listdir
from os.path import exists,join
import markdown
from yaml import load

from bolttools.common import UNITS

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
				post["content"] = markdown.markdown(content)
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


def tables2d_as_dicts(params):
	"""
	Convert the 2D tables of a Parameters instance into a form suitable for the html_table Jinja Filter

	Returns a list of dicts
	"""
	res = []
	for table in params.tables2d:
		result = None
		if params.types[table.result] in UNITS:
			result = "%s (%s)" % (table.result,UNITS[params.types[table.result]])
		else:
			result = table.result
		res.append({
			"data" : [table.data[i] for i in params.choices[table.rowindex]],
			"corner" : result,
			"col_header" : table.columns,
			"row_header" : params.choices[table.rowindex]
		})
	return res


def tables_as_dicts(params):
	"""
	Convert the tables of a Parameters instanceinto a form suitable for the html_table Jinja Filter

	Returns a list of dicts
	"""
	res = []
	for table in params.tables:
		header = [str(table.index)]
		for p in table.columns:
			if params.types[p] in UNITS:
				header.append("%s (%s)" % (str(p), UNITS[params.types[p]]))
			else:
				header.append("%s" % str(p))
		res.append({
			"data" : [[idx] + table.data[idx] for idx in params.choices[table.index]],
			"header" : header,
		})
	return res

