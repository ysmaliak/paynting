from django.urls import path
from paynting import views
from .views import HomePageView, MasterpieceCreateView, MasterpieceDeleteView, MasterpieceUpdateView, SearchView, \
    account_view, signup_view, sort_view, activation_sent_view, activate

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('masterpiece/create/', MasterpieceCreateView.as_view(), name='masterpiece_create'),
    path('masterpiece/<int:pk>/update/', MasterpieceUpdateView.as_view(), name='masterpiece_update'),
    path('masterpiece/<int:pk>/delete/', MasterpieceDeleteView.as_view(), name='masterpiece_delete'),
    path('account/<str:username>', account_view, name='account_view'),
    path('masterpiece/<int:primary_key>', views.masterpiece_detail_view, name='masterpiece_detail'),
    path('signup/', signup_view, name='signup'),
    path('search/', SearchView.as_view(), name='search'),
    path('sort/', sort_view, name='sort'),
    path('sent/', activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
]
