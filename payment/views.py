from django.shortcuts import render, redirect
from decouple import config
from .models import Cart, CartItem, Pay, PayItem
from datetime import datetime
import requests


def order_list(member_id):
    """ 장바구니 내 항목들의 총 가격, 결제시 표기할 항목명, 수량 등의 정보를 처리하여 사전형으로 반환하는 함수"""
    total_cnt = 0
    total_price = 0
    product_list = []
    cart = Cart.objects.get(m_id=member_id)
    cart_id = cart.id
    items = CartItem.objects.filter(cart_id=cart_id)
    for item in items:
        total_cnt += item.cnt
        prod = item.p_code
        total_price += prod.price * item.cnt
        if not product_list:
            product_list.append(prod.p_name)

    if total_cnt == 1:
        product_display_name = product_list[0]
    else:
        product_display_name = product_list[0] + f' 외 {total_cnt - 1}건'

    context = {
        'cart_id': cart_id,
        'total_cnt': total_cnt,
        'total_price': total_price,
        'product_display_name': product_display_name
    }
    return context


def index(request):
    """ 주문 내역 최종 확인 함수 """
    member_id = request.session['user_id']
    cart = Cart.objects.get(m_id=member_id)
    cart_id = cart.id
    items = CartItem.objects.filter(cart_id=cart_id)
    total_amount = 0
    for item in items:
        total_amount += int(item.p_code.price) * int(item.cnt)
    content = {
        'cart': cart,
        'items': items,
        'total': total_amount
    }
    return render(request, 'payment/paymentCheck.html', content)


def pay(request):
    """ 결제 요청 함수 : kakaopay API로 결제 정보를 넘겨 결제를 요청하는 함수 """
    current_time = int(datetime.today().strftime('%H'))
    if current_time < 9 or current_time > 21:
        return redirect('main:main')

    m_id = request.session['user_id']
    context = order_list(m_id)
    cart_id = context['cart_id']
    if request.method == "POST":
        URL = "https://kapi.kakao.com/v1/payment/ready"
        headers = {
            "Authorization": "KakaoAK " + f"{config('api_key')}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }
        data = {
            "cid": "TC0ONETIME",
            "partner_order_id": cart_id,
            "partner_user_id": m_id,
            "item_name": context['product_display_name'],
            "quantity": "1",
            "total_amount": context['total_price'],
            "tax_free_amount": "0",
            "approval_url": f'http://localhost:8000/payment/{cart_id}/approval',
            "cancel_url": f'http://localhost:8000/payment/cancel',
            "fail_url": f'http://localhost:8000/payment/fail',
        }

        res = requests.post(URL, headers=headers, data=data)
        tid = res.json()['tid']
        print(tid)
        post = Cart.objects.get(id=cart_id)
        post.tid = tid
        post.save()
        next_url = res.json()['next_redirect_pc_url']
        return redirect(next_url)

    return render(request, 'payment/paymentCheck.html')


def approval(request, cart_id):
    """ 결제 승인 함수 : 결제 정보를 다시 넘겨주고 일치하는지 확인 후 승인 """
    info = Cart.objects.get(id=cart_id)
    tid = info.tid
    URL = 'https://kapi.kakao.com/v1/payment/approve'
    headers = {
        "Authorization": "KakaoAK " + f"{config('api_key')}",
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
    }

    data = {
        "cid": "TC0ONETIME",
        # "tid": request.session['tid'],
        "tid": tid,
        "partner_order_id": info.id,
        "partner_user_id": info.m_id,
        "pg_token": request.GET.get("pg_token"),
    }

    # 승인 완료시 응답을 받아오는 변수 res(ponse)
    res = requests.post(URL, headers=headers, data=data)
    amount = res.json()['amount']['total']
    res = res.json()
    approved_date = res['approved_at'][:10]
    approved_time = res['approved_at'][11:]
    approved_at = approved_date + ' ' + approved_time
    print(approved_at)
    pay_record = Pay.objects.create(c_code=info.c_code, m_id=info.m_id, date=approved_at, total=amount)
    pay_record.save()

    context = {
        'res': res,
        'amount': amount,
        'pay_info': pay_record,
    }
    # 결체 승인되었으므로 check=True로 변경
    info.check = True
    info.save()
    pay_info = Pay.objects.filter(m_id=info.m_id).order_by('date').last()
    print(pay_info.id)
    cart_id = info.id
    # 결제 완료(check=True)인 경우 장바구니 내역을 결제 내역으로 옮김
    if info.check:
        cart_items = CartItem.objects.filter(cart_id=cart_id)
        for item in cart_items:
            pay_item = PayItem.objects.create(cnt=item.cnt, opt=item.opt, p_code=item.p_code, pay_id=pay_info.id)
            pay_item.save()
        # 장바구니 삭제
        cart_items.delete()
        info.delete()

    # kakaopay 이용하면서 session이 이상해지므로 로그인 상태 다시 구현
    user_id_str = str(info.m_id)
    request.session['user_id'] = user_id_str
    request.session['login'] = True
    return render(request, 'payment/paymentApproval.html', context=context)


def complete(request):
    """ 완료 후 메인 페이지로 이동 """
    return redirect('main:main')


def fail(request):
    """ 결제 실패시 이동할 페이지 """
    return render(request, 'payment/paymentFail.html')


def cancel(request):
    """ 결제 취소시 이동할 페이지 """
    return render(request, 'payment/paymentCancel.html')


def pay_history(request):
    """ 사용자의 결제 내역을 선택한 날짜별로 보여주는 함수 """
    if request.method == 'POST':
        prev_date = request.POST['fromDate']
        curr_date = request.POST['toDate']
        period = prev_date + ' - ' + curr_date
        prev_date = prev_date + ' 00:00:00'
        curr_date = curr_date + ' 23:59:59'
        user_id = request.session['user_id']
        pay_infos = Pay.objects.filter(m_id=user_id, date__range=[prev_date, curr_date])
        context = {
            'pay_infos': pay_infos,
            'period': period
        }
        return render(request, 'payment/pay_history.html', context=context)
    else:
        return render(request, 'payment/pay_history.html')
