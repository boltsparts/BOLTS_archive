#bolttools - a framework for creation of part libraries
#Copyright (C) 2013 Johannes Reinhardt <jreinhardt@ist-dein-freund.de>
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import string
from os import listdir, makedirs, walk
from os.path import join, basename, splitext, exists, relpath
import subprocess
from shutil import copyfile
# pylint: disable=W0622
from codecs import open

from common import BackendExporter
from license import LICENSES_SHORT
import statistics, checker, openscad

#inspired by html.py but avoiding the dependency
def html_table(table_data,header=None,row_classes=None):
	"generates the content of a html table without the surrounding table tags"
	res = []
	if not header is None:
		row = " ".join([u"<th>%s</th>" % unicode(head) for head in header])
		res.append(u"<tr>%s<tr>" % row)
	if row_classes is None:
		row_classes = [None]*len(table_data)
	for row_data,row_class in zip(table_data,row_classes):
		row = " ".join([u"<td>%s</td>" % unicode(datum) for datum in row_data])
		if row_class is None:
			res.append(u"<tr>%s</tr>" % row)
		else:
			res.append(u"<tr class='%s'>%s</tr>" % (row_class,row))
	return u"\n".join(res)

def prop_row(props,prop,value):
	props.append("<tr><th><strong>%s:</strong></th><td>%s</td></tr>" %
		(prop,value))


