from ..models import UserModel
from django.views.generic import DetailView

class UserView(DetailView):
    model = UserModel
    template_name = 'user.html'