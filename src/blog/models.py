from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from django.template.defaultfilters import slugify
import markdown


class Blog(models.Model):
	DRAFT = 'D'
	PUBLISHED = 'P'
	STATUS = (
		(DRAFT,'Draft'),
		(PUBLISHED,'Published'),
	)

	title = models.CharField(max_length=256)
	slug = models.SlugField(max_length=256, null=True, blank=True)
	content = models.TextField(max_length=4000)
	status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
	blogger = models.ForeignKey(User)
	create_date = models.DateTimeField(auto_now_add=True)
	update_date = models.DateTimeField(blank=True, null=True)
	update_user = models.ForeignKey(User, null=True, blank=True, related_name="editor")

	class Meta:
		verbose_name = _("Blog")
		verbose_name_plural = _("Blogs")
		ordering = ("-create_date",)

	def __unicode__(self):
		return self.title

	def save(self,*args,**kwargs):
		if not self.pk:
			super(Blog,self).save(*args,**kwargs)
		else:
			self.update_date = datetime.now()
		if not self.slug:
			self.slug = slugify("%s %s"%(self.pk,self.title.lower()))
		super(Blog,self).save(*args,**kwargs)


	def get_content(self):
		return markdown.markdown(self.content,safe_mode='escape')
		
	@staticmethod
	def get_published_posts():
		posts = Blog.objects.filter(status=Blog.PUBLISHED)
		return posts

	def create_tags(self,tags):
		tags = tags.strip().split(' ')
		for tag in tags:
			if tag:
				t,created = Tag.objects.get_or_create(tag=tag.lower(),blog=self)

	def get_tags(self):
		return Tag.objects.filter(blog=self)

	def get_summary(self):
		if len(self.content) > 256:
			return "%s ....."%(self.content[:256])
		return self.content


class Tag(models.Model):
	tag = models.CharField(max_length=50)
	blog = models.ForeignKey(Blog)

	class Meta:
		verbose_name = _('Tag')
		verbose_name_plural = _('Tags')
		unique_together = (('tag', 'blog'),)
        index_together = [['tag', 'blog'],]

	def __unicode__(self):
		return self.tag 

	@staticmethod
	def get_popular_tags():
		tags = Tag.objects.all()
		d = {}
		for tag in tags:
			if tag.blog.status == Blog.PUBLISHED:
				if tag.tag in d:
					d[tag.tag] += 1
				else:
					d[tag.tag] = 1
		tags = sorted(d.items(), key=lambda item: item[1])
		if len(tags) < 10:
			return tags
		return tags[-9:]
