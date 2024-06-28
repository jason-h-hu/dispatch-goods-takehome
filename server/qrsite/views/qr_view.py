import qrcode
import io
from django.http import HttpResponse, Http404
from ..models import UserModel
from string import Template

def get_user_or_throw(id):
    try:
        user = UserModel.objects.get(id=id)
        return user
    except UserModel.DoesNotExist:
        raise Http404('User does not exist')

def get_qr(request, id):
    host = request.META['HTTP_HOST']
    get_user_or_throw(id)
    qr = qrcode.QRCode()
    qr.add_data(Template('$host/users/$id').substitute(
        host=host,
        id=id
    ))
    img = qr.make_image()
    byte_io = io.BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    return HttpResponse(byte_io, content_type='image/png')