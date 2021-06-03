from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Picture
from .forms import PictureForm
from .models import Grading
from .forms import GradingForm
from django.shortcuts import get_object_or_404
from django.db.models import Sum


global picture_form_

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
        'pictures': user_pictures,
        'user': user
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
    if request.method == 'POST':
        global profile_name
        profile_name = str(request.POST['username'])
        return redirect('view_profile')
    if request.method == 'GET':
        sort_type = 0
        try:
            sort = request.GET['sorted']
            if sort == 'general':
                sort_type = 0
            elif sort == 'meaning':
                sort_type = 1
            elif sort == 'technique':
                sort_type = 2
            elif sort == 'originality':
                sort_type = 3
        except:
            pass
    all_pictures_rating = Grading.objects.all()
    all_pictures = Picture.objects.all()
    pictures_with_rating = {}
    pictures_with_rating_to_sort = {}

    for picture in all_pictures:
        pictures_with_rating.update({picture: [[0],[0],[0]]})
        for picture_rate in all_pictures_rating:
            if picture == picture_rate.picture_id:
                pictures_with_rating[picture][0][0] += picture_rate.rate_content_meaning
                pictures_with_rating[picture][1][0] += picture_rate.rate_draw_technique
                pictures_with_rating[picture][2][0] += picture_rate.rate_originality
    
    if sort_type == 1:
        pictures = sort_pictures(0, pictures_with_rating, pictures_with_rating_to_sort)
        data = {'pictures': pictures}
    elif sort_type == 2:
        pictures = sort_pictures(1, pictures_with_rating, pictures_with_rating_to_sort)
        data = {'pictures': pictures}
    elif sort_type == 3:
        pictures = sort_pictures(2, pictures_with_rating, pictures_with_rating_to_sort)
        data = {'pictures': pictures}
    elif sort_type == 0:
        pictures = sort_pictures(3, pictures_with_rating, pictures_with_rating_to_sort)
        data = {'pictures': pictures}   
    return render(request, 'view_pic/scoreboard.html', data)


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

def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    all_gradings = Grading.objects.all()
    all_pictures = Picture.objects.all()
    data = {}
    
    user = request.user
    is_evaluate = False
    for grade in all_gradings:
        if picture == grade.picture_id:
            if user == grade.evaluating_user:
                is_evaluate = True
    
    if is_evaluate is False:
        if request.method == 'POST':
            form = GradingForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.evaluating_user = request.user
                post.picture_id = picture
                post.save()
                data.update({'rate': True})
        else:
            form = GradingForm()

        data.update({
            'picture_data': picture,
            'grading_form': form,
            'not_evaluate' : True
        })
    else:
        data = {
            'picture_data': picture,
        }

    picture_with_rating = {}
    picture_with_rating.update({picture: [[0],[0],[0]]})
    num_of_grades = 0 
    for picture_rate in all_gradings:
        if picture == picture_rate.picture_id:
            picture_with_rating[picture][0][0] += picture_rate.rate_content_meaning
            picture_with_rating[picture][1][0] += picture_rate.rate_draw_technique
            picture_with_rating[picture][2][0] += picture_rate.rate_originality
            num_of_grades += 1

    meaning_sum = picture_with_rating[picture][0][0] 
    technique_sum = picture_with_rating[picture][1][0]
    originality_sum = picture_with_rating[picture][2][0]
    try:
        mid_meaning = meaning_sum / num_of_grades
        mid_technique = technique_sum / num_of_grades
        mid_originality = originality_sum / num_of_grades
    except:
        mid_meaning = 0
        mid_technique = 0
        mid_originality = 0
    data.update({
            'meaning': meaning_sum,
            'mid_meaning': mid_meaning,
            'technique': technique_sum,
            'mid_technique': mid_technique,
            'originality': originality_sum,
            'mid_originality': mid_originality
        })
    return render(request, 'view_pic/details_view.html', data)

def sort_pictures(num_of_sort, pictures_with_rating, pictures_with_rating_to_sort):
    pictures_with_rating_sorted = {}
    pictures_sorted = []
    if num_of_sort < 3:
        for picture_rate in pictures_with_rating:
             pictures_with_rating_to_sort[picture_rate] = pictures_with_rating[picture_rate][num_of_sort]
        
        sorted_keys = sorted(pictures_with_rating_to_sort, key=pictures_with_rating_to_sort.get, reverse=True)  # [1, 3, 2]
        
        for key in sorted_keys:
            pictures_with_rating_sorted[key] = pictures_with_rating_to_sort[key]
        for key in pictures_with_rating_sorted:
            pictures_sorted.append(key)
        print(pictures_with_rating_sorted)

    else:
        for picture_rate in pictures_with_rating:
            picture_rates = pictures_with_rating[picture_rate]
            pictures_with_rating_to_sort[picture_rate] = picture_rates[0][0] + picture_rates[1][0] + picture_rates[2][0]
        sorted_keys = sorted(pictures_with_rating_to_sort, key=pictures_with_rating_to_sort.get, reverse=True)  # [1, 3, 2]
        
        for key in sorted_keys:
            pictures_with_rating_sorted[key] = pictures_with_rating_to_sort[key]
        for key in pictures_with_rating_sorted:
            pictures_sorted.append(key)
        print(pictures_with_rating_sorted)

    return pictures_sorted