from django.shortcuts import render, redirect
from payment.models import Member, Company, CompanyAdmin, Product, Pay, PayItem
from django.db.models import Sum, Count
import json
from datetime import datetime
from django.db.models.functions import Substr


def sales_data_chart(sql, data_type):
    pay_list = Pay.objects.raw(sql)
    series_opt = []
    company_list = Company.objects.all()
    total = 0
    for company in company_list:
        value_dict = {}
        value_dict['name'] = str(company.c_name) + " " + data_type
        data_list = [0] * 13
        for p in pay_list:
            if str(p.c_code) == str(company.c_code):
                index = int(p.check_hour) - 9
                data_list[index] += int(p.sum_per_day)
                total += int(p.sum_per_day)
        value_dict['data'] = data_list
        series_opt.append(value_dict)
    return series_opt, total


def sales_data(request):
    current_date = datetime.today().strftime('%Y-%m-%d')
    current_year = current_date[:4]
    current_month = current_date[5:7]
    pay_total = Pay.objects.filter(date__year=current_year, date__month=current_month).aggregate(Sum('total'))
    pay_total = int(pay_total['total__sum'])
    pay_count = Pay.objects.filter(date__year=current_year, date__month=current_month).aggregate(Count('total'))
    pay_count = int(pay_count['total__count'])
    day_count = Pay.objects.filter(date__year=current_year, date__month=current_month).values(date_a=Substr('date', 1, 10)).annotate(Count('total'))
    month_avg = round((pay_total / len(day_count)), 1)
    month_count_avg = round((pay_count / len(day_count)), 1)

    categories = [str(i) + '시' for i in range(9, 22)]
    series = {}
    sql1 = '''select id, date(p.date) as check_date, hour(p.date) as check_hour, sum(total) as sum_per_day, c_code
                                    from payment_pay as p
                                    where date(p.date) = CURDATE()
                                    group by c_code, check_date, check_hour
                                    order by c_code, check_date, check_hour'''
    data1, total_price = sales_data_chart(sql1, '매출액')
    sql2 = '''select id, date(p.date) as check_date, hour(p.date) as check_hour, count(total) as sum_per_day, c_code
                from payment_pay as p
                where date(p.date) = CURDATE()
                group by c_code, check_date, check_hour
                order by c_code, check_date, check_hour'''
    data2, total_count = sales_data_chart(sql2, '주문 건수')

    series['column'] = data1
    series['line'] = data2

    final_data = {'categories': categories, 'series': series}
    final_json_data = json.dumps(final_data, indent=4)

    context = {
        'data': final_json_data,
        'total_price': total_price,
        'total_count': total_count,
        'month_avg': month_avg,
        'month_count_avg': month_count_avg,
        'current_date': current_date,
    }

    return render(request, 'companyAdmin/test.html', context=context)


def new(request):
    try:
        if request.session['admin_login']:
            return redirect('companyAdmin:visual')
    except KeyError:
        pass

    return render(request, 'companyAdmin/new.html')


def logout(request):
    del request.session['admin_login']
    return redirect('main:main')


def visual(request):
    try:
        if request.session['admin_login']:
            url = 'companyAdmin/maps.html'
            message = {'message': ''}
    except KeyError:
        id = request.POST.get('userid')
        pwd = request.POST.get('pwd')
        # data의 값이 admin인지 아닌지를 판별하는 판별식을 코드로 표현
        comp = CompanyAdmin.objects.values_list()
        url = 'companyAdmin/new.html'

        if id != comp[0][1]:
            message = {'message': '아이디가 잘못되었습니다'}
        elif pwd != comp[0][2]:
            message = {'message': '비밀번호가 잘못되었습니다'}
        else:
            url = 'companyAdmin/maps.html'
            message = {'message': ''}
            request.session['admin_login'] = True

    return render(request, url, message)


def maps(request):
    return render(request, 'companyAdmin/maps.html')


