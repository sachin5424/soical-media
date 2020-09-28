from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models
from django.shortcuts import reverse
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver



class Profile(models.Model):
    profile_pic = models.ImageField(upload_to='media/profile_pic/',blank=True,null=True,default='nopic/slide3.jpg')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200,blank=True,null=True)
    phone_no = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=15, null=True, blank=True)
    def __str__(self):
        return self.user.username

    def get_profle_url(self):
        return reverse('facebook:profile_detail',kwargs={'pk': self.id})

    def get_add_frind_url(self):
        return reverse('facebook:frnd_add', kwargs={'pk': self.id})

    def get_add_frind_confirm_url(self):
        return reverse('facebook:frnds_confirm',  kwargs={'user': self.user})

    def get_add_frind_unfrnds_url(self):
        return reverse('facebook:frnds_unfrnds',  kwargs={'pk': self.id})
    # def get_add_frind_del_url(self):
    #     return reverse('facebook:frnds_del',  kwargs={'pk': self.id})

    def get_request_Profile_url(self):
        return reverse('facebook:profile_detail_user', kwargs={'user': self.user})





class User_Post(models.Model):
    pic = models.ImageField(upload_to='post/')
    subject = models.CharField(max_length=200)
    msg = models.TextField(null=True, blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(Profile,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "%s" % self.subject


class AddFriend(models.Model):
    add =models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='add')
    add_by =models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='add_by')
    send_rqst = models.BooleanField(default=False)
    confirmn= models.BooleanField(default=False)
    def __str__(self):
        return '%s (%s)'%(self.add ,self.add_by)

class User_Post_commt(models.Model):
    post =models.ForeignKey(User_Post,on_delete=models.CASCADE,related_name='post')
    commt =models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='commt')
    you_msg= models.CharField(null=True,blank=True,max_length=250)
    def __str__(self):
        return '%s (%s)'%(self.post ,self.commt)

   
    




@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)