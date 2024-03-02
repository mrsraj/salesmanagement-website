from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.template import loader
from django.contrib import messages
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta,datetime

from django.db.models import Avg,Sum,F,DateField
from django.db.models.functions import TruncMonth



# DataBases Table Import:
from .models import user, customer, service,Payment

# Create your views here.


def registerpage(request):
    RegForm = loader.get_template("RegistrationForm.html")
    return HttpResponse(RegForm.render())


def AboutFun(request):
    AboutPage = loader.get_template("Page.html")
    return HttpResponse(AboutPage.render())


@csrf_exempt
def savedata(request):
    name = request.POST["fname"]
    mob = int(request.POST["phone"])
    email = request.POST["Email"]
    paswd = request.POST["pswd"]

    # member = user.objects.create(name=name, email=email, mobile=mob,pswd=paswd)

    try:
        member = user(name=name, email=email, mobile=mob, pswd=paswd)
        member.save()
    except IntegrityError as err:
        v = err.args[1]
        if "@gmail.com" in v:
            return HttpResponse(
                "This email id alreay exist Please enter other Gmail Id:"
            )
        else:
            return HttpResponse(
                "This Mobile No alreay exist Plase enter other Mobile No:"
            )

    return HttpResponseRedirect("/")


def loginpage(request):
    LoginPage = loader.get_template("login.html")
    return HttpResponse(LoginPage.render())


@csrf_exempt
def pswdverify(request):
    emailid = request.POST["uname"]
    pswd1 = request.POST["psw"]
    userpswd = user.objects.filter(email=emailid, pswd=pswd1).values()
    if len(userpswd) > 0:
        request.session["userAccount"] = emailid
        request.session["userId"] = userpswd[0]["id"]

        return HttpResponseRedirect("/dashboard/")
    else:
        return HttpResponse("email or password is invalid")


def dashboardpage(request):
    if "userAccount" in request.session:
        dashboard = loader.get_template("dashboard.html")
        return HttpResponse(dashboard.render())
    else:
        return HttpResponseRedirect("/")


def CustomerPage(request):
    if "userAccount" in request.session:

        CustForm = loader.get_template("CustRegistrationForm.html")

        return HttpResponse(CustForm.render())
    else:

        return HttpResponseRedirect("/")


@csrf_exempt
def CustomerData(request):
    if "userAccount" not in request.session:
        messages.error(request, "User not logged in")
        return HttpResponseRedirect("/")

    name = request.POST["Name"]
    addr = request.POST["Addr"]
    Mob_No1 = int(request.POST["Mob_No"])
    fk_User_Id1 = user.objects.get(id=request.session["userId"])
    type = request.POST["Type"]

    Data = customer(
        Name=name, Mob_No=Mob_No1, Addr=addr, fk_User_Id=fk_User_Id1, Type=type
    )
    try:
        Data.save()
        messages.success(request, "Data saved successfully.")
    except Exception as err:
        messages.error(request, "Somthin is Wrong.")

    return render(request, 'CustRegistrationForm.html')


@csrf_exempt
def Add_Service(request):
    id =  user.objects.get(id=request.session["userId"])
    Name1 = request.POST["name"]
    Type1 = request.POST["Type"]
    Date1 = request.POST["Date"]
    Rate1 = request.POST["rate"]
    Qty = request.POST["quantity"]
    # fk_User_Id1 = user.objects.get(id=id)
    fk_User_Id1=id
    fk_customer_Id1 = customer.objects.get(id=5)

    Data = service(
        Name=Name1,
        Qantity=Qty,
        Date=Date1,
        Rate=Rate1,
        Type=Type1,
        fk_User_Id=fk_User_Id1,
        fk_customer_Id=fk_customer_Id1,
    )
    try:
        Data.save()
        messages.success(request, "Data saved successfully.")
    except Exception as err:
        messages.error(request, "Somthin is Wrong.")
    return render(request, 'dashboard.html')


def ShowClient(request):
    id =  user.objects.get(id=request.session["userId"])
    clientData = {
        'DataSet': customer.objects.filter(fk_User_Id = id,Type  = "Client")
    }
    return render(request,'ClientShowTable.html',clientData)


def ShowSupplier(request):
    id =  user.objects.get(id=request.session["userId"])
    SupplierData = {
        'DataSet': customer.objects.filter(fk_User_Id = id, Type = "Supplier")
    }
    return render(request,'ClientShowTable.html',SupplierData)


def logout(request):
    request.session.flush()
    return HttpResponseRedirect("/")


def delete(request,Id):
  member = customer.objects.get(id=Id)
  member.delete()
  return HttpResponse('Deleted')


def detailsPage(request):
    
    current_month = datetime.now().month
    # year = datetime.now().year
    # day = datetime.now().day
    filterdata={
        'today_Purchase' : service.objects.filter(Type = "Supplier",Date=datetime.now().date()).aggregate(Sum("Qantity", default=0)),
        'today_Purchase_price' : service.objects.filter(Type = "Supplier",Date=datetime.now().date()).aggregate(price = Sum(F("Qantity")*F('Rate'))),
        
        'today_Selling' : service.objects.filter(Type = "Client",Date=datetime.now().date()).aggregate(Sum("Qantity", default=0)),
        'today_Selling_price' : service.objects.filter(Type = "Client",Date=datetime.now().date()).aggregate(price = Sum(F("Qantity")*F('Rate'))),
        
        'current_month_Purchase' : service.objects.filter(Type = "Supplier",Date__month=current_month).aggregate(sum = Sum('Qantity',default=0)),
        'current_mon_Purchase_price' : service.objects.filter(Type = "Supplier",Date__month=current_month).aggregate(price = Sum(F("Qantity")*F('Rate'))),
        
        'current_month_selling' : service.objects.filter(Type = "Client",Date__month=current_month).aggregate(sum = Sum('Qantity',default=0)),
        'current_month_selling_price' : service.objects.filter(Type = "Client",Date__month=current_month).aggregate(price = Sum(F("Qantity")*F('Rate'))),
    }
    return render(request,'DetailsPage.html',filterdata)
    # return HttpResponse(list(filterdata.items()))
    
    # return HttpResponse("Execute")
    


def apifunction(request,type):
    if type=="Client":
        data = list(customer.objects.filter(Type="Client").values('Name','id'))  
    else:
        data = list(customer.objects.filter(Type="Supplier").values('Name','id'))
        
    return JsonResponse(data,safe=False)
    # return HttpResponse(client_data)
        
        
def PaymentPage(request):
    page = loader.get_template('PayDetails.html')
    return HttpResponse(page.render())
    
@csrf_exempt
def PaymentForm(request):
    paymentPage = loader.get_template('PaymentForm.html')
    return HttpResponse(paymentPage.render())
        
