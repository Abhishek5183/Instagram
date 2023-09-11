from django.shortcuts import render,redirect
from app.forms import *
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dummy(request):
    email_2 = request.user
    print(email_2)
    userprofile_obj = UserProfile.objects.filter(phone_number = '8880969162')
    context = {'userprofile_obj' : userprofile_obj}
    print(userprofile_obj)
    return render(request, 'home.html',context)

def signup(request):
    reg_obj = UserRegForm()
    context = {'reg_obj' : reg_obj}
    if request.method == 'POST' and request.FILES:
        print('hii')
        user_obj = UserRegForm(request.POST,request.FILES)
        if user_obj.is_valid():
            username = user_obj.cleaned_data.get('username')
            password = user_obj.cleaned_data.get('password')
            password = make_password(password)
            email = user_obj.cleaned_data.get('email')
            phone_number = user_obj.cleaned_data.get('phone_number')
            image = user_obj.cleaned_data.get('image')
            UPO = UserProfile.objects.get_or_create(username = username, password = password, email = email, phone_number = phone_number, image = image)[0]
            UPO.save()
            return render(request, 'signin.html')

        return HttpResponse('Sorry')
    return render(request, 'signup.html', context)


def signin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user_obj = authenticate(email = email, password = password)
        if user_obj:
            print('Enyered')
            if user_obj.is_active:
                login(request, user_obj)
                request.session['email'] = email
                return HttpResponseRedirect(reverse('dummy'))
    return render(request,'signin.html')

@login_required
def profile(request):
    email = request.user
    userprofile_obj = UserProfile.objects.filter(email = email)
    following_count = Followers.objects.filter(email = email).count()
    profile_obj = Uploaded_images.objects.filter(user_id = email)
    post_count = Uploaded_images.objects.filter(user_id = email).count()
    context = {'profile_obj': profile_obj, 'userprofile_obj': userprofile_obj, 'following_count' : following_count, 'post_count' : post_count }
    return render(request, 'profile.html', context)

@login_required
def post(request):
    if request.method == 'POST' or request.FILES:
        image = request.FILES['img']
        email = request.user
        img_obj = Uploaded_images.objects.create(image = image, user_id = email)
        return HttpResponse('Done')
    return render(request, 'post.html')

@login_required
def search(request):
    userprofile_obj = UserProfile.objects.filter(phone_number = '8880969162')
    context = {'userprofile_obj' : userprofile_obj}
    return render(request, 'search.html',context)

@login_required
def forget_password(request):
    return render(request, 'forget_password.html')

@login_required
def followers_id(request, pk):
    temp = Followers.objects.filter(follower_id = pk)
    if temp:
        return HttpResponse('already exist')
    else:
        em = request.user
        tem = UserProfile.objects.get(email = em )
        foll = Followers.objects.create(email = tem,  follower_id  = pk, active = 1)
        foll.save()
        return HttpResponse('Done')
    
@login_required
def followers_page(request):
    email = request.user
    emails = []
    empty_queryset = UserProfile.objects.none()
    FOLOBJ = Followers.objects.filter(email = email)
    for i in FOLOBJ:
        emails.append(i.follower_id)
    print(emails)
    for i in emails:
        empty_queryset = empty_queryset | UserProfile.objects.filter(email = i)
        print(empty_queryset)
    context = {'empty_queryset' : empty_queryset}
    return render(request, 'followers_page.html', context)

@login_required
def edit_profile(request):
    email = request.user
    EDP = UserProfile.objects.filter(email = email)
    context = {'EDP' : EDP}
    if request.method == 'POST' and request.FILES:
        email = request.user
        username = request.POST['username']
        bio = request.POST['bio']
        image = request.FILES['image']
        gender = request.POST['gender']
        if image:
            UIMG = UserProfile.objects.update_or_create(email = email,defaults={'image':image})[0]
            UIMG.save()
        USOBJ = UserProfile.objects.update_or_create(email = email,defaults={'username':username, 'bio':bio, 'image':image})[0]
        USOBJ.save()
        return HttpResponseRedirect(reverse('profile'))
    return render(request, 'edit_profile.html', context)
@login_required
def story(request, email):
    temp = UserProfile.objects.filter(email = email)
    context = {'temp' : temp}
    return render(request, 'story.html', context)


@login_required
def signout(request):
    logout(request)
    return render(request, 'signin.html')
    
@login_required
def like(request):
    return render(request, 'like.html')



@login_required
def friends_profile(request, email):
    userprofile_obj = UserProfile.objects.filter(email = email)
    following_count = Followers.objects.filter(email = email).count()
    profile_obj = Uploaded_images.objects.filter(user_id = email)
    post_count = Uploaded_images.objects.filter(user_id = email).count()
    context = {'profile_obj': profile_obj, 'userprofile_obj': userprofile_obj, 'following_count' : following_count, 'post_count' : post_count }
    return render(request, 'profile.html', context)