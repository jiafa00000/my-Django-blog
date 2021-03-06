#coding:utf-8
from django.shortcuts import render
from django.shortcuts import render_to_response,get_object_or_404
from django.template import RequestContext
from article.models import Article,Tag,Classification
from django.http import Http404
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.syndication.views import Feed #订阅RSS
import json
from django.core import serializers
#from urllib2 import urlopen as uu
import urllib
import re
import requests
# Create your views here.
 

def note_index(request):

    is_home=True
    articles = Article.objects.all()
    paginator = Paginator(articles,6)#每个页面最多显示6篇文章
    page_num = request.GET.get('page')
    tags=Tag.objects.all()
    try:
        articles = paginator.page(page_num)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)

     #显示最新发布的前10篇文章
     #ar_newpost = Article.objects.order_by('-publish_time')[:10]     
    classification = Classification.class_list.get_Class_list()#分类,以及对应的数目
    #tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    tagCloud=Tag.tag_list.get_Tag_list()
    date_list = Article.date_list.get_Article_onDate()#按月归档,以及对应的文章数目
    taglist=Tag.tag_list.get_Tag_list()
    return render_to_response('note/index_new.html',
            locals(), #它返回的字典对所有局部变量的名称与值进行映射。
            context_instance=RequestContext(request))


def home(request):

     # is_home=True
     # articles = Article.objects.all()
     # paginator = Paginator(articles,6)#每个页面最多显示6篇文章
     # page_num = request.GET.get('page')
     # try:
     #     articles = paginator.page(page_num)
     # except PageNotAnInteger:
     #     articles = paginator.page(1)
     # except EmptyPage:
     #     articles = paginator.page(paginator.num_pages)


     # #显示最新发布的前10篇文章
     # #ar_newpost = Article.objects.order_by('-publish_time')[:10]
     

     # classification = Classification.class_list.get_Class_list()#分类,以及对应的数目
     # tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
     # date_list = Article.date_list.get_Article_onDate()#按月归档,以及对应的文章数目
  
     return render_to_response('index.html',
            locals(), #它返回的字典对所有局部变量的名称与值进行映射。
            context_instance=RequestContext(request))
def detail(request, year,month,day,id):
    try:
       article = Article.objects.get(id=str(id))
    except Article.DoesNotExist:
       raise Http404

    #ar_newpost = Article.objects.order_by('-publish_time')[:10]

    classification = Classification.class_list.get_Class_list()
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    #tags=Tag.objects.all()
    taglist=Tag.tag_list.get_Tag_list()

    return render_to_response('note/content_new.html',
            locals(),
            context_instance=RequestContext(request))
def archive_month(request, year,month):
    
    is_arch_month = True
    articles = Article.objects.filter(publish_time__year=year).filter(publish_time__month=month)#当前日期下的文章列表
    paginator = Paginator(articles,6)
    page_num = request.GET.get('page')
    try:
         articles = paginator.page(page_num)
    except PageNotAnInteger:
         articles = paginator.page(1)
    except EmptyPage:
         articles = paginator.page(paginator.num_pages)

    #ar_newpost = Article.objects.order_by('-publish_time')[:10]
    classification = Classification.class_list.get_Class_list()  
    #tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    taglist=Tag.tag_list.get_Tag_list()
    tagCloud=Tag.tag_list.get_Tag_list()
    #tags=Tag.objects.all()
    return render_to_response('note/index_new.html',
            locals(),
            context_instance=RequestContext(request))
def classfiDetail(request, classfi):
    
    is_classfi = True
    temp = Classification.objects.get(name=classfi) #获取全部的Article对象
    articles = temp.article_set.all()
    paginator = Paginator(articles,6)
    page_num = request.GET.get('page')
    try:
         articles = paginator.page(page_num)
    except PageNotAnInteger:
         articles = paginator.page(1)
    except EmptyPage:
         articles = paginator.page(paginator.num_pages)

    #ar_newpost = Article.objects.order_by('-publish_time')[:10]
    classification = Classification.class_list.get_Class_list()    
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    #tags=Tag.objects.all()
    taglist=Tag.tag_list.get_Tag_list()
        
    return render_to_response('note/index_new.html',
            locals(),
            context_instance=RequestContext(request))
