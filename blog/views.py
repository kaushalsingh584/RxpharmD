from datetime import timezone
from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.views.generic.edit import UpdateView
from blog.forms import PostForm,CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required #for functions based views
from django.contrib.auth.mixins import LoginRequiredMixin #for functions based views
from django.views.generic import TemplateView,ListView,DetailView,CreateView,DeleteView
from blog.models import Post,Comment
# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    # this function is actually a query to retrieve data where ilt means "less than or equal to".there are many such as __exact ,__iexact ,etc
    # select * form blog_Post where  publish_date <='2006-01-01' ;
    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    # here both loginRequiredMixins and CreateView are classes from which we r going to inherit methods
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model  = Post

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model  = Post

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
     #this waits till the blog is actually deleted

class DraftListView(LoginRequiredMixin,ListView):
    login_url  = '/login/'
    redirect_field_name = 'post/post_list.html'
    mode = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull = True).order_by('created_date')


    
# functions to add comments (which require primary key as parameter)

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect('post_detail',pk = post.pk)
    else:
        form = CommentForm()

    return render(request,'blog/comment_form.html',{'form':form})


@login_required
def comment_approve(request,pk):
    comment  = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail.html',pk = comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk)
    post_pk = comment.post.pk #saving for passing to redirect later
    comment.delete()
    return  redirect('post_detail.html',pk=post_pk)

@login_required
def post_publish(request,pk):
    if (pk!=0):
        print("value got ")
    # post_pk = pk
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)


#     @login_required
# def post_publish(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.publish
#     return redirect('post_detail', pk=pk)