# def sales_data(request):
#     return render(request, 'companyAdmin/sales_data.html')


def append(request):
    message = {'message': ''}
    return render(request, 'companyAdmin/append.html', message)


def delete(request):
    return render(request, 'companyAdmin/delete.html')


def month(request):
    if request.method == "POST":
        s_date = request.POST['start_month']
        e_date = request.POST['end_month']
        date_info = s_date + '  -  ' + e_date
        print(s_date, e_date)
        s_year = s_date[:4]
        s_month = s_date[-2:]
        e_year = e_date[:4]
        e_month = e_date[-2:]
        print(s_year, s_month, e_year, e_month)
        categories = []
        while True:
            categories.append(s_date)
            if s_date == e_date:
                break

            if s_month == '12':
                s_year = str(int(s_year) + 1)
                s_month = '01'
                s_date = s_year + '-' + s_month
                print(s_date)
            else:
                s_month = str(int(s_month) + 1).zfill(2)
                s_date = s_year + '-' + s_month
                print(s_date)

        print(categories)

        companies = Company.objects.all()
        series = []
        for company in companies:
            c_code = company.c_code
            value_dict = {'name': str(company.c_name)}
            data_list = []
            for date in categories:
                search_year = date[:4]
                search_month = date[-2:]
                try:
                    total_price = Pay.objects.filter(c_code=c_code, date__year=search_year, date__month=search_month).aggregate(Sum('total'))
                    data_list.append(total_price['total__sum'])
                except Pay.DoesNotExist:
                    data_list.append(0)
            value_dict['data'] = data_list
            series.append(value_dict)

        final_data = {'categories': categories, 'series': series}
        final_json_data = json.dumps(final_data, indent=4)
        print(final_json_data)

        return render(request, 'companyAdmin/month.html', context={'data': final_json_data, 'date_info': date_info})

    return render(request, 'companyAdmin/month.html')


def location(request):
    loc_list = Company.objects.all()
    context = {
        'loc_list': loc_list
    }
    return render(request, 'companyAdmin/location.html', context=context)


def location_detail(request):
    if request.method == "POST":
        loc_list = Company.objects.all()
        c_code = request.POST['location']
        c_name = Company.objects.get(c_code=c_code).c_name
        month_date = request.POST['monthDate']
        print(c_code, month_date)
        search_month = month_date[-2:]
        print(search_month)
        search_year = month_date[:4]
        print(search_year)

        sales_by_branch = Pay.objects.filter(c_code=c_code, date__year=search_year, date__month=search_month)
        total_price = sales_by_branch.aggregate(Sum('total'))
        total_by_branch = total_price['total__sum']
        context = {
            'sales': sales_by_branch,
            'loc_list': loc_list,
            'name': c_name,
            'total': total_by_branch,
            'date': month_date,
        }

        return render(request, 'companyAdmin/location.html', context=context)


def append_complete(request):
    url = 'companyAdmin/append_complete.html'
    p_code = request.POST.get('p_code')
    p_name = request.POST.get('p_name')
    price = request.POST.get('price')
    # image_path = request.POST.get('image_path')
    image_path = request.FILES['image_path']
    p_desc = request.POST.get('p_desc')
    try:
        product = Product(p_code=p_code, p_name=p_name, price=price, user_image_path=image_path, p_desc=p_desc)
        product.save()
        message = {'message': '추가 완료.'}
    except:
        url = 'companyAdmin/append.html'
        message = {'message': '데이터 형식이 잘못되었습니다(상품코드는 4자리 입니다)'}

    return render(request, url, message)


def delete_complete(request):
    url = 'companyAdmin/delete_complete.html'
    p = request.POST.get('p_code')
    try:
        product = Product.objects.get(p_code=p)
        product.delete()
    except Product.DoesNotExist:
        url = 'companyAdmin/delete.html'

    message = {'message': '존재하지 않는 상품 코드입니다'}

    return render(request, url, message)


def plist(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'companyAdmin/plist.html', context)
