from django.db import models

# Create your models here.


class Member(models.Model):
    m_name = models.CharField(max_length=20)    # 회원 이름
    m_id = models.CharField(max_length=11, primary_key=True)    # 회원 id
    m_password = models.CharField(max_length=11)    # 회원 비밀번호
    m_number = models.CharField(max_length=11)  # 회원 전화번호
    mail = models.EmailField(max_length=128)    # 회원 이메일주소

    def __str__(self):
        return self.m_id


class Company(models.Model):
    c_name = models.CharField(max_length=20)    # 점포명
    c_code = models.CharField(max_length=4, primary_key=True)   # 점포코드
    lat = models.CharField(max_length=100, null=True)    # 점포 위치(위도)
    lng = models.CharField(max_length=100, null=True)  # 점포 위치(경도)

    def __str__(self):
        return self.c_code


class CompanyAdmin(models.Model):
    ca_id = models.CharField(max_length=11)     # 관리자 id
    ca_password = models.CharField(max_length=11)       # 관리자 비밀번호

    def __str__(self):
        return self.ca_id


class Product(models.Model):
    p_code = models.CharField(max_length=4, primary_key=True)       # 상품 코드
    p_name = models.CharField(max_length=20)        # 상품 이름
    price = models.IntegerField(default=0)          # 상품 가격
    image_path = models.CharField(max_length=200, null=True)      # 상품 이미지 경로
    user_image_path = models.ImageField(null=True, upload_to="", blank=True)    # 관리자가 등록한 상품 이미지 경로
    p_desc = models.CharField(max_length=200)       # 상품 설명

    def __str__(self):
        return self.p_code


class Cart(models.Model):
    m_id = models.ForeignKey(Member, on_delete=models.CASCADE, db_column="m_id")        # 회원 id
    tid = models.CharField(max_length=128, default='0')  # 결제 고유 번호
    check = models.BooleanField(default=False)  # 승인(결제)여부
    c_code = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="c_code")  # 점포 코드


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    p_code = models.ForeignKey(Product, on_delete=models.CASCADE, db_column="p_code")       # 상품 코드
    cnt = models.IntegerField()  # 상품 수량
    opt = models.BooleanField(default=False)  # 음료 옵션(iced:True/ hot:False)


class Pay(models.Model):
    c_code = models.ForeignKey(Company, on_delete=models.CASCADE, db_column="c_code")   # 점포 코드
    m_id = models.ForeignKey(Member, on_delete=models.CASCADE, db_column="m_id")        # 회원 id
    date = models.DateTimeField(null=True, default=None)     # 결제 날짜
    total = models.IntegerField(null=False)       # 총 결제 금액

    def __str__(self):
        return self.m_id


class PayItem(models.Model):
    pay = models.ForeignKey(Pay, on_delete=models.CASCADE)
    p_code = models.ForeignKey(Product, on_delete=models.CASCADE, db_column="p_code")  # 상품 코드
    cnt = models.IntegerField()  # 상품 수량
    opt = models.BooleanField(default=False)  # 음료 옵션(iced:True/ hot:False)

