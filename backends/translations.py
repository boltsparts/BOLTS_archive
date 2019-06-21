from common import Backend, UNITS
from babel.messages.catalog import Catalog
from babel.messages.pofile import write_po, read_po

class TranslationBackend(Backend):
	def __init__(self,repo,databases):
		Backend.__init__(self,repo,'translations',databases,[])

	def _name_extract(self,cat,name,cl,coll):
		cat.add(name.name.get_nice(),auto_comments=[
			'ClassName name nice',
			'data/%s.blt, class: %s\n' % (coll.id,cl.id)
		])

		cat.add(name.labeling.nice,auto_comments=[
			'ClassName labeling nice',
			'data/%s.blt, class: %s\n' % (coll.id,cl.id)
		])

		cat.add(name.description,auto_comments=[
			'ClassName description',
			'data/%s.blt, class: %s\n' % (coll.id,cl.id)
		])

	def _standard_extract(self,cat,std,cl,coll):
		cat.add(std.labeling.nice,auto_comments=[
			'ClassStandard labeling nice',
			'data/%s.blt, class: %s\n' % (coll.id,cl.id)
		])

		cat.add(std.description,auto_comments=[
			'ClassStandard description\n',
			'data/%s.blt, class: %s\n' % (coll.id,cl.id)
		])

	def _class_extract(self,cat,cl,coll):
		for pname in cl.parameters.parameters:
			cat.add(cl.parameters.description[pname],auto_comments=[
				'Parameter description %s\n' % pname,
				'data/%s.blt, class %s\n' % (coll.id,cl.id)
			])

	def _coll_extract(self,cat,coll):
		cat.add(coll.name,auto_comments=['collection name','data/%s.blt' % coll.id])
		cat.add(coll.description,auto_comments=[
			'collection description','data/%s.blt' % coll.id
		])

	def write_output(self,out_path,**kwargs):
		args = self.validate_arguments(kwargs,[],{})

		template = Catalog(domain="parts", project="BOLTS")

		for coll, in self.repo.itercollections():
			self._coll_extract(template,coll)

		for cl,coll in self.repo.iterclasses(["class","collection"]):
			self._class_extract(template,cl,coll)

		for name,cl,coll in self.repo.iternames(["name","class","collection"]):
			self._name_extract(template,name,cl,coll)

		for std,cl,coll in self.repo.iterstandards(["standard","class","collection"]):
			self._standard_extract(template,std,cl,coll)

		with open(out_path,'w') as fid:
			write_po(fid,template)
