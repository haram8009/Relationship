from django.shortcuts import render,get_object_or_404,redirect
from django.core.paginator import Paginator
from .models import Blog, Comment, Tag
from .forms import BlogForm


def home(request):
    blogs = Blog.objects.all()
    paginator = Paginator(blogs, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'home.html',{'page_obj':page_obj})

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    comments = Comment.objects.filter(blog=blog)

    tags = blog.tag.all()
    return render(request,'detail.html',{'blog':blog, 'comments':comments, 'tags':tags})

def new(request):
    tags = Tag.objects.all()
    return render(request,'new.html', {'tags':tags})

def create(request):
    new_blog = Blog()
    new_blog.title = request.POST.get('title')
    new_blog.content = request.POST.get('content')
    new_blog.image = request.FILES.get('image')
    new_blog.author = request.user

    new_blog.save()

    tags = request.POST.getlist('tags')
    for tag_id in tags:
        tag = Tag.objects.get(id=tag_id)
        new_blog.tag.add(tag) # add 내부에서 save를 알아서 해줘서 이 뒤에 save 또 안해도 됨
    return redirect('detail', new_blog.id)

def edit(request, blog_id):
    edit_blog = get_object_or_404(Blog, pk=blog_id)

    if request.user != edit_blog.author:
        return redirect('home')
 
    return render(request, 'edit.html', {'edit_blog':edit_blog})


def update(request, blog_id):
    old_blog = get_object_or_404(Blog, pk=blog_id)
    old_blog.title = request.POST.get('title')
    old_blog.content = request.POST.get('content')
    old_blog.image = request.FILES.get('image')
    old_blog.save()
    return redirect('detail', old_blog.id)

# def update(request, blog_id):
#     old_blog = get_object_or_404(Blog, pk=blog_id)
#     form = BlogForm(request.POST, instance=old_blog)

    # 클라이언트가 유효한 값을 입력한 경우
    # if form.is_valid():
    #     new_blog = form.save(commit=False)
    #     new_blog.save()
    #     return redirect('detail', old_blog.id)

    # return render(request, 'new.html', {'old_blog':old_blog})


def delete(request, blog_id):
    delete_blog = get_object_or_404(Blog, pk=blog_id)

    # TODO: 본인이 쓴 글이 아니면 삭제 안되게하기

    delete_blog.delete()
    return redirect('home')

def create_comment(request, blog_id):
    comment = Comment()
    comment.content=request.POST.get('content')
    comment.blog = get_object_or_404(Blog, pk=blog_id)
    comment.author = request.user
    comment.save()
    return redirect('detail', blog_id)

def new_comment(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'new_comment.html', {'blog':blog})
