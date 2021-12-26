from django.shortcuts import render
from payment.models import Member
# Create your views here.


def main(request):
    try:
        request.session['login']
        user_id = request.session['user_id']
        member_info = Member.objects.get(m_id=user_id).m_name
        context = {
            'name': member_info
        }
    except KeyError:
        context = {'name': None}

    return render(request, 'main/main.html', context)
