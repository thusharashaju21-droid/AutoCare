from django.urls import path
from service.views import SignUpView
from service.views import GetMeView
from service.views import ServiceRequestListCreateView
from service.views import ServiceRequestDetailView
from service.views import ServiceRequestFilterView
from service.views import ServiceRequestSearchView
from service.views import PendingServiceRequestView
from service.views import ServiceRequestCountView
from service.views import ServiceRequestPriorityView

from rest_framework.authtoken.views import obtain_auth_token
     
urlpatterns = [

    # Registration and User
    path("register/", SignUpView.as_view()),
    path("me/", GetMeView.as_view()),

    #generate token
    path("token/",obtain_auth_token),

    # Create and List
    path("service-requests/", ServiceRequestListCreateView.as_view()),

    # Retrieve, Update and Delete
    path("service-requests/<int:pk>/", ServiceRequestDetailView.as_view()),

    # Filtering
    path("service-requests/filter/", ServiceRequestFilterView.as_view()),

    # Searching
    path("service-requests/search/", ServiceRequestSearchView.as_view()),

    # Pending Requests
    path("service-requests/pending/", PendingServiceRequestView.as_view()),

    # Count and Reports
    path("service-requests/count/", ServiceRequestCountView.as_view()),

    # High and Critical
    path("service-requests/high-critical/", ServiceRequestPriorityView.as_view()),

]
