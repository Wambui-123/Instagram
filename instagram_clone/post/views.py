from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.views.generic import ListView, DetailView, CreateView

from post.models import Stream, Post, Tag, Likes
from post.forms import NewPostForm
from django.views import generic
from comment.forms import CommentForm
from comment.models import Comment


from django.contrib.auth.decorators import login_required

from django.urls import reverse
from authy.models import Profile


class IndexView(generic.ListView):
    template_name = "index.html"
    context_object_name = "post_items"
    
    def get_queryset(self):
      return Post.objects.order_by("-posted")
  

class PostDetailsView(generic.DetailView):
    model = Post
    
    template_name = "post_detail.html"
    def get_context_data(self, **kwargs):
        context_object_name = "post_items"
        context = super().get_context_data(**kwargs)
        context["comment"] = CommentForm(self.request.POST or None)
        return context

# Create your views here.
# @login_required
# def index(request):
# 	user = request.user
# 	posts = Stream.objects.filter(user=user)


# 	group_ids = []

# 	for post in posts:
# 		group_ids.append(post.post_id)
  		
# 	post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')		
# 	print(post_items.values())
# 	template = loader.get_template('index.html')

# 	context = {
# 		'post_items': post_items,

# 	}

# 	return HttpResponse(template.render(context, request))

# def PostDetails(request, post_id):
# 	post = get_object_or_404(Post, id=post_id)
# 	user = request.user
# 	profile = Profile.objects.get(user=user)
	
# 	if request.user.is_authenticated:
# 		profile = Profile.objects.get(user=user)


# 	template = loader.get_template('post_detail.html')

# 	context = {
# 		'post':post,
# 		'profile':profile,
# 	}

# 	return HttpResponse(template.render(context, request))


@login_required
def NewPost(request):
    user = request.user.id
    tags_objs = []
    
    if request.method == 'POST':
        form = NewPostForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.cleaned_data.get('picture')
            caption = form.cleaned_data.get('caption')
            tags_form = form.cleaned_data.get('tags')
            
            tags_list = list(tags_form.split(','))
            
            for tag in tags_list:
                t, created = Tag.objects.get_or_create(title=tag)
                tags_objs.append(t)
                
            p, created = Post.objects.get_or_create(picture=picture, caption=caption, user_id=user) 
            p.tags.set(tags_objs) 
            p.save()
            return redirect('index')
        
    else:
        form = NewPostForm()
    
    context = {
        'form': form,
    }    
    
    return render(request, 'newpost.html', context)

def tags(request, tag_slug):
	tag = get_object_or_404(Tag, slug=tag_slug)
	posts = Post.objects.filter(tags=tag).order_by('-posted')

	template = loader.get_template('tag.html')

	context = {
		'posts':posts,
		'tag':tag,
	}

	return HttpResponse(template.render(context, request))



@login_required
def like(request, post_id):
	# user = request.user
	post = get_object_or_404(Post, pk=post_id)
	post.likes += 1
	post.save()

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))

@login_required
def favorite(request, post_id):
	user = request.user
	post = Post.objects.get(id=post_id)
	profile = Profile.objects.get(user=user)

	if profile.favorites.filter(id=post_id).exists():
		profile.favorites.remove(post)

	else:
		profile.favorites.add(post)

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))