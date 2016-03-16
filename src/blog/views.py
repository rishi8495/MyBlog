from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
from django.views.generic import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from decorators import ajax_required
import markdown

from .models import *
from .forms import BlogForm

class BlogDetailView(View):
	def get(self,request,slug=None):
		post = get_object_or_404(Blog,slug=slug,status=Blog.PUBLISHED)
		return render(request,'blog/detail_post.html',{
			'post':post
		})

class BlogListView(View):
	def get(self,request):
		posts = Blog.get_published_posts()
		paginator = Paginator(posts,5)
		page = request.GET.get('page')
		try:
			posts = paginator.page(page)
		except PageNotAnInteger:
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_pages)
		popular_tags = Tag.get_popular_tags()
		return render(request,'blog/posts.html',{
			'posts':posts,
			'popular_tags':popular_tags
			})



class CreateBlogView(View):
	@method_decorator(login_required)
	def get(self,request):
		form = BlogForm()
		return render(request,'blog/new.html',{
			'form':form
			})

	@method_decorator(login_required)
	def post(self,request):
		form = BlogForm(request.POST)
		if form.is_valid():
			blog = Blog()
			blog.blogger = request.user
			blog.title = form.cleaned_data.get('title')
			blog.content = form.cleaned_data.get('content')
			status = form.cleaned_data.get('status')
			if status == Blog.PUBLISHED:
				blog.status = status
			blog.save()
			tags = form.cleaned_data.get('tags')
			blog.create_tags(tags)
			return redirect('/')
		return render(request,'blog/new.html',{
			'form':form
			})

class DraftView(View):
	@method_decorator(login_required)
	def get(self,request):
		drafts = Blog.objects.filter(blogger=request.user,status=Blog.DRAFT)
		return render(request,'blog/drafts.html',{
			'drafts':drafts
			})


class TagView(View):
	def get(self,request,tag_name):
		tags = Tag.objects.filter(tag=tag_name)
		posts = []
		for tag in tags:
			if tag.blog.status == Blog.PUBLISHED:
				posts.append(tag.blog)
		popular_tags = Tag.get_popular_tags()
		return render(request,'blog/posts.html',{
			'posts':posts,
			'popular_tags':popular_tags
			})
