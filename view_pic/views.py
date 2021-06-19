from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Picture
from .forms import PictureForm


@login_required
def upload(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.current_user = request.user
            post.save()
            return redirect('home')
    else:
        form = PictureForm()

    data = {
        'form': form
    }
    return render(request, 'view_pic/upload.html', data)


@login_required
def view_home(request):
    pictures = Picture.objects.all()
    if request.method == 'POST':
        global profile_name
        profile_name = str(request.POST['username'])
        return redirect('view_profile')
    data = {
        'pictures': pictures
    }
    return render(request, 'view_pic/view_home.html', data)


@login_required
def view_your_profile(request):
    user = request.user
    all_pictures = Picture.objects.all()
    user_pictures = []
    for picture in all_pictures:
        if picture.current_user == user:
            user_pictures.append(picture)
    data = {
        'pictures': user_pictures
    }
    return render(request, 'view_pic/view_your_profile.html', data)

@login_required
def view_profile(request):
    all_pictures = Picture.objects.all()
    user_pictures = []
    try:
        user = request.GET['user_to_see']
        for picture in all_pictures:
            if str(picture.current_user) == user:
                user_pictures.append(picture)
    except:
        user = profile_name
        for picture in all_pictures:
            if str(picture.current_user) == user:
                user_pictures.append(picture)
    data = {
        'pictures': user_pictures,
        'user': user
    }
    return render(request, 'view_pic/view_profile.html', data)

@login_required
def view_scoreboard(request):
    return render(request, 'view_pic/dummy.html')


@method_decorator(login_required, name="dispatch")
class PictureDeleteView(DeleteView):
    model = Picture
    success_url = '/view_pic/'
    template_name = 'view_pic/picture_delete.html'


@method_decorator(login_required, name="dispatch")
class PictureUpdateView(UpdateView):
    model = Picture
    template_name = 'view_pic/upload.html'
    form_class = PictureForm
    success_url = '/view/'


class PictureDetailView(DetailView):
    model = Picture
    template_name = 'view_pic/details_view.html'
    context_object_name = 'picture_data'
