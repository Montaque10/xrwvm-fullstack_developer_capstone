# Uncomment the imports before you add the code
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
# from . import views

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration
    path(route='login', view=views.login_user, name='login'),
    path(route='logout', view=views.logout_user, name='logout'),
    path(route='register', view=views.registration, name='register'),

    # path for dealer reviews view
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get_dealer_reviews/<int:dealer_id>', view=views.get_dealer_reviews, name='get_dealer_reviews'),
    path(route='get_dealer_details/<int:dealer_id>', view=views.get_dealer_details, name='get_dealer_details'),

    # path for add a review view
    path(route='add_review', view=views.add_review, name='add_review'),
    path(route='analyze_review_sentiments', view=views.analyze_review_sentiments, name='analyze_review_sentiments'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
