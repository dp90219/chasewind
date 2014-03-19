from django.conf.urls import patterns, url

urlpatterns = patterns('blog.views',
        url(r'^$', 'index', name='index'),
        url(r'^posts/$', 'post', name='post'),
        url(r'^posts/(?P<post_title>\w+)/$', 'post', name='post'),
        url(r'^register/$', 'register', name='register'),
        url(r'^login/$', 'user_login', name='login'),
        url(r'^logout/$', 'user_logout', name='logout'),
        url(r'^profile/$', 'profile', name='profile'),
        url(r'^search/$', 'search', name='search'),
        url(r'^category/(?P<category_name>\w+)/$', 'category', name='category'),
        url(r'^auto_add_page/', 'auto_add_page', name='auto_add_page'),
        url(r'^search_ajax/', 'search_ajax', name='search_ajax'),
        url(r'goto/', 'track_url', name='goto'),
        )
