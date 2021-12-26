from django.shortcuts import render, redirect
from payment.models import Member
from django.http import JsonResponse


def id_overlap_check(request):
    id = request.GET.get('id')
    user = Member.objects.filter(m_id=id)
    if str(user) == "<QuerySet []>":
        overlap = "pass"
    else:
        overlap = "fail"

    context = {'overlap': overlap}
    return JsonResponse(context)


def login(request):
    try:
        if request.session['login'] and request.session['user_id']:
            return redirect('order:index')
    except KeyError:
        pass

    return render(request, 'user/login.html')


def login_check(request):
    user_id = request.POST.get('user_id')
    user_pwd = request.POST.get('pwd')
    # 아이디 틀렸을 때 오류처리 필요
    try:
        data = Member.objects.get(m_id=user_id)
    except Member.DoesNotExist:
        url = 'user/login_fail.html'
    else:
        if data.m_password == user_pwd:
            request.session['user_id'] = user_id
            request.session['login'] = True
            return redirect('order:index')
        else:
            url = 'user/login_fail.html'

    return render(request, url)


def register(request):
    url = 'user/register.html'
    return render(request, url)


def register_check(request):
    user_id = request.POST.get('id')
    user_pwd = request.POST.get('pwd1')
    user_name = request.POST.get('name')
    user_domain = request.POST.get('domain')
    user_phone1 = request.POST.get('phone1')
    user_phone2 = request.POST.get('phone2')
    user_phone3 = request.POST.get('phone3')
    user_number = user_phone1 + user_phone2 + user_phone3
    user_email1 = request.POST.get('email1')
    user_email2 = request.POST.get('email2')
    user_mail = user_domain + '@' + user_email2
    if user_email2 == "blank":
        user_mail = user_domain + '@' + user_email1
    member = Member.objects.create(m_name=user_name, m_id=user_id, m_password=user_pwd, m_number=user_number, mail=user_mail)
    member.save()
    url = 'user/register_success.html'
    return render(request, url)


def findID(request):
    url = 'user/findID.html'
    return render(request, url)


# #입력받은 전화번호가 table 정보와 일치하는지 확인이 안됨
def findID_check(request):
    user_name = request.POST.get('name')
    number1 = request.POST.get('phone1')
    number2 = request.POST.get('phone2')
    number3 = request.POST.get('phone3')
    user_number = number1 + number2 + number3
    try:
        data = Member.objects.get(m_name=user_name, m_number=user_number)
    except Member.DoesNotExist:
        url = 'user/findID.html'
        message = {'message': '이름 또는 전화번호가 틀립니다.'}
    else:
        url = 'user/findID_success.html'
        m_id = data.m_id
        message = {'message': f'아이디는 {m_id} 입니다.'}

    return render(request, url, message)


def findPW(request):
    url = 'user/findPW.html'
    return render(request, url)


def findPW_check(request):
    user_name = request.POST.get('name')
    user_id = request.POST.get('id')
    user_phone1 = request.POST.get('phone1')
    user_phone2 = request.POST.get('phone2')
    user_phone3 = request.POST.get('phone3')
    user_number = user_phone1 + user_phone2 + user_phone3

    try:
        data = Member.objects.get(m_id=user_id, m_name=user_name, m_number=user_number)
    except Member.DoesNotExist:
        url = 'user/findPW.html'
        message = {'message': '이름, ID, 전화번호를 다시 확인해주세요!'}
    else:
        user_pw = data.m_password
        url = 'user/findPW_success.html'
        message = {'message': f'{user_name}님의 비밀번호는 {user_pw}입니다'}

    return render(request, url, message)


def return_login(request):
    url = 'user/login.html'
    return render(request, url)


def logout(request):
    try:
        if request.session['login']:
            request.session['login'] = False
            del request.session['user_id']
            request.session.modified = True
    except KeyError:
        print('로그인 정보가 없습니다.')
        pass

    return redirect('main:main')
