from django.db import models
from django.conf import settings
from accounts.models import User 

# ====== category ====( define in blog)====
    
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Blog(models.Model):

   

    title = models.CharField(max_length=200)
    short_desc = models.TextField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to="blog_images/", blank=True, null=True)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

   

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


    
    # ====== Contact===

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    # ======See_Our_Blogs======

class See_Our_Blogs(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email 
    
    #  ======Comment====

class Comment(models.Model):
    blog = models.ForeignKey(
        Blog,
        related_name="comments",
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
       
    def __str__(self):
      return f"{self.user.email} on {self.blog.title}"


#   ========loginuser============

class LoginUser(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
         on_delete=models.CASCADE
        )
    login_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.login_date}"
