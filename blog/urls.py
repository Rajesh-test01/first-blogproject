from django.urls import path
from blog import views
from . import api_views
from rest_framework.authtoken.views import obtain_auth_token

# urlpatterns = [
#     # DASHBOARD (single entry for all roles)
#     path("dashboard/", views.dashboard_view, name="dashboard"),

# ]
urlpatterns = [
    
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("admin-dashboard/", views.admin_dashboard, name='admin_dashboard'),
    path("dashboard/create/", views.blog_create, name="blog_create"),
    path("dashboard/edit/<int:id>/", views.blog_edit, name="blog_edit"),
    path("dashboard/delete/<int:id>/", views.blog_delete, name="blog_delete"),



    # ================= AUTH =================
    path('login/', views.login_view, name='login'),
    # path('register_view/', views.register_view, name='register_view'),
    path('logout/', views.logout_view, name='logout'),

    # ================= BLOG PAGES =================
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
    path('search/', views.search_blog, name='search_blog'),
    path('contact/', views.contact, name='contact'),
    path("see-our-blogs/", views.see_our_blogs, name="see_our_blogs"),
    path("thank_you/", views.thank_you, name="thank_you"),

    # ================= HOME (LAST) =================
    path('', views.blog_list, name='blog_list'),
]

# ================= API URLs =================

urlpatterns += [
    path("api/login/", obtain_auth_token, name="api_login"),
    path("api/blogs/", api_views.blog_list_api),
    path("api/blogs/<int:id>/", api_views.blog_detail_api),
    path("api/categories/", api_views.category_list_api),
    path("api/category/<int:id>/blogs/", api_views.category_blogs_api),
    path("api/blogs/<int:blog_id>/comments/", api_views.blog_comment_api),
]

