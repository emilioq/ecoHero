# by EMILIO
# Contains all the 'views' for the  website.
# when a user on a website requests a page, this page determines how the site
# will respond to the request based on various conditions.

from django.shortcuts import redirect
from django.shortcuts import render
from django.http import HttpResponse
from .form import RegisterForm

from django.conf import settings
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib.auth.hashers import make_password, check_password

import datetime
from .models import Post
from .models import PostApproval
from .models import PostStatus
from .models import PostSubmit

from .models import RegisteredUser
from .models import Admin
from .models import Agent
from django.db.models import Q
#from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test



#Views for the 'About' portion of the site
def aboutIndex(request):
    return render(request, 'about/index.html', context={})
def aboutAndrew(request):
    return render(request, 'about/aboutAndrew.html', context={})
def aboutPreston(request):
    return render(request, 'about/aboutPreston.html', context={})
def aboutSahas(request):
    return render(request, 'about/aboutSahas.html', context={})
def aboutConnor(request):
    return render(request, 'about/aboutConnor.html', context={})
def aboutEmilio(request):
    return render(request, 'about/aboutEmilio.html', context={})
def aboutMarcelo(request):
    return render(request, 'about/aboutMarcelo.html', context={})
def aboutPeitong(request):
    return render(request, 'about/aboutPeitong.html', context={})



#Home Page
#If user is logged in -> indexUser
#If user is guest -> index2
def index2(request):
    approvedIDs = PostApproval.objects.filter(approval=1).values_list('post', flat=True).order_by('-post')
    posts = Post.objects.filter(post_id__in = approvedIDs).order_by('-time')

    if request.user.is_authenticated:
        user = RegisteredUser.objects.get(username = request.user)
        if Admin.objects.filter(user = user.user_id).exists():
            return render(request, 'indexAdmin.html', context={'posts': posts[:8]})
        elif Agent.objects.filter(user = user.user_id).exists():
            return render(request, 'indexAgent.html', context={'posts': posts[:8]})
        else:
            return render(request, 'indexUser.html', context={'posts': posts[:8]})
    else:
        return render(request, 'index2.html', context={'posts': posts[:8]})



#Submitting a hazard
#HazardUpload brings you to submission page
#HazardUpload2 submits form
def HazardUpload(request):
    return render(request, 'hazardUpload.html', context={})

