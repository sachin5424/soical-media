from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile,User_Post,AddFriend,User_Post_commt
from .forms import User_Postform,AddFriend_form,User_Post_commtform
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# Create your views here.
@login_required
def index(request):
    # profile_D = Profile.objects.all()
    k =request.user


    your_post = User_Post.objects.filter(uploaded_by__user=k)
  
    profile =None
    jquery = request.GET.get('jquery')
    if jquery:
        profile = Profile.objects.filter(user__username__icontains=jquery)
    else:
        profile = User_Post.objects.filter(uploaded_by__user=k).order_by('-id')
    username = request.user
    user_profile = Profile.objects.get(user=request.user)

    # print(user_profile)
    post = User_Postform()
    if request.method == 'POST':
        post = User_Postform(request.POST,request.FILES)
        if post.is_valid():
            form = post.save()
            form.uploaded_by = user_profile

            form.save()
            return redirect('facebook:home')
 

    parm={
        'profile':profile,
        'post':post
    }
    return render(request, 'insta/index.html',parm)


# class profile_detail(DetailView):
#     model = Profile
@login_required
def profile_detail(request,pk):
    profile_D = get_object_or_404(Profile,id=pk)
    userId = profile_D.user   
    user=request.user.username
    post_D = User_Post.objects.filter(uploaded_by__user=userId)
    add_frnds =AddFriend_form()
    check_frnds = AddFriend.objects.filter(add_by__user__username=userId,send_rqst=True,confirmn=False)
    
    if request.method == 'POST':
       post = request.POST.get('post')
       you_msg = request.POST.get('you_msg')
       user_profile = Profile.objects.get(user=request.user)
       commment_post = User_Post.objects.get(id=post)
       commment = User_Post_commt(commt=user_profile,post=commment_post,you_msg=you_msg)
       commment.save()
     
    parm= {
        'profile_D':profile_D,
        'post':post_D,
        'add_frnds':add_frnds,
        'check_frnds':check_frnds,
        # 'commment_count':commment_count,
        # 'commment':commment
           }
    return render(request,'insta/profile_detail.html',parm)

@login_required
def frnd_add(request,pk):
    k =  get_object_or_404(Profile,id=pk)
    p= k.user.username
 
    username = request.user
    profile = Profile.objects.get(user=username)
    profile_buy = Profile.objects.get(user__username=p)
    frnd_request,created = AddFriend.objects.get_or_create(add=profile,add_by=profile_buy,confirmn=False,send_rqst=True)
    frnd_request.save()
    return redirect('facebook:profile_detail',pk=pk)

@login_required
def profile_detail_user(request,user):
    user = request.user.username

    user_detail_id = get_object_or_404(Profile,user__username=user)
  
    profile_post = User_Post.objects.filter(uploaded_by=user_detail_id)
    frndRequest = AddFriend.objects.filter(add_by__user__username=user,confirmn=False)
    you_frnds = AddFriend.objects.filter(add_by__user__username=user,confirmn=True)
    
  

    parm ={
       'user_profile_detail':user_detail_id,
       'profile_post':profile_post,
       'frndRequest':frndRequest ,
       'you_frnds':you_frnds,
     
    }
    return render(request,'insta/profile_detail_user.html',parm)
@login_required
def frnds_confirm(request,user):
    user = request.user.username

    user_detail_id = get_object_or_404(Profile,user__username=user)
    conf = AddFriend.objects.filter(add_by__user__username=user).update(confirmn=True)
    return redirect('facebook:profile_detail_user',user=user)
@login_required
def frnds_unfrnds(request,pk):
    k =  get_object_or_404(Profile,id=pk)
    p= k.user.username
    username = request.user
    profile = Profile.objects.get(user=username)
    profile_buy = Profile.objects.get(user__username=p)
    frnd_request = AddFriend.objects.get(add=profile,add_by=profile_buy,confirmn=False,send_rqst=True).delete()
    return redirect('facebook:profile_detail',pk=pk)



class Post_commt(View):
    """docstring for ClassName"""
    def get(self, *args, **kwargs):
        
        # print(profile_D)
        profile_D=kwargs['pk']
        print('id',profile_D)
        a = User_Post.objects.get(id=profile_D)

        print(a)
        commt= User_Post_commt.objects.filter(post_id=profile_D)
        print('commt',commt)

       
   
        parm={
        'profile_D':a,
        'commt':commt,
        }
        
        return render(self.request, 'insta/post_User_Post_commt.html',parm)
    def post(self,request,*args, **kwargs):
        pk=kwargs['pk']
        if request.method == 'POST':
           post = request.POST.get('post')
           you_msg = request.POST.get('you_msg')
           user_profile = Profile.objects.get(user=request.user)
           commment_post = User_Post.objects.get(id=post)
           commment = User_Post_commt(commt=user_profile,post=commment_post,you_msg=you_msg)
           commment.save()
        return HttpResponseRedirect(request.path_info)







@login_required
def user_login(request):
    if request.user.is_authenticated:
        return redirect('facebook:home')
    else:
        form = AuthenticationForm()
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user =authenticate(username=username,password=password)
            if user is None:
               return redirect('facebook:user_login')
            else:
                login(request,user)
                return redirect('facebook:home')
        else:
            return render(request,'insta/user_login.html',{'form':form})

def register_user(request):
    if request.user.is_authenticated:
        return redirect('facebook:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('Username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            user = User.objects.create_user(username=username,password=password1,email=email)
            user.save()
            return redirect('facebook:user_login')
        else:
            return render(request,'insta/register_user.html')