def tagDetail(request, tag):
    
    is_tag = True
    temp = Tag.objects.get(name=tag) #获取全部的Article对象
    #articles = Article.objects.filter(tags=tag)
    articles = temp.article_set.all()
    paginator = Paginator(articles,6)
    page_num = request.GET.get('page')
    try:
         articles = paginator.page(page_num)
    except PageNotAnInteger:
         articles = paginator.page(1)
    except EmptyPage:
         articles = paginator.page(paginator.num_pages)

    #ar_newpost = Article.objects.order_by('-publish_time')[:10]


    classification = Classification.class_list.get_Class_list()    
    #tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    taglist=Tag.tag_list.get_Tag_list()
    tagCloud=Tag.tag_list.get_Tag_list()
    #tags=Tag.objects.all()
     
    return render_to_response('note/index_new.html',
            locals(),
            context_instance=RequestContext(request))
def about(request):
  
    #ar_newpost = Article.objects.order_by('-publish_time')[:10]
    classification = Classification.class_list.get_Class_list()    
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    #tags=Tag.objects.all()
    taglist=Tag.tag_list.get_Tag_list()

    return render_to_response('blog/about.html',
            locals(),
            context_instance=RequestContext(request))
def archive(request):
    
    
    archive = Article.date_list.get_Article_OnArchive()
    
    ar_newpost = Article.objects.order_by('-publish_time')[:10]
    classification = Classification.class_list.get_Class_list()    
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    #tags=Tag.objects.all()
    taglist=Tag.tag_list.get_Tag_list()

    return render_to_response('note/archive_new.html',
            locals(),
            context_instance=RequestContext(request))
class RSSFeed(Feed) :
    title = "RSS feed "
    link = "feeds/posts/"
    description = "RSS feed - blog posts"

    def items(self):
        return Article.objects.order_by('-publish_time')

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.publish_time

    def item_description(self, item):
        return item.content
def blog_search(request):#实现对文章标题的搜索
   
    is_search = True
    #ar_newpost = Article.objects.order_by('-publish_time')[:10]
    classification = Classification.class_list.get_Class_list()    
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    #tags=Tag.objects.all()
    taglist=Tag.tag_list.get_Tag_list()

    error = False
    if 's' in request.GET:
        s = request.GET['s']
        if not s:
            return render(request,'blog/index.html')
        else:
            articles = Article.objects.filter(title__icontains = s)
            if len(articles) == 0 :
                error=True

    return render_to_response('blog/index.html',
            locals(),
            context_instance=RequestContext(request))
    #return redirect('/')

def message(request):
    
    
    classification = Classification.class_list.get_Class_list()  
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    #tags=Tag.objects.all()
    taglist=Tag.tag_list.get_Tag_list()

    return render_to_response('note/message_new.html',
            locals(),
            context_instance=RequestContext(request))

def tags(request):
    classification = Classification.class_list.get_Class_list()  
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()
    #tags=Tag.objects.all()
    taglist=Tag.tag_list.get_Tag_list()
    tag_article=Tag.tag_list.get_Article_onTag
    return render_to_response('note/tag_new.html',
            locals(),
            context_instance=RequestContext(request))

def albums(request):
    classification = Classification.class_list.get_Class_list()  
    tagCloud = json.dumps(Tag.tag_list.get_Tag_list(),ensure_ascii=False)#标签,以及对应的文章数目
    date_list = Article.date_list.get_Article_onDate()

    taglist=Tag.tag_list.get_Tag_list()

    return render_to_response('album/albumlog.html',
            locals(),
            context_instance=RequestContext(request))

   





        




        
            
