from winreg import QueryInfoKey
from django.http import QueryDict
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

import blog
from .models import Blog , Comment
from .forms import BlogForm
from .models import Contact
from accounts.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .models import See_Our_Blogs
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib.auth import logout
from .forms import BlogForm





def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(blogs,settings.MAX_PAGE_LIMIT)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    return render(request, 'blog_list.html', {'blogs': blogs})

def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)

    related_blogs = blog.object.filter(
        category = blog.category
    ).exclude(id=blog.id)[:4]      # 👈 same category, exclude current blog

    if request.method == "POST" and request.user.is_authenticated:
        text = request.POST.get("text")
        Comment.objects.create(
            blog=blog,
            User=request.user,
            text=text
        )
        return redirect("blog_detail.html", id=blog.id)
    return render(request,"blog_detail.html",{
        blog:blog,
        related_blogs:related_blogs
    })
    

@login_required
def blog_edit(request, id):
    blog = get_object_or_404(Blog, id=id)

    if blog.owner != request.user:
        return redirect("dashboard")

    form = BlogForm(request.POST or None, request.FILES or None, instance=blog)
    if form.is_valid():
        form.save()
        return redirect("dashboard")

    return render(request, "dashboard/blog_create.html", {
        "form": form
    })

@login_required
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.owner = request.user
            blog.save()
            return redirect("dashboard")
    else:
        form = BlogForm()

    return render(request, "dashboard/blog_create.html", {
        "form": form
    })

@login_required

def dashboard_view(request):
     user = request.user
     blogs = Blog.objects.filter(owner=user)
     comments = Comment.objects.filter(blog__owner=user)\
     .prefetch_related("comments","comments_user")

     return render(request,"dashboard/dashboard.html",{
         "blogs":blogs,
         "Comments":comments,
         "user_role":user.role,
     })
     

@login_required
def blog_delete(request, id):
    blog = get_object_or_404(Blog, id=id)

    if blog.owner != request.user:
        return redirect("dashboard")

    blog.delete()
    return redirect("dashboard")


# ========= search ========

def search_blog(request):
    query = request.GET.get("q")
    results = []

    if query:
        results = Blog.objects.filter(title__icontains=query)

    context = {
        "results": results,
        "query": query
    }

    return render(request, "search.html", context)

# =============contact==========

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")
        message = request.POST.get("message")

        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            address=address,
            message=message
        )
        messages.success(request, "Message submitted successfully!")
        return redirect("contact")  # reload page after submit

    return render(request, "contact.html")


# ===========login view===========



def login_view(request):
    if request.user.is_authenticated:
       return redirect("dashboard")

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            next_url = request.GET.get("next")
            return redirect(next_url if next_url else "dashboard")

        else:
            return render(request, "login.html", {
                "error": "Invalid email or password"
            })

    # ==== (GET request)
    return render(request, "login.html")
            


# =======register=========

def register_view(request):
    if request.method =="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
   
    #    ==username already exists=======
        if User.objects.filter(username=username).exists():
            messages.error(request, "username already exists")
            return redirect("register_view")


    # ===email already exists====
        if User.objects.filter(email=email).exists():
            messages.error(request, "email already exists")
            return redirect("register_view")
        
        # ===create user===

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )


        messages.success(request,"Registation successful. please join.")
        return redirect("login")

    
    return render(request,"register.html")

# ======= email view ( in footer)=====

def see_our_blogs(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if email:
            if See_Our_Blogs.objects.filter(email=email).exists():
                messages.warning(request, "You are already subscribed.")
                return redirect(request.META.get("HTTP_REFERER", "/"))
            else:
                See_Our_Blogs.objects.create(email=email)
                return redirect("thank_you")

    return redirect("/")   

# ====== thank you======

def thank_you(request):
    return render(request, "blog/thank_you.html")


# ======= comments on blog=====

def blog_detail(request, id):
    blog = get_object_or_404(Blog, id=id)

    # ✅ WHEN USER POSTS A COMMENT
    if request.method == "POST":
        if request.user.is_authenticated:
            text = request.POST.get("text")

            Comment.objects.create(
                blog=blog,
                user=request.user,
                text=text
            )

            return redirect("blog_detail", id=blog.id)

    return render(request, "blog_detail.html", {
        "blog": blog
    })


# ======= logout========
def logout_view(request):
    logout(request)
    return redirect("login")


    # ========admin--dashboard=====

@login_required
def admin_dashboard(request):

    if not request.user.is_staff:
        return redirect("dashboard") 
    

    total_users = User.objects.count()
    total_blogs = User.objects.count()
    total_comments = User.objects.count()

    users = User.objects.all()

    return render(request, "dashboard/admin_dashboard.html", {
        "total_users": total_users,
        "total_blogs": total_blogs,
        "total_comments": total_comments,
        "users": users,
    })
