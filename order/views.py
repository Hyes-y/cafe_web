from django.shortcuts import render, redirect, get_object_or_404
from payment.models import Member, Cart, CartItem, Product, Company


def index(request):
    return render(request, 'order/shopsel.html')


def shopsel(request, c_code):
    user_id = request.session['user_id']
    user = Member.objects.get(m_id=user_id)
    company = Company.objects.get(c_code=c_code)
    try:
        cart_info = Cart.objects.get(m_id=user_id)
        print(cart_info.check)
        if cart_info.check:
            cart_info.delete()
            raise ValueError
    except (Cart.DoesNotExist, ValueError):
        new_cart = Cart.objects.create(c_code=company, m_id=user)
        new_cart.save()
        return redirect('order:product')
    else:
        company_name = cart_info.c_code.c_name
        company_code = str(cart_info.c_code)
        if company_code != c_code:
            context = {
                'message': f'다른 지점({company_name})의 상품이 이미 장바구니에 등록되어 있습니다.'
            }
            return render(request, 'order/shopsel.html', context=context)

    return redirect('order:product')


def product(request):
    user_id = request.session['user_id']

    if Cart.objects.get(m_id=user_id):
        product_item = Product.objects.filter(p_code__startswith='2')
        context = {
            'product': product_item
        }
        return render(request, 'order/product_test.html', context=context)
    else:
        return redirect('order:login')
    # return render(request, 'order/product.html')


def option(request, p_code):
    prod = Product.objects.get(p_code=p_code)
    context = {
        'product': prod
    }
    return render(request, 'order/option.html', context=context)


def cart_save(request, p_code):
    cart_info = Cart.objects.get(m_id=request.session['user_id'])
    cart_id = cart_info.id
    p_code = Product.objects.get(p_code=p_code)
    size = request.POST.get('size')
    opt = int(request.POST.get('ice_hot'))
    cnt = (request.POST.get('cnt'))
    opt2 = request.POST.get('here_togo')
    print(size, opt, cnt, type(cnt), opt2)
    try:
        item_in_cart = CartItem.objects.get(cart_id=cart_id, p_code=p_code, opt=opt)
    except CartItem.DoesNotExist:
        item = CartItem.objects.create(cnt=cnt, opt=opt, p_code=p_code, cart_id=cart_id)
        item.save()
    else:
        item_in_cart.cnt = int(item_in_cart.cnt) + int(cnt)
        item_in_cart.save()

    return redirect('order:cart')


def cart(request):
    try:
        cart_info = Cart.objects.get(m_id=request.session['user_id'])
    except Cart.DoesNotExist:
        context = {
            'message': '장바구니 내역이 존재하지 않습니다.'
        }
    else:
        cart_id = cart_info.id
        products = CartItem.objects.filter(cart_id=cart_id)
        context = {
            "cart": cart_info,
            "products": products
        }

    return render(request, 'order/cart.html', context=context)


def cart_remove(request, product_id):
    value = request.POST.get('cart-remove')
    print(value)
    item = CartItem.objects.get(id=product_id)
    if value == 'cart_all':
        item.delete()
    else:
        if item.cnt > 1:
            item.cnt -= 1
            item.save()
        else:
            item.delete()
    return redirect('order:cart')


def remove(request):
    cart_info = Cart.objects.get(m_id=request.session['user_id'])
    cart_id = cart_info.id
    cart_items = CartItem.objects.filter(cart_id=cart_id)
    cart_items.delete()
    cart_info.delete()
    return redirect('order:index')