def HazardUpload2(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')

        if(title == ''):
            return render(request, 'hazardUpload.html', context={'match': 'Please enter a title.', 'title': title, 'description': description, 'location': location})
        if(location == ''):
            return render(request, 'hazardUpload.html', context={'match': 'Please enter a location.', 'title': title, 'description': description, 'location': location})


    else:
        title = 'error'
        description = 'error'
        location = 'error'

    new_id = (Post.objects.all().count()) + 1
    now = datetime.datetime.now()
    submission = Post()

    postApproval = PostApproval()
    postStatus = PostStatus()
    postSubmit = PostSubmit()

    user = request.user

    submission.title = title
    submission.description = description
    submission.location = location
    submission.type = request.POST.get('category')

    if (len(request.FILES) != 0):
        image = request.FILES['image']
        image.name = str(new_id) + '.jpg'
        submission.image = image

    submission.post_id = new_id
    #submission.approval = 0
    #submission.status = 'PENDING'
    submission.time = now
    #submission.save()

    if request.user.is_authenticated:
        submission.user = user
        submission.save()

        postApproval.post = submission
        postApproval.approval = 0
        postApproval.save()

        postStatus.post = submission
        postStatus.status = 'PENDING'
        postStatus.save()

        postSubmit.post = submission
        postSubmit.user = user
        postSubmit.time = now
        postSubmit.save()

        return render(request, 'hazardUpload.html', context={'matchGreen': 'Hazard posted successfully.'})
    else:

        username = request.POST.get('username')
        password = request.POST.get('password')
        confpassword = request.POST.get('confpassword')

        if username is None:
            return render(request, 'hazardUpload.html', context={'match': 'You must be logged in to submit. You can register below.',
                                                                'guest': 'true', 'title': title, 'description': description, 'location': location,
                                                                'username':'', 'password':'', 'confpassword':''})

        if RegisteredUser.objects.filter(username = username).exists():
            return render(request, 'hazardUpload.html', context={'match2': 'Username already exists',
                                                                'guest': 'true', 'title': title, 'description': description, 'location': location,
                                                                'username': username, 'password': password, 'confpassword': confpassword})
        if password != confpassword:
            return render(request, 'hazardUpload.html', context={'match2': 'Passwords do not match',
                                                                'guest': 'true', 'title': title, 'description': description, 'location': location,
                                                                'username': username, 'password': '', 'confpassword': ''})
        if len(username) <= 3:
            return render(request, 'hazardUpload.html', context={'match2': 'Username must be at least 4 character',
                                                                'guest': 'true', 'title': title, 'description': description, 'location': location,
                                                                'username': username, 'password': password, 'confpassword': confpassword })
        if len(password) <= 4:
            return render(request, 'hazardUpload.html', context={'match2': 'Password must be at least 5 character',
                                                                'guest': 'true', 'title': title, 'description': description, 'location': location,
                                                                'username': username, 'password': password, 'confpassword': confpassword })

        user = RegisteredUser()

        user.user_id = (RegisteredUser.objects.all().count()) + 1
        user.username = username
        user.password = password
        user.register_date = now
        user.save()
        auth_login(request, user)

        return render(request, 'hazardUpload.html', context={'matchGreen': 'Account created. You may now submit.', 'title': title, 'description': description, 'location': location})





#Loggin in and Logging out
#checks if username exists and if password match
@user_passes_test(lambda u: u.is_anonymous)
def login(request):
    if request.method == 'POST':
        lg_username = request.POST.get('lg_username')
        lg_password = request.POST.get('lg_password')

        if RegisteredUser.objects.filter(username = lg_username).exists():
            db_user = RegisteredUser.objects.get(username = lg_username)

            if db_user.ban == 'PERMA':
                return render(request, 'login/login.html', context={'match': 'The account is permanently banned'})
            if db_user.ban == 'TEMP':
                return render(request, 'login/login.html', context={'match': 'The account is temporarily banned'})

            if check_password(lg_password, db_user.password):
                auth_login(request, db_user)

                approvedIDs = PostApproval.objects.filter(approval=1).values_list('post', flat=True).order_by('-post')
                posts = Post.objects.filter(post_id__in = approvedIDs).order_by('-time')

                if Admin.objects.filter(user = db_user.user_id).exists():
                    return render(request, 'indexAdmin.html', context={'posts': posts[:8]})
                elif Agent.objects.filter(user = db_user.user_id).exists():
                    return render(request, 'indexAgent.html', context={'posts': posts[:8]})
                else:
                    return render(request, 'indexUser.html', context={'user': db_user, 'posts': posts[:8]})
            else:
                return render(request, 'login/login.html', context={'match': 'Incorrect password'})

        else:
            return render(request, 'login/login.html', context={'match': 'Username does not exist'})

    else:
        return render(request, 'login/login.html', context={})

def logout(request):
    auth_logout(request)
    approvedIDs = PostApproval.objects.filter(approval=1).values_list('post', flat=True).order_by('-post')
    posts = Post.objects.filter(post_id__in = approvedIDs).order_by('-time')
    return render(request, 'index2.html', context={'posts': posts[:8]})



#Account Registration
#register brings you to registration page
#register2 submits register form if valid
@user_passes_test(lambda u: u.is_anonymous)
def register(request):
    return render(request, 'login/register.html', context={})

@user_passes_test(lambda u: u.is_anonymous)
def register2(request):
    reg_username = ""
    reg_password = ""
    reg_confPassword = ""

    if request.method == 'POST':
        reg_username = request.POST.get('reg_username')
        reg_password= request.POST.get('reg_password')
        reg_confPassword = request.POST.get('reg_password_confirm')
    else:
        reg_username = 'error'
        reg_password = 'error'
        reg_confPassword = 'error2'

    if RegisteredUser.objects.filter(username = reg_username).exists():
        return render(request, 'login/register.html', context={'match': 'Username already exists'})
    if reg_password != reg_confPassword:
        return render(request, 'login/register.html', context={'match': 'Passwords do not match'})
    if len(reg_username) <= 3:
        return render(request, 'login/register.html', context={'match': 'Username must be at least 4 character'})
    if len(reg_password) <= 4:
        return render(request, 'login/register.html', context={'match': 'Password must be at least 5 character'})

    else:
        now = datetime.datetime.now()
        user = RegisteredUser()

        user.user_id = (RegisteredUser.objects.all().count()) + 1
        user.username = reg_username
        user.password = make_password(reg_password)
        user.register_date = now
        user.save()

        return render(request, 'login/login.html', context={'match2': 'Account created. Please log in.'})



#Forgot Password
#!! CURRENTLY DOES NOT FUNCTION !!
def forgotpassword(request):
    return render(request, 'login/forgotpassword.html', context={})



#Hazard Search Results
#Gets user search input and matches with Posts' title, location, and description in database
#Checks if the Post ID is approved (approval = 1)
#Matches category based on dropdown option
#Finally, sorts by oldest or newest based on dropdown option
def searchresults2(request):
    if request.method == 'POST':
        search_input = request.POST.get('search')
        category = request.POST.get('category')
        sort = request.POST.get('sort')
    else:
        search_input = ""
        category = 'none'
        sort = "newest"

    approvedIDs = PostApproval.objects.filter(approval=1).values_list('post', flat=True)

    if category == 'Chemical':
        posts = Post.objects.filter(Q(post_id__in = approvedIDs) & (Q(type__icontains = 'CHEMICAL') & (Q(title__icontains = search_input)|Q(location__icontains = search_input)|Q(description__icontains = search_input))))
    elif category == 'Biological':
        posts = Post.objects.filter(Q(post_id__in = approvedIDs) & (Q(type__icontains = 'BIOLOGICAL') & (Q(title__icontains = search_input)|Q(location__icontains = search_input)|Q(description__icontains = search_input))))
    elif category == 'Physical':
        posts = Post.objects.filter(Q(post_id__in = approvedIDs) & (Q(type__icontains = 'PHYSICAL') & (Q(title__icontains = search_input)|Q(location__icontains = search_input)|Q(description__icontains = search_input))))
    else:
        posts = Post.objects.filter(Q(post_id__in = approvedIDs) & (Q(title__icontains = search_input)|Q(location__icontains = search_input)|Q(description__icontains = search_input)))



    if sort == "oldest":
        posts = posts.order_by('post_id')
    else:
        posts = posts.order_by('-post_id')

    return render(request, 'searchresults2.html', context={'posts': posts, 'input': search_input, 'category': category, 'sort': sort})


#Hazard Post
#displays more detailed information on a hazard posting
def hazardPost(request, id):
    post = Post.objects.get(post_id=id)

    if PostApproval.objects.filter(post = id).exists():
        if PostApproval.objects.get(post = id).approval == 1:
            return render(request, 'hazardPost.html', context={'post': post})
        else:
            return redirect('index2')
    else:
        return redirect('index2')




#Admin Dashboard
#Displays all pending posts to be approved
@user_passes_test(lambda u: Admin.objects.filter(user = u.user_id).exists())
def admin(request):
    unapprovedIDs = PostApproval.objects.filter(approval=0).values_list('post', flat=True)
    posts = Post.objects.filter(post_id__in = unapprovedIDs).order_by('time')
    return render(request, 'adminResults.html', context={'posts': posts})

#Admin listing for post deletion
@user_passes_test(lambda u: Admin.objects.filter(user = u.user_id).exists())
def adminDelete(request):
    if request.method == 'POST':
        search_input = request.POST.get('search')
        category = request.POST.get('category')
        sort = request.POST.get('sort')
    else:
        approvedIDs = PostApproval.objects.filter(approval=1).values_list('post', flat=True)
        posts = Post.objects.filter(post_id__in = approvedIDs).order_by('-time')
        return render(request, 'adminDelete.html', context={'posts': posts})

    approvedIDs = PostApproval.objects.filter(approval=1).values_list('post', flat=True)

    if category == 'Chemical':
        posts = Post.objects.filter(Q(post_id__in = approvedIDs) & (Q(type__icontains = 'CHEMICAL') & (Q(title__icontains = search_input)|Q(location__icontains = search_input)|Q(description__icontains = search_input))))
    elif category == 'Biological':
        posts = Post.objects.filter(Q(post_id__in = approvedIDs) & (Q(type__icontains = 'BIOLOGICAL') & (Q(title__icontains = search_input)|Q(location__icontains = search_input)|Q(description__icontains = search_input))))
    elif category == 'Physical':
        posts = Post.objects.filter(Q(post_id__in = approvedIDs) & (Q(type__icontains = 'PHYSICAL') & (Q(title__icontains = search_input)|Q(location__icontains = search_input)|Q(description__icontains = search_input))))
    else:
        posts = Post.objects.filter(Q(post_id__in = approvedIDs) & (Q(title__icontains = search_input)|Q(location__icontains = search_input)|Q(description__icontains = search_input)))



    if sort == "oldest":
        posts = posts.order_by('post_id')
    else:
        posts = posts.order_by('-post_id')

    return render(request, 'adminDelete.html', context={'posts': posts, 'input': search_input, 'category': category, 'sort': sort})

#Admin listing for user banning
@user_passes_test(lambda u: Admin.objects.filter(user = u.user_id).exists())
def adminBan(request):
    users = RegisteredUser.objects.all()
    return render(request, 'adminBan.html', context={'users': users})

#Admin approving a hazard
@user_passes_test(lambda u: Admin.objects.filter(user = u.user_id).exists())
def hazardApprove(request, id):
    post = PostApproval.objects.get(post_id=id)
    adminUser = Admin.objects.get(user = request.user)

    if PostApproval.objects.filter(post = id).exists():
        if post.approval == 0:
            post.approval = 1
            post.admin = adminUser
            post.save()
            return redirect('admin')
        else:
            return redirect('admin')
    else:
        return redirect('admin')

#Admin rejecting a hazard
@user_passes_test(lambda u: Admin.objects.filter(user = u.user_id).exists())
def hazardReject(request, id):
    post = PostApproval.objects.get(post_id=id)
    adminUser = Admin.objects.get(user = request.user)

    if PostApproval.objects.filter(post = id).exists():
        if post.approval == 0:
            post.approval = -1
            post.admin = adminUser
            post.save()
            return redirect('admin')
        else:
            return redirect('admin')
    else:
        return redirect('admin')

#Admin deleting a hazard
@user_passes_test(lambda u: Admin.objects.filter(user = u.user_id).exists())
def hazardDelete(request, id):
    post = PostApproval.objects.get(post_id=id)

    if PostApproval.objects.filter(post = id).exists():
        if post.approval == 1:
            post.approval = -1
            post.save()
            return redirect('adminDelete')
        else:
            return redirect('adminDelete')
    else:
        return redirect('adminDelete')

#Admin perma banning a user
@user_passes_test(lambda u: Admin.objects.filter(user = u.user_id).exists())
def userPBan(request, uname):
    user = RegisteredUser.objects.get(username=uname)

    if RegisteredUser.objects.filter(username = uname).exists():
        if user.ban != 'ADMIN':
            user.ban = 'PERMA'
            user.save()
            return redirect('adminBan')
        else:
            return redirect('adminBan')
    else:
        return redirect('adminBan')

#Admin temp banning a user
@user_passes_test(lambda u: Admin.objects.filter(user = u.user_id).exists())
def userTBan(request, uname):
    user = RegisteredUser.objects.get(username=uname)

    if RegisteredUser.objects.filter(username = uname).exists():
        if user.ban != 'ADMIN':
            user.ban = 'TEMP'
            user.save()
            return redirect('adminBan')
        else:
            return redirect('adminBan')
    else:
        return redirect('adminBan')

#Admin unbanning a user
@user_passes_test(lambda u: Admin.objects.filter(user = u.user_id).exists())
def userUnban(request, uname):
    user = RegisteredUser.objects.get(username=uname)

    if RegisteredUser.objects.filter(username = uname).exists():
        if user.ban != 'PERMA' and user.ban != 'ADMIN':
            user.ban = None
            user.save()
            return redirect('adminBan')
        else:
            return redirect('adminBan')
    else:
        return redirect('adminBan')





#Agent Dashboard
#Displays all pending posts for status change
@user_passes_test(lambda u: Agent.objects.filter(user = u.user_id).exists())
def agent(request):
    if request.method == 'POST':
        search_input = request.POST.get('search')
        category = request.POST.get('category')
        sort = request.POST.get('sort')
    else:
        approvedIDs = PostApproval.objects.filter(approval=1).values_list('post', flat=True)
        posts = Post.objects.filter(post_id__in = approvedIDs).order_by('-post_id')
        status = PostStatus.objects.filter(post__in = approvedIDs).order_by('-post_id')
        pns = zip(posts, status)

        return render(request, 'agentResults.html', context={'pns': pns, 'posts': posts})

    approvedIDs = PostApproval.objects.filter(approval=1).values_list('post', flat=True)

    if category == 'Chemical':
        posts = Post.objects.filter(Q(post_id__in = approvedIDs) & (Q(type__icontains = 'CHEMICAL') & (Q(title__icontains = search_input)|Q(location__icontains = search_input)|Q(description__icontains = search_input))))
    elif category == 'Biological':
        posts = Post.objects.filter(Q(post_id__in = approvedIDs) & (Q(type__icontains = 'BIOLOGICAL') & (Q(title__icontains = search_input)|Q(location__icontains = search_input)|Q(description__icontains = search_input))))
    elif category == 'Physical':
        posts = Post.objects.filter(Q(post_id__in = approvedIDs) & (Q(type__icontains = 'PHYSICAL') & (Q(title__icontains = search_input)|Q(location__icontains = search_input)|Q(description__icontains = search_input))))
    else:
        posts = Post.objects.filter(Q(post_id__in = approvedIDs) & (Q(title__icontains = search_input)|Q(location__icontains = search_input)|Q(description__icontains = search_input)))

    status = PostStatus.objects.filter(post__in = posts).order_by('-post_id')

    if sort == "oldest":
        posts = posts.order_by('post_id')
        status = status.order_by('post_id')

    else:
        posts = posts.order_by('-post_id')
        status = status.order_by('-post_id')

    pns = zip(posts, status)

    return render(request, 'agentResults.html', context={'pns': pns, 'posts': posts, 'input': search_input, 'category': category, 'sort': sort})


#Agent changing status to in progress
@user_passes_test(lambda u: Agent.objects.filter(user = u.user_id).exists())
def hazardInProgress(request, id):
    post = PostStatus.objects.get(post_id=id)
    agentUser = Agent.objects.get(user = request.user)

    if PostStatus.objects.filter(post = id).exists():
        post.status = 'IN PROGRESS'
        post.agent = agentUser
        post.save()
        return redirect('agent')
    else:
        return redirect('agent')

#Admin changing status to finished
@user_passes_test(lambda u: Agent.objects.filter(user = u.user_id).exists())
def hazardFinished(request, id):
    post = PostStatus.objects.get(post_id=id)
    agentUser = Agent.objects.get(user = request.user)

    if PostStatus.objects.filter(post = id).exists():
        post.status = 'FINISHED'
        post.agent= agentUser
        post.save()
        return redirect('agent')
    else:
        return redirect('agent')
