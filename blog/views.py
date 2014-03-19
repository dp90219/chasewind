from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from blog.models import Category, Post
# Create your views here.

def get_archives():
    archives = Category.objects.all().order_by('name')
    return archives
from datetime import datetime
def index(request):
    context = RequestContext(request)
    posts = Post.objects.all().order_by('-create_time')
    context_dict = {'posts': posts}

    context_dict['archives'] = get_archives()

    if request.session.get('last_visit'):
        last_visit_time = request.session.get('last_visit')
        visits = request.session.get('visits', 0)
        last_time = datetime.strptime(last_visit_time[: -7], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_time).seconds > 3:
            request.session['last_visit'] = str(datetime.now())
            request.session['visits'] = visits + 1
    else:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = 1
    return render_to_response('blog/index.html', context_dict,  context)

def post(request, post_title=''):
    context = RequestContext(request)
    context_dict = {'archives': get_archives()}
    if not post_title:
        posts = Post.objects.order_by('-create_time')
        context_dict['posts'] = posts
        return render_to_response('blog/post_index.html', context_dict, context)
    else:
        post = Post.objects.get(title=post_title)
        context_dict['post'] = post

        return render_to_response('blog/post.html', context_dict, context)

from django.contrib.auth.models import User
from blog.forms import UserForm
def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            registered = True
            return HttpResponse("Now you're reigstered")
        else:

            print user_form.errors
    else:
        user_form = UserForm()

    context_dict = {'archives': get_archives()}
    context_dict['user_form'] = user_form
    context_dict['registered'] = registered

    return render_to_response('blog/register.html', context_dict, context)

    
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username, password = request.POST['username'], request.POST['password']

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('/blog/')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print 'Invalid login details {0}, {1}'.format(username, password)
            return HttpResponse("Invalid login details supplied.")

    else:
        context_dict = {'archives': get_archives()}
        return render_to_response('blog/login.html', context_dict, context)
    
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
@login_required
def user_logout(request):
    logout(request)
    return redirect('/blog/')
        
    
@login_required
def profile(request):
    context = RequestContext(request)
    last_visit = request.session.get('last_visit', 0)
    visits = request.session.get('visits', 0)
    context_dict = {'archives': get_archives()}
    context_dict['last_visit'] = last_visit
    context_dict['visits'] = visits
    return  render_to_response('blog/profile.html', context_dict, context)

from blog.search import run_query
@login_required
def search(request):
    context = RequestContext(request)
    context_dict = {'archives': get_archives()}
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            result_list = run_query(query)
            context_dict['result_list'] = result_list
    return render_to_response('blog/search.html', context_dict, context)


def category(request, category_name):
    context = RequestContext(request)
    context_dict = {'archives': get_archives()}
    category = Category.objects.get(name=category_name)
    if category:
        posts = Post.objects.filter(category=category)
        context_dict['posts'] = posts
        return render_to_response('blog/category.html', context_dict, context)
    

@login_required
def auto_add_page(request):
    context = RequestContext(request)
    context_dict = {'archives': get_archives()}
    category_name = 'collect'
    author = context['user'].username
    print author
    if request.method == 'GET':
        title = request.GET['title']
        url = request.GET['url']
        summary = request.GET['summary']
        print title, url, summary
        category = Category.objects.get(name=category_name)
        p = Post.objects.get_or_create(category_id=category.id, title=title, author=author, url=url, summary=summary)
        context_dict['posts'] = Post.objects.filter(category=category)

    return render_to_response('blog/category.html', context_dict, context)

@login_required
def search_ajax(request):
    context = RequestContext(request)
    context_dict = {'archives': get_archives()}
    
    if request.method == 'GET':
        query = request.GET['query'].strip()
        if query:
             result_list = run_query(query)
             context_dict['result_list'] = result_list
    return render_to_response('blog/search_ajax.html', context_dict, context)
        


from django.shortcuts import redirect
def track_url(request):
    post_id = None
    url = '/blog/posts'
    if request.method == "GET":
        print "has get"
        if 'post_id' in request.GET:
            print 'has post_id'
            post_id = request.GET['post_id']
            try:
                post = Post.objects.get(id=post_id)
                print 'enter in '
                post.views = post.views + 1
                url = post.url
                post.save()
            except:
                pass
    return redirect(url)


        
   
