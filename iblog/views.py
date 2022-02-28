from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import USERBLOG
from django.contrib.auth.decorators import login_required

# Create your views here.


def index(request):
    return render(request,"iblog/index.html")

def register(request):

    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

        if User.objects.filter(username=username):
            context={'msg':'Username already exists'}
            return render(request,'iblog/register.html',context)

        if User.objects.filter(email=email):
            context={'msg':'Email already exists'}
            return render(request,'iblog/register.html',context)

        user = User.objects.create_user(username, email, password)
        user.save()
        context={'msg':'Account created'}
        return render(request, "iblog/signin.html", context)
    return render(request, "iblog/register.html")


def signin(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            context={'msg':'User Not identified'}
            return render(request,'iblog/signin.html',context)
    return render(request,'iblog/signin.html')

def signout(request):
    logout(request)
    context={'msg':"Successfully logged out"}
    return render(request,'iblog/index.html',context)
  

@login_required(login_url='signin')
def writeblogs(request):
    if request.method=="POST":
        if request.user.is_authenticated:
            title=request.POST['title']
            tag=request.POST['tag']
            description=request.POST['description']
            author=request.user
            user=request.user
            userblog=USERBLOG(title=title,author=author,description=description,tag=tag,user=user)
            userblog.save()
            context={'msg':'You have successfully posted a blog'}
            return render(request,'iblog/writeblogs.html',context)
        

    return render(request,'iblog/writeblogs.html')

@login_required(login_url='signin')
def yourblog(request):
    if request.user.is_authenticated:
        politics=USERBLOG.objects.filter(tag="Politics")
        tech=USERBLOG.objects.filter(tag="Tech")
        others=USERBLOG.objects.filter(tag="Others")
        sports=USERBLOG.objects.filter(tag="Sports")
        user=request.user
        context={
            'user':user,
            'tech':tech,
            "others":others,
            'sports':sports,
            'politics':politics

        }
        return render(request,'iblog/yourblog.html',context)

@login_required(login_url='signin')  
def myblog(request):
    if request.user.is_authenticated:
        user=request.user
        allblogs=USERBLOG.objects.filter(user=user)
        
        return render(request,'iblog/myblog.html',{'allblogs':allblogs,'user':user})


def blogpost(request,id):
    text=USERBLOG.objects.filter(id=id).first()  
    context={'text':text}
    return render(request,'iblog/blogpost.html',context)

def deleteblog(request,id):
    text=USERBLOG.objects.filter(id=id).first()  
    text.delete()
    return redirect('myblog')


def aboutus(request):
    return render(request,'iblog/aboutus.html')

def profile(request):
    if request.user.is_authenticated:
        user=request.user
        details=User.objects.filter(username=user).first()
       
    return render(request,'iblog/profile.html',{'details':details})


def search(request):
   
    query=request.GET['query']
    if len(query)>78:
        allPosts=USERBLOG.objects.none()
    else:
        allPostsTitle= USERBLOG.objects.filter(title__icontains=query)
        # allPostsAuthor= USERBLOG.objects.filter(author__icontains=query)
        allPostsdescription =USERBLOG.objects.filter(description__icontains=query)
        allPosts=  allPostsTitle.union(allPostsdescription)
        # return render(request, 'iblog/search.html')
    if allPosts.count()==0:
        context = {'msg':"No search result found"}
        return render(request, 'iblog/search.html', context)

    params={'allPosts': allPosts, 'query': query}
    return render(request, 'iblog/search.html', params)
