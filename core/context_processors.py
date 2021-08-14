from siteconfig.models import *
from core.models import *

def postfooter(request):
    footerposts=Post.objects.filter(featured=True).order_by('-created_on')[:3]
    return {'fposts':footerposts}

def gallery(request):
    galimgs=Gallery.objects.order_by('-timestamp')[:4]
    return {'galimgs':galimgs}

def contacts(request):
    c=Contacts.objects.order_by("dateadded")[:6]
    return {'contacts':c}

def customname(request):
    customname=Customblogname.objects.all()
    return {'custom':customname}

def about_org(request):
    desk_details=About.objects.all()
    return {'desk_details':desk_details}

def update_logo(request):
    logo=UpdateLogo.objects.all()
    return {'logo':logo}

def post_categories(request):
    categories=Category.objects.all()
    return {'categories':categories}