from django.shortcuts import render, redirect
from myapp.models import Contact, Product, Orders, OrderUpdate
from django.contrib import messages
from math import ceil
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

# import razorpay


# Create your views here.
def index(request):
    allProds = []
    catprods = Product.objects.values("category", "id")
    # print(catprods)
    cats = {item["category"] for item in catprods}
    # print(catprods)
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params = {"allProds": allProds}

    return render(request, "index.html", params)


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        pnumber = request.POST.get("pnumber")
        myquery = Contact(name=name, email=email, desc=desc, phonenumber=pnumber)
        myquery.save()
        messages.info(request, "We will get back to you soon..")

    return render(request, "contact.html")


def about(request):
    return render(request, "about.html")


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect("/auth/login")

    if request.method == "POST":
        items_json = request.POST.get("itemsJson", "")
        name = request.POST.get("name", "")
        amount = request.POST.get("amt")
        order_currency = request.POST.get("INR")
        email = request.POST.get("email", "")
        address1 = request.POST.get("address1", "")
        address2 = request.POST.get("address2", "")
        city = request.POST.get("city", "")
        state = request.POST.get("state", "")
        zip_code = request.POST.get("zip_code", "")
        phone = request.POST.get("phone", "")
        Order = Orders(
            items_json=items_json,
            name=name,
            amount=amount,
            email=email,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
        )
        print(amount)
        Order.save()
        update = OrderUpdate(
            order_id=Order.order_id, update_desc="The Order has been placed..."
        )
        update.save()
        thank = True

    # razorpay_client = razorpay.Client(
    # auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET)
    #     )

    # razorpay_order = razorpay_client.order.create(
    # dict(amount=amount, payment_capture=1)
    #     )
    # razorpay_order_id = razorpay_order["id"]
    # callback_url = 'paymenthandler/'
    # context = {}
    # context['razorpay_order_id'] = order_id
    # context['razorpay_merchant_id'] = settings.RAZOR_KEY_ID
    # context['razorpay_amount'] = amount
    # context['callback_url'] = callback_url

    return render(request, "checkout.html")


@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == "CHECKSUMHASH":
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, key, checksum)
    if verify:
        if response_dict["RESPCODE"] == "01":
            print("order successful")
            a = response_dict["ORDERID"]
            b = response_dict["TXNAMOUNT"]
            rid = a.replace("WebShop Cart", "")

            print(rid)
            filter2 = Orders.objects.filter(order_id=rid)
            print(filter2)
            print(a, b)
            for post1 in filter2:
                post1.oid = a
                post1.amountpaid = b
                post1.paymentstatus = "PAID"
                post1.save()
            print("run agede function")
        else:
            print("order was not successful because" + response_dict["RESPMSG"])
    return render(request, "paymentstatus.html", {"response": response_dict})


def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect("/auth/login")
    currentuser = request.user.username
    items = Orders.objects.filter(email=currentuser)
    rid = ""
    for i in items:
        print(i.oid)
        # print(i.order_id)
        myid = i.oid
        rid = myid.replace("WebShop Cart", "")
        print(rid)
    status = OrderUpdate.objects.filter(order_id=int(rid))
    for j in status:
        print(j.update_desc)

    context = {"items": items, "status": status}
    # print(currentuser)
    return render(request, "profile.html", context)


def payment(request):
    return render(request, "payment.html")


def succes(request):
    return render(request, "succes.html")


def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Login & Try Again")
        return redirect("/auth/login")
    currentuser = request.user.username
    items = Orders.objects.filter(email=currentuser)
    rid = ""
    for i in items:
        print(i.oid)
        # print(i.order_id)
        myid = i.oid
        rid = myid.replace("WebShoppers", "")
        print(rid)
    # status = OrderUpdate.objects.filter(order_id=int(rid))
    # for j in status:
    #     print(j.update_desc)
    context = {"items": items}

    return render(request, "profile.html",context)