class HTMLExporter(BackendExporter):
	def __init__(self,repo,databases):
		BackendExporter.__init__(self,repo,databases)
		self.templates = {}

		self.freecad = self.databases["freecad"]
		self.openscad = self.databases["openscad"]
		self.drawings = self.databases["drawings"]

		self.statistics = statistics.StatisticsExporter(repo,databases)
		self.checker = checker.CheckerExporter(repo,databases)

	def write_output(self,out_root):
		#load templates
		template_dir = join(self.repo.path,"backends","html")
		for dirpath,dirnames,filenames in walk(template_dir):
			for filename in filenames:
				name = join(relpath(dirpath,template_dir),splitext(filename)[0]).replace("./","")
				self.templates[name] = string.Template(open(join(dirpath,filename)).read())

		#clear output and copy files
		self.clear_output_dir(out_root)

		html_root = join(out_root,"html")
		makedirs(join(html_root,"classes"))
		makedirs(join(html_root,"collections"))
		makedirs(join(html_root,"bodies"))
		makedirs(join(html_root,"images"))
		makedirs(join(html_root,"drawings"))

		#write unchanged files
		for name in ["atom.xml","blog.html","contribute.html","public_domain.html","unclear_license.html"]:
			copyfile(join(template_dir,name),join(out_root,name))

		copyfile(join(template_dir,"no_drawing.png"),join(html_root,"drawings","no_drawing.png"))

		#write specification collections, parts and bodies
		for coll in self.repo.collections:
			with open(join(html_root,"collections","%s.html" % coll.id),'w','utf8') as fid:
				content = self._get_collection_content(coll)
				fid.write(self.templates["collection"].substitute(content))

			for cl in coll.classes:
				with open(join(html_root,"classes","%s.html" % cl.name),'w','utf8') as fid:
					content = self._get_class_content(coll,cl)
					fid.write(self.templates["class"].substitute(content))
				#copy drawings
				if cl.id in self.drawings.getbase:
					if not exists(join(html_root,"drawings",coll.id)):
						makedirs(join(html_root,"drawings",coll.id))
					drawing = self.drawings.getbase[cl.id]
					drawing_png = drawing.get_png()
					if not drawing_png is None:
						copyfile(drawing_png,join(html_root,"drawings",coll.id,drawing.filename + ".png"))

		#write body pages
		for body in self.repo.standard_bodies:
			with open(join(html_root,"bodies","%s.html" % body),'w','utf8') as fid:
				content = self._get_body_content(body)
				fid.write(self.templates["body"].substitute(content))

		#write spec index
		with open(join(html_root,"index.html"),'w','utf8') as fid:
			content = self._get_specs_index_content()
			fid.write(self.templates["html/index"].substitute(content))

		#write start page
		with open(join(out_root,"index.html"),'w','utf8') as fid:
			stats = self.statistics.get_part_statistics()
			params = {}
			for field in ["classes","collections","standards","commonconfigurations","bodies"]:
				params[field] = stats[field]
			contributors_names = self.statistics.get_contributors_list()
			params["contributors"] = str(len(contributors_names))
			fid.write(self.templates["index"].substitute(params))

		#write download page
		with open(join(out_root,"downloads.html"),"w","utf8") as fid:
			content = self._get_download_content()
			fid.write(self.templates["downloads"].substitute(content))

		#write task page
		with open(join(out_root,"tasks.html"),'w','utf8') as fid:
			content = self._get_task_page_content()
			fid.write(self.templates["tasks"].substitute(content))

		#write contributors list
		with open(join(out_root,"contributors.html"),'w','utf8') as fid:
			contributors_names = self.statistics.get_contributors_list()
			params = {}
			params["ncontributors"] = str(len(contributors_names))
			params["table"] = html_table([[name] for name in contributors_names])

			fid.write(self.templates["contributors"].substitute(params))

		#write base graphs
		for coll in self.repo.collections:
			#write dot files
			image_path = join(html_root,'images')
			with open(join(image_path,'%s.dot' % coll.id),'w','utf8') as fid:
				fid.write(self._get_coll_base_graph_dot(coll))

			#render dots to svg
			with open(join(image_path,"%s.svg" % coll.id),'w','utf8') as fid:
				fid.write(subprocess.check_output(["dot","-Tsvg",join(image_path,"%s.dot" % coll.id)]))

			#render dots to png
			with open(join(image_path,"%s.png" % coll.id),'wb') as fid:
				fid.write(subprocess.check_output(["dot","-Tpng",join(image_path,"%s.dot" % coll.id)]))

	def _get_coll_base_graph_dot(self,coll):
		res = []

		res.append("digraph G {")
		res.append("rankdir=LR; nodesep=0.5; ranksep=1.5;splines=polyline;")
		std_cluster = ["subgraph cluster_std {"]
		std_cluster.append('label="Standards";')
		cl_cluster = ["subgraph cluster_cl {"]
		cl_cluster.append('label="Classes";')
		fcd_cluster = ["subgraph cluster_fcd {"]
		fcd_cluster.append('label="FreeCAD";')
		ocd_cluster = ["subgraph cluster_ocd {"]
		ocd_cluster.append('label="OpenSCAD";')
		links = []

		layout_classes = "[width=3, height=0.8, fixedsize=true]"
		layout_base = "[width=4, height=0.8, fixedsize=true]"
		layout_standard = "[width=3, height=0.8, fixedsize=true]"

		classes = []
		for cl in coll.classes:
			if not cl.id in classes:
				cl_cluster.append('"%s" %s;' % (cl.id,layout_classes))

				if (not self.freecad is None) and cl.id in self.freecad.getbase:
					base = self.freecad.getbase[cl.id]
					filename = basename(base.filename)
					if base.type == "function":
						fcd_cluster.append('"%s:%s" %s;' % (filename,base.name,layout_base))
						links.append('"%s" -> "%s:%s";' % (cl.id, filename,base.name))
					elif base.type == "fcstd":
						fcd_cluster.append('"%s:%s" %s;' % (filename,base.objectname,layout_base))
						links.append('"%s" -> "%s:%s";' % (cl.id, filename,base.objectname))

				if (not self.openscad is None) and  cl.id in self.openscad.getbase:
					base = self.openscad.getbase[cl.id]
					filename = basename(base.filename)
					if base.type == "module":
						ocd_cluster.append('"%s:%s" %s;' % (filename,base.name,layout_base))
						links.append('"%s" -> "%s:%s";' % (cl.id, filename,base.name))
					elif base.type == "stl":
						ocd_cluster.append('"%s:%s" %s;' % (filename,"STL",layout_base))
						links.append('"%s" -> "%s:%s";' % (cl.id, filename,"STL"))

				classes.append(cl.id)

			if not cl.standard is None:
				std_cluster.append('"%s" %s;' % (cl.name,layout_standard))
				links.append('"%s" -> "%s";' % (cl.name, cl.id))

		cl_cluster.append("}")
		std_cluster.append("}")
		fcd_cluster.append("}")
		ocd_cluster.append("}")

		res.extend(cl_cluster)
		res.extend(std_cluster)
		res.extend(fcd_cluster)
		res.extend(ocd_cluster)
		res.extend(links)
		res.append("}")

		return "\n".join(res)

	def _get_task_page_content(self):
		params = {}

		for name,check in self.checker.checks.iteritems():
			params[name + "title"] = check.get_title()
			params[name + "description"] = check.get_description()
			params[name + "table"] = html_table(check.get_table(),check.get_headers())

		return params

	def _get_specs_index_content(self):
		params = {}
		params["title"] = "BOLTS Index"
		data = [ [
				"<a href='collections/%s.html'>%s</a>" % (coll.id,coll.name),
				coll.description
			] for coll in self.repo.collections]
		header = ["Name", "Description"]
		params["collections"] = html_table(data,header)
		data = [ [
				"<a href='bodies/%s.html'>%s</a>" % (body,body),
				"Standards issued by %s" % body
			] for body in self.repo.standard_bodies]
		header = ["Name", "Description"]
		params["bodies"] = html_table(data,header)

		return params

	def _get_download_content(self):
		asset_path = join(self.repo.path,"downloads")
		backends = ["freecad","openscad"]

		#find most current release
		release = {}
		development = {}

		for backend in backends:
			release[backend] = {}
			development[backend] = {}
			for filename in listdir(join(asset_path,backend)):
				basename,ext = splitext(filename)
				if ext == ".gz":
					ext = ".tar.gz"
					basename = splitext(basename)[0]
				parts = basename.split("_")
				version_string = parts[2]

				#some old development snapshots have no license in filename
				license = "none"
				if len(parts) > 3:
					license = parts[3]

				kind = development[backend]
				version = None
				try:
					version = int(version_string)
				except ValueError:
					version = float(version_string)
					kind = release[backend]

				if not license in kind:
					kind[license] = {}
				if not ext in kind[license]:
					kind[license][ext] = (version, join(backend,filename))
				elif version > kind[license][ext][0]:
					kind[license][ext] = (version, join(backend,filename))

		params = {}

		for kind,kind_name in zip([release, development],
			["release","development"]):
			for backend in backends:
				rows = []
				for license in ["lgpl2.1+","gpl3"]:
					if license in kind[backend]:
						rows.append([LICENSES_SHORT[license],
							'<a href="downloads/%s">.tar.gz</a>' % (kind[backend][license][".tar.gz"][1]),
							'<a href="downloads/%s">.zip</a>' % (kind[backend][license][".zip"][1])])
				if len(rows) == 0:
					rows = [["No %s distribution available" % kind_name]]
				params["%s%s" % (backend, kind_name)] = html_table(rows)
		return params

	def _get_collection_content(self,coll):
		params = {}
		params["title"] = coll.name
		params["description"] = coll.description or "No description available"
		params["collectionid"] = coll.id

		author_links = ["<a href='mailto:%s'>%s</a>" % (m,n)
			for m,n in zip(coll.author_mails,coll.author_names)]
		params["author"] = " and <br>".join(author_links)

		params["license"] = "<a href='%s'>%s</a>" % \
			(coll.license_url,coll.license_name)

		data = [["<a href='../classes/%s.html'>%s</a>" % (cl.name,cl.name),
				cl.description,
				cl.status] for cl in coll.classes]
		header = ["Name", "Description", "Status"]
		row_classes = [cl.status for cl in coll.classes]
		params["classes"] = html_table(data,header,row_classes)

		return params

	def _get_body_content(self,body):
		params = {}
		params["title"] = body
		params["description"] = "Standards issued by %s" % body

		data = [["<a href='../classes/%s.html'>%s</a>" % (cl.name,cl.name),
				cl.description,
				cl.status] for cl in self.repo.standardized[body]]
		header = ["Name", "Description", "Status"]
		row_classes = [cl.status for cl in self.repo.standardized[body]]
		params["classes"] = html_table(data,header,row_classes)

		return params


	def _get_class_content(self,coll,cl):
		params = {}

		params["title"] = cl.name
		params["description"] = cl.description or "No description available"

		#find drawing
		if cl.id in self.drawings.getbase:
			drawing = self.drawings.getbase[cl.id]
			if drawing.get_png() is None:
				params["drawing"] = "no_drawing.png"
			else:
				params["drawing"] = join(drawing.collection,drawing.filename+ ".png")
		else:
			params["drawing"] = "no_drawing.png"

		props = []

		for mail,name in zip(coll.author_mails,coll.author_names):
			prop_row(props,"Author","<a href='mailto:%s'>%s</a>" % (mail,name))
		prop_row(props,"License","<a href='%s'>%s</a>" %
			(coll.license_url,coll.license_name))
		prop_row(props,"Collection","<a href='../collections/%s.html'>%s</a>" %
				(coll.id,coll.name))

		if not cl.standard is None:
			identical = ", ".join(["<a href='%s.html'>%s</a>" % (id,id)
				for id in cl.standard if id != cl.name])
			if identical:
				prop_row(props,"Identical to",identical)

			prop_row(props,"Status",cl.status)
			prop_row(props,"Standard body","<a href='../bodies/%s.html'>%s</a>" %
				(cl.standard_body,cl.standard_body))
			if not cl.replaces is None:
				prop_row(props,"Replaces","<a href='%s.html'>%s</a>" %
					(cl.replaces,cl.replaces))

			if not cl.replacedby is None:
				prop_row(props,"Replaced by","<a href='%s.html'>%s</a>" %
					(cl.replacedby,cl.replacedby))

		prop_row(props,"Class ID",cl.id)

		if cl.url:
			prop_row(props,"Url",cl.url)
		prop_row(props,"Source",cl.source)

		params["properties"] = "\n".join(props)

		#TODO: multiple tables properly
		params["dimensions"] = ""
		for table in cl.parameters.tables:
			keys = sorted(table.data.keys())
			#try to detect metric threads
			if "M" in [str(v)[0] for v in table.data.keys()]:
				try:
					keys = sorted(table.data.keys(),key=lambda x: float(x[1:]))
				except ValueError:
					keys = sorted(table.data.keys())
			data = [[key] + table.data[key] for key in keys]

			lengths = {"Length (mm)" : "mm", "Length (in)" : "in"}

			header = [str(table.index)]
			for p in table.columns:
				if cl.parameters.types[p] in lengths:
					header.append("%s (%s)" % (str(p), lengths[cl.parameters.types[p]]))
				else:
					header.append("%s" % str(p))

			params["dimensions"] += html_table(data,header)

		#freecad information
		if self.freecad is None:
			params["freecad"] = "<tr><td>FreeCAD Backend is not available</td></tr>\n"
		else:
			if cl.id in self.freecad.getbase:
				base = self.freecad.getbase[cl.id]
				freecad_props = []
				for mail,name in zip(base.author_mails,base.author_names):
					prop_row(freecad_props,"Author","<a href='mailto:%s'>%s</a>" % 
						(mail,name))
				prop_row(freecad_props,"License","<a href='%s'>%s</a>" %
					(base.license_url,base.license_name))
				params["freecad"] = "\n".join(freecad_props)
			else:
				params["freecad"] = "<tr><td>Class is not available in FreeCAD</td></tr>\n"

		#openscad
		if self.openscad is None:
			params["openscad"] = "<tr><td>OpenSCAD Backend is not available</td></tr>\n"
			params["openscadincantation"] = ""
		else:
			if cl.id in self.openscad.getbase:
				base = self.openscad.getbase[cl.id]
				openscad_props = []
				for mail,name in zip(base.author_mails,base.author_names):
					prop_row(openscad_props,"Author","<a href='mailto:%s'>%s</a>" %
						(mail,name))
				prop_row(openscad_props,"License","<a href='%s'>%s</a>" %
					(base.license_url,base.license_name))
				params["openscad"] = "\n".join(openscad_props)

				params["openscadincantation"] = "<h2>Incantations</h2>\n"
				params["openscadincantation"] += "{% highlight python %}\n"
				params["openscadincantation"] += "%s(%s);\n" % (cl.openscadname,
					openscad.get_signature(cl,cl.parameters.union(base.parameters)))
				params["openscadincantation"] += "dims = %s_dims(%s);\n" % (cl.openscadname,
					openscad.get_signature(cl,cl.parameters.union(base.parameters)))
				params["openscadincantation"] += "{% endhighlight %}\n"
			else:
				params["openscad"] = "<tr><td>Class not available in OpenSCAD</td></tr>\n"
				params["openscadincantation"] = ""

		return params
