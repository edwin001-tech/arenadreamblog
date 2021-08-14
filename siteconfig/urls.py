from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('policies/', login_required(SitePoliciesView.as_view()), name='site_policies_view'),
    path('contacts/', login_required(contact), name='contacts'),
    path('our/partners/', login_required(OurPartnersView.as_view()), name='our_partners_view'),
    path('How/it/works/', login_required(HowItWorksView.as_view()), name='how_it_works_view'),
    path('FAQ/', login_required(FAQView.as_view()), name='faq_view'),
]