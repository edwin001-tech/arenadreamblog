from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from .models import *

# Create your views here.
def contact(request):
    context={
        'tag_line':'Contacts Page'
    }
    return render(request,'siteconfig/contact.html',context)

class SitePoliciesView(LoginRequiredMixin,View):
    template_name = 'siteconfig/site_policies.html'
    def get(self, request, *args, **kwargs):
        policies=Site_Policies.objects.all()
        context = {
              'policies':policies,
               'tag_line':'Our Policies',
        }
        return render(request, self.template_name, context=context)

class OurPartnersView(LoginRequiredMixin,View):
    template_name = 'siteconfig/site_policies.html'
    def get(self, request, *args, **kwargs):
        third_parties=ThirdParty.objects.all()
        context = {
              'third_parties':third_parties,
              'tag_line':'Our Partners',
        }
        return render(request, self.template_name, context=context)

class FAQView(LoginRequiredMixin,View):
    template_name = 'siteconfig/FAQ.html'
    def get(self, request, *args, **kwargs):
        faqs=FQA.objects.all()
        context = {
              'faqs':faqs,
               'tag_line':'FAQ - Frequently Asked Questions & Their Answers',
        }
        return render(request, self.template_name, context=context)

class HowItWorksView(LoginRequiredMixin,View):
    template_name = 'siteconfig/How_it_works.html'
    def get(self, request, *args, **kwargs):
        howitworks=Howitworks.objects.all()
        context = {
              'howitworks':howitworks,
               'tag_line':'How It Works',
        }
        return render(request, self.template_name, context=context)