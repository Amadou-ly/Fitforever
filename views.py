import math
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from .models import *
from random import shuffle

# Create your views here.

def index(request):
    cats = Category.objects.all()
    categories = []
    for c in cats:
        sub = SubCategory.objects.filter(category=c.category_id)
        categories.append({'cat': c, 'sub': sub})
    cart = Cart.objects.filter(user=request.session.get('user_id')).order_by('-cart_id')
    count = 0

    for cart in cart:
        count += 1

    list_prod = []
    product_ = Items.objects.all()
    product_list = list(product_)
    shuffle(product_list)

    for prod in product_:
        dis = prod.price-((prod.price * prod.discount.discount) / 100)
        list_prod.append({'prod': prod, 'discount': math.ceil(dis)})

    return render(request, 'index.html', {'products': list_prod, "categories": categories, "count": count})


def contact(request):
    cats = Category.objects.all()
    categories = []

    for c in cats:
        sub = SubCategory.objects.filter(category=c.category_id)
        categories.append({'cat': c, 'sub': sub})

    product = Items.objects.all()
    cart = Cart.objects.filter(user=request.session.get('user_id')).order_by('-cart_id')
    count = 0

    for cart in cart:
        count += 1
    userInfo = Users.objects.filter(user_id=request.session.get('user_id')).first()

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        if 'user_id' in request.session:
            user = Users.objects.filter(user_id=request.session.get('user_id')).first()
            userInfo = user.username
        else:
            who = request.POST['email']
            userInfo = who
        C = Contact(user=userInfo,
                    subject=subject,
                    message=message)
        C.save()
        return redirect('index')
    else:
        return render(request, 'Contact.html', {'products': product, "categories": categories, "count": count})


def search(request):
    items = Items.objects.all()

    query = request.GET.get("q")
    if query:
        items = items.filter(title__icontains=query)

        cats = Category.objects.all()
        categories = []

        for c in cats:
            sub = SubCategory.objects.filter(category=c.category_id)
            categories.append({'cat': c, 'sub': sub})

        cart = Cart.objects.filter(user=request.session.get('user_id')).order_by('-cart_id')
        count = 0

        for cart in cart:
            count += 1

        list_prod = []
        for prod in items:
            dis = prod.price - ((prod.price * prod.discount.discount) / 100)
            list_prod.append({'prod': prod, 'discount': math.ceil(dis)})

        return render(request, 'category.html',
                      {'items': list_prod, 'query': query, "categories": categories, "count": count})


def cart(request):
    item = Items.objects.all()[:4]
    list_prod = []

    for prod in item:
        dis = prod.price-((prod.price * prod.discount.discount) / 100)
        list_prod.append({'prod': prod, 'discount': math.ceil(dis)})

    cats = Category.objects.all()
    categories = []
    cart = Cart.objects.filter(user=request.session.get('user_id'))
    prices = 0
    for cart in cart:
        prices += cart.total_cost

    for c in cats:
        sub = SubCategory.objects.filter(category=c.category_id)
        categories.append({'cat': c, 'sub': sub})

    carts = Cart.objects.filter(user=request.session.get('user_id')).order_by('-cart_id')
    count = 0
    for carts in carts:
        count += 1
    bag = Cart.objects.filter(user=request.session.get('user_id')).order_by('-cart_id')

    prod_list = []
    for prod in bag:
        dis = prod.price - ((prod.price * prod.discount) / 100)
        prod_list.append({'prod': prod, 'discount': math.ceil(dis)})

    return render(request, 'cart.html',
                  {'item': list_prod, "categories": categories, "bag": prod_list, "prices": prices,
                   "count": count})


def checkout(request):
    cats = Category.objects.all()
    categories = []

    address = Users.objects.filter(user_id=request.session.get('user_id'))

    cart = Cart.objects.filter(user=request.session.get('user_id'))
    prices = 0
    tot_disc = 0
    for cart in cart:
        prices += cart.total_cost
        disc = ((cart.price * cart.discount)/100)
        top = math.ceil(disc)
        tot_disc += top

    for c in cats:
        sub = SubCategory.objects.filter(category=c.category_id)
        categories.append({'cat': c, 'sub': sub})

    carts = Cart.objects.filter(user=request.session.get('user_id')).order_by('-cart_id')
    count = 0
    for carts in carts:
        count += 1

    bag = Cart.objects.filter(user_id=request.session.get('user_id'))
    list_prod = []
    for prod in bag:
        dis = prod.price - ((prod.price * prod.discount) / 100)
        list_prod.append({'prod': prod, 'discount': math.ceil(dis)})

    product = Items.objects.all()
    expensive = prices + 300

    return render(request, 'checkout.html',
                  {'product': product, "categories": categories, "bag": list_prod, "address": address, "prices": prices,
                   "count": count, "tot_disc": tot_disc, "expensive": expensive})


def category(request, cat, subCat=None):

    if subCat is None:
        product_ = Items.objects.filter(category_id=cat)
    else:
        product_ = Items.objects.filter(category_id=cat, subcategory_id=subCat)

    list_prod = []
    for prod in product_:
        dis = prod.price - ((prod.price * prod.discount.discount) / 100)
        list_prod.append({'prod': prod, 'discount': math.ceil(dis)})




    cats = Category.objects.all()
    categories = []
    cart = Cart.objects.filter(user=request.session.get('user_id')).order_by('-cart_id')
    count = 0

    for cart in cart:
        count += 1

    for c in cats:
        sub = SubCategory.objects.filter(category=c.category_id)
        categories.append({'cat': c, 'sub': sub})

    return render(request, 'category.html', {'products_': list_prod, "categories": categories, "count": count})


def product(request, id):
    cats = Category.objects.all()
    categories = []

    cart = Cart.objects.filter(user=request.session.get('user_id')).order_by('-cart_id')
    count = 0

    for cart in cart:
        count += 1

    for c in cats:
        sub = SubCategory.objects.filter(category=c.category_id)
        categories.append({'cat': c, 'sub': sub})

    related = Items.objects.all()
    product = Items.objects.filter(item_id=id).first()
    x = product.price - ((product.price * product.discount.discount) / 100)
    dis = math.ceil(x)
    return render(request, 'product.html',
                  {'product': product, "dis": dis, "categories": categories, 'related': related, "count": count})


def login(request):
    cats = Category.objects.all()
    categories = []

    for c in cats:
        sub = SubCategory.objects.filter(category=c.category_id)
        categories.append({'cat': c, 'sub': sub})

    product = Items.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        cust = Users.objects.filter(username=username, password=password)
        if len(cust) != 0:
            cust = cust[0]
            request.session['user_id'] = cust.user_id
            request.session['last_name'] = cust.last_name

            return redirect('index')
        else:
            messages.info(request, "Invalid Password or Username")
            return redirect('login')

    else:
        return render(request, 'login.html', {'product': product, "categories": categories})


def logout(request):
    auth.logout(request)
    return redirect('/')


def blog(request):
    cats = Category.objects.all()
    categories = []

    cart = Cart.objects.filter(user=request.session.get('user_id')).order_by('-cart_id')
    count = 0

    for cart in cart:
        count += 1

    for c in cats:
        sub = SubCategory.objects.filter(category=c.category_id)
        categories.append({'cat': c, 'sub': sub})

    product = Items.objects.all()
    user = Users.objects.filter(user_id=request.session.get('user_id')).first()
    blog = Blog.objects.all().order_by('-date')

    return render(request, 'blog.html',
                      {'products': product, "categories": categories, 'blog': blog, "count": count})


def signup(req):
    cats = Category.objects.all()
    categories = []

    for c in cats:
        sub = SubCategory.objects.filter(category=c.category_id)
        categories.append({'cat': c, 'sub': sub})
    if req.method == 'POST':
        username = req.POST['username']
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        email = req.POST['email']
        password = req.POST['password']
        confirmpassword = req.POST['confirmpassword']
        address = req.POST['address']
        address2 = req.POST['address2']
        country = req.POST['country']
        zipcode = req.POST['zipcode']
        phone = req.POST['phone']
        if password == confirmpassword:
            u = Users(username=username,
                      first_name=first_name,
                      last_name=last_name,
                      email=email,
                      password=password,
                      address=address,
                      address2=address2,
                      country=country,
                      zipcode=zipcode,
                      phone=phone)
            u.save()
            return render(req, 'login.html')
        else:
            messages.info(req, "Password not matching")
            return render(req, "signup.html")

    else:
        return render(req, 'signup.html', {"categories": categories})


def add_to_cart(request):
    item_id = request.POST['item_id']
    quantity = request.POST['quantity']
    sc = request.POST['sc']
    price = request.POST['price']
    image = request.POST['image']
    discount = request.POST['discount']

    userInfo = Users.objects.filter(user_id=request.session.get('user_id')).first()
    products = Items.objects.filter(item_id=item_id).first()
    sale = Items.objects.filter(price=price).first()
    rate = sale.price
    same = Cart.objects.filter(itemname=products, size=sc).first()

    if same is None:
        c = Cart(user=userInfo, quantity=quantity, itemname=products, size=sc, price=rate, image=image,
                 discount=discount)
        c.save()
    else:
        print(same)
        qty = same.quantity
        print(qty)
        q = int(quantity)
        if qty == 0:
            new_qty = q
        if qty != 0:
            new_qty = qty + q
        Cart.objects.filter(itemname=products, size=sc).delete()
        c = Cart(user=userInfo, quantity=new_qty, itemname=products, size=sc, price=rate, image=image,
                 discount=discount)
        c.save()

    return redirect('cart')


def remove(request, id_cart):
    Cart.objects.filter(cart_id=id_cart).delete()

    return redirect('cart')


def empty(request):
    Cart.objects.filter(user=request.session.get('user_id')).delete()
    return redirect('cart')


