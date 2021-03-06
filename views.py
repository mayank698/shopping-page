from django.shortcuts import render
from .models import product,Contact,Order,OrderUpdate
from math import ceil
from django.http import HttpResponse
import json
def index(request):
    allprods=[]
    catprods=product.objects.values('category','id')
    cats={item['category']for item in catprods}
    for cat in cats:
        prod=product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) + (n // 4))
        allprods.append([prod,range(1,nSlides),nSlides])
    params={'allprods':allprods}
    return render(request,"shop/index.html", params)
def about(request):
    return render(request,"shop/about.html")
def contact(request):
    if request.method=="POST":
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        query=request.POST.get('query','')
        contact=Contact(name=name, email=email, phone=phone, query=query)
        print(name,email,phone,query)
        contact.save()
        submit = True;
        return render(request,"shop/contact.html",{'submit':submit})
    return render(request,"shop/contact.html")
def tracker(request):
    if request.method=="POST":
        order_id=request.POST.get('order_id','')
        email=request.POST.get('email','')
        try:
            order=Order.objects.filter(order_id=order_id, email=email)
            if len(order)>0:
                update=OrderUpdate.objects.filter(order_id=order_id)
                updates=[]
                for item in update:
                    updates.append({'text':item.update_desc,'time':item.timestamp})
                    response=json.dumps(updates, default=str)
                    return HttpResponse(response)
            else:
                pass
        except Exception as e:
            pass
    return render(request,"shop/tracker.html")
def search(request):
    return render(request,"shop/search.html")
def checkout(request):
    if request.method=="POST":
        items_json=request.POST.get('ItemsJSON','')
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        address=request.POST.get('address','')+" "+request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')
        phone=request.POST.get('phone','')
        zip_code=request.POST.get('zip_code','')
        order=Order(items_json=items_json,name=name, email=email, address=address, city=city, zip_code=zip_code, phone=phone, state=state)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank=True;
        id=order.order_id
        return render(request,"shop/checkout.html",{'thank':thank,'id':id})
    return render(request,"shop/checkout.html")
def product_view(request,myid):
    Product = product.objects.filter(id=myid)
    return render(request,"shop/product_view.html",{'product':Product[0]})
