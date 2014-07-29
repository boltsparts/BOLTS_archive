import datetime
import re
from os import walk, listdir
from os.path import exists, join, relpath, splitext
import markdown
from yaml import safe_load as load
from docutils import core

from bolttools.common import UNITS

def split_yaml_header(fid):
	line = fid.readline()
	if line.strip() != '---':
		raise ValueError('No YAML header found at the beginning')
	header = []
	for line in fid:
		if line.strip() == '---':
			break
		header.append(line)
	content = ''.join(line for line in fid)
	return load('\n'.join(header)),content

class Specification:
	def __init__(self,path):
		self.version = {}
		self.changes = open(join(path,"changes.rst")).read()

		spec_pattern = re.compile("blt_spec_([0-9]\.[0-9])\.rst")

		for filename in listdir(path):
			match = spec_pattern.match(filename)
			if not match is None:
				self.version[match.group(1)] = open(join(path,filename)).read()
	def get_version(self,version):
		return self.version[version]
	def get_changes(self):
		return self.changes

class Documentation:
	def __init__(self,path):
		self.documents = []
		self.categories = set([])
		self.audiences = set([])
		self.versions = set([])

		for version in listdir(path):
			self.versions.add(version)
			for cat in listdir(join(path,version)):
				self.categories.add(cat)
				for filename in listdir(join(path,version,cat)):
					if filename.startswith('.'):
						continue
					doc = {}
					doc["category"] = cat
					doc["version"] = version

					with open(join(path,version,cat,filename)) as fid:
						header, content = split_yaml_header(fid)

					doc["title"] = header["title"]
					doc["filename"] = splitext(filename)[0]
					doc["audience"] = header["audience"]

					self.audiences.add(header["audience"])

					doc["content"] = [ p.strip().replace("%","%%") for p in content.split('\n\n')]
					self.documents.append(doc)

		self.categories = list(self.categories)
		self.audiences = list(self.audiences)
		self.versions = list(self.versions)
		self.versions.sort(key=lambda x: float(x))

	def extract_messages(self,fid):
		for doc in self.documents:
			fid.write('\n#. document title\n')
			fid.write('#: docs/%s/%s/%s\n' % (doc["version"],doc["category"],doc["filename"]))
			fid.write('msgid "%s"\nmsgstr ""\n' % doc["title"])
			for paragraph in doc["content"]:
				fid.write('\n#: docs/%s/%s/%s\n' % (doc["version"],doc["category"],doc["filename"]))
				fid.write('msgid "%s"\nmsgstr ""\n' % '\\n"\n"'.join(paragraph.split("\n")))

	def get_versions(self):
		return self.versions

	def get_stable(self):
		return self.versions[-2]

	def get_dev(self):
		return self.versions[-1]

	def get_categories(self):
		return self.categories

	def get_audiences(self):
		return self.audiences

	def get_documents(self,version=None,category=None,audience=None,filename=None):
		res = []
		for doc in self.documents:
			if (not version is None) and doc["version"] != version:
				continue
			if (not category is None) and doc["category"] != category:
				continue
			if (not audience is None) and doc["audience"] != audience:
				continue
			if (not filename is None) and doc["filename"] != filename:
				continue
			res.append(doc)
		return res


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