def write(request):
    userInfo = Users.objects.filter(user_id=request.session.get('user_id')).first()
    cats = Category.objects.all()
    categories = []
    cart = Cart.objects.filter(user=userInfo)
    count = 0

    for cart in cart:
        count += 1

    for c in cats:
        sub = SubCategory.objects.filter(category=c.category_id)
        categories.append({'cat': c, 'sub': sub})

    if request.method == 'POST':
        title = request.POST['title']
        caption = request.POST['caption']
        image = request.POST['image']
        B = Blog(title=title,
                 caption=caption,
                 image=image,
                 user=userInfo)
        B.save()
        return redirect('blog')

    else:
        return render(request, 'write.html', {"categories": categories, "count": count})


def account(request):
    cats = Category.objects.all()
    categories = []

    for c in cats:
        sub = SubCategory.objects.filter(category=c.category_id)
        categories.append({'cat': c, 'sub': sub})

    carts = Cart.objects.filter(user=request.session.get('user_id'))
    prices = 0
    for cart in carts:
        prices += cart.total_cost
    userInfo = Users.objects.filter(user_id=request.session.get('user_id')).first()
    display = Order.objects.filter(user=userInfo).order_by('-order_id')
    cart = Cart.objects.filter(user=request.session.get('user_id'))
    count = 0

    for cart in cart:
        count += 1

    user = Users.objects.filter(user_id=request.session.get('user_id'))
    cart = Cart.objects.filter(user=request.session.get('user_id')).order_by('-cart_id')
    bag = Cart.objects.filter(user=request.session.get('user_id')).order_by('-cart_id')

    return render(request, 'account.html',
                  {"user": user, "cart": cart, "prices": prices, "categories": categories, "count": count, "bag": bag,
                   "display": display})


def edit_profile(req):
    userInfo = req.session.get('user_id')
    cats = Category.objects.all()
    categories = []

    cart = Cart.objects.filter(user=userInfo)
    count = 0

    for cart in cart:
        count += 1

    for c in cats:
        sub = SubCategory.objects.filter(category=c.category_id)
        categories.append({'cat': c, 'sub': sub})
    user = Users.objects.filter(user_id=userInfo)
    if req.method == 'POST':
        username = req.POST['username']
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        email = req.POST['email']
        password = req.POST['password']
        confirmpassword = req.POST['confirmpassword']
        address = req.POST['address']
        address2 = req.POST['address2']
        country = req.POST['country']
        zipcode = req.POST['zipcode']
        phone = req.POST['phone']

        if password == confirmpassword:
            u = Users(user_id=userInfo, username=username, first_name=first_name, last_name=last_name, email=email,
                      password=password, address=address, address2=address2, country=country, zipcode=zipcode,
                      phone=phone)
            u.save()

            return render(req, 'login.html')

        else:
            messages.info(req, "Password not matching")
            return render(req, "signup.html")

    else:
        return render(req, 'edit_profile.html', {"categories": categories, "count": count, "user": user})


def order(request):
    count = Cart.objects.filter(user_id=request.session.get('user_id'))
    address_type = request.POST['shipping']
    delivery_type = request.POST['delivery']
    payment_type = request.POST['payment']
    address_line1 = request.POST['address_line1']
    address_line2 = request.POST['address_line2']
    country = request.POST['country']
    zipcode = request.POST['zipcode']
    paytm = request.POST['paytmno']
    username = request.POST['username']
    cardNumber = request.POST['cardNumber']
    month = request.POST['month']
    year = request.POST['year']

    userInfo = Users.objects.filter(user_id=request.session.get('user_id')).first()

    a = "Different"
    b = "Paytm"
    c = "Debit Card"
    for count in count:
        bag = Cart.objects.filter(user_id=request.session.get('user_id')).first()
        quantity = bag.quantity
        name = bag.itemname
        price = bag.price
        image = bag.image
        discount = bag.discount
        bag.delete()

        o = Order(user=userInfo, item=name, quantity=quantity, price=price, image=image,
                             delivery=delivery_type, payment=payment_type, address=address_type, discount=discount)
        o.save()
        id = o.order_id

        if address_type == a:
            A = Different_Address(user=userInfo,
                                  order_id=id,
                                  address_line1=address_line1,
                                  address_line2=address_line2,
                                  country=country,
                                  zipcode=zipcode)
            A.save()

        if payment_type == b:
            P = Paytm(user=userInfo,
                      order_id=id,
                      number=paytm)
            P.save()

        if payment_type == c:
            C = Card(user=userInfo,
                     order_id=id,
                     name=username,
                     card_no=cardNumber,
                     month=month,
                     year=year)
            C.save()

    return redirect('display_orders')


def display_orders(request):
    cats = Category.objects.all()
    categories = []

    for c in cats:
        sub = SubCategory.objects.filter(category=c.category_id)
        categories.append({'cat': c, 'sub': sub})

    userInfo = Users.objects.filter(user_id=request.session.get('user_id')).first()
    display = Order.objects.filter(user=userInfo).order_by('-order_id')
    cart = Cart.objects.filter(user=request.session.get('user_id')).order_by('-cart_id')

    prod_list = []
    for prod in display:
        dis = prod.price - ((prod.price * prod.discount) / 100)
        prod_list.append({'prod': prod, 'discount': math.ceil(dis)})

    count = 0
    for cart in cart:
        count += 1

    return render(request, "orders.html", {"display": prod_list, "count": count, "categories": categories})
