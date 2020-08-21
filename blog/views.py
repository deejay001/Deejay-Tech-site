from django.shortcuts import render, get_object_or_404
from .models import Post, Category
from django.views import generic
from .forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.


def home_page(request):
    return render(request, 'index.html')


def post_list(request):
    post = Post.objects.filter(status=1).order_by('-created_on')
    recent = Post.objects.filter(status=1).order_by('-created_on')[1:]
    category = Category.objects.all()

    paginator = Paginator(post, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_l = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        post_l = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_l = paginator.page(paginator.num_pages)

    return render(request, 'blog.html', {'post_list': post_l,
                                         'page': page,
                                         'category': category,
                                         'recent': recent,
                                         })


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    paginate_by = 3
    template_name = 'blog.html'


def post_detail(request, slug):
    template_name = "post_detail.html"
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()

    else:
        comment_form = CommentForm()

    recent = Post.objects.filter(status=1).order_by('-created_on')[1:]
    category = Category.objects.all()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new comment': new_comment,
                                           'comment_form': comment_form,
                                           'category': category,
                                           'recent': recent,
                                           })


def category_view(request, title):
    category = get_object_or_404(Category, title=title)
    posts = category.post.filter(status=1)

    recent = Post.objects.filter(status=1).order_by('-created_on')[1:]
    categor = Category.objects.all()

    return render(request, 'blog.html', {'post_list': posts,
                                         'recent': recent,
                                         'category': categor,
                                         })
