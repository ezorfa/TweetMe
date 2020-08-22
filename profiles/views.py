from django.http import Http404
from django.shortcuts import render, redirect  

from .models import Profile
from .forms import ProfileForm

# Create your views here.


def profile_update_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("/login?next=/profile/update")
    user = request.user
    my_profile = user.profile
    initial = {
        "first_name" : user.first_name,
        "last_name" : user.last_name,
        "email_address" : user.email_address,

    }
    form = ProfileForm(request.POST or None, instance=my_profile, initial=initial)
    if form.is_valid():
        profile_obj = form.save(commit=False)
        first_name = form.cleaned_data.get('first_name')
        last_name = form.cleaned_data.get('last_name')
        email_address = form.cleaned_data.get('email_address')
        user.first_name = first_name
        user.last_name = last_name
        user.email_address = email_address
        user.save()
        profile_obj.save()
    context = {
        "form" : form,
        "btn_label" : "Save",
        "title" : "Update profile",
            }
    return render(request, "profiles/form.html", context)

def profile_detail_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username = username)
    if not qs.exists():
        raise Http404
    profile_obj = qs.first
    context = {
        "username" : username,
        "profile" : profile_obj
    }
    return render(request, "profiles/detail.html", context)