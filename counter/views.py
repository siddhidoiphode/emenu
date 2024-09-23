
from django.http import HttpResponse
# from django.contrib import redirects
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages






def counter_home(request):
    table_numbers=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    context={'table_numbers':table_numbers}
    return render(request,'counter/counter_home.html',context)

def login_view(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('counter_home')
        else:
            messages.error(request,'Invalid user or password..')
            return render(request,'counter/login.html')
    return render(request,"counter/login.html")

def logout_view(request):
    logout(request)
    return login_view(request)







def menu(request):
    return render(request,'counter/menu.html')

def tableList1(request):
    tab=request.GET.get('tab','recent')
    table_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15]  # Example: Replace with your logic to get table numbers
    if tab == 'all':
        template_name = 'counter/tableList.html'
        context = {'table_numbers': table_numbers}
    else:
        template_name = 'counter/counter_home.html'
        context = {'table_numbers': table_numbers}

    return render(request, template_name, context)

from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def get_table_receipt(request, table_number):
    # print(f"Table number requested: {table_number}")
    receipt_data = {
        "1": {
            "customer_name": "John Doe",
            "order_no": "1",
            "date": "15th September 2024",
            "items": [
                {"item": "Grilled Chicken", "qty": 2, "price": "$10.00", "total": "$20.00"},
                {"item": "French Fries", "qty": 1, "price": "$05.00", "total": "$05.00"},
                {"item": "Soda", "qty": 2, "price": "$03.00", "total": "$06.00"},
            ],
            "subtotal": "$31.00",
            "tax": "$2.48",
            "total": "$33.48"
        },
        "2": {
            "customer_name": "Jane Smith",
            "order_no": "789012",
            "date": "16th September 2024",
            "items": [
                {"item": "Burger", "qty": 1, "price": "$8.00", "total": "$8.00"},
                {"item": "Salad", "qty": 1, "price": "$6.00", "total": "$6.00"},
                {"item": "Juice", "qty": 1, "price": "$4.00", "total": "$4.00"},
            ],
            "subtotal": "$18.00",
            "tax": "$1.44",
            "total": "$19.44"
        }
        # Add more table numbers as needed
    }

    # Fetch data based on table_number or return an error if not found
    data = receipt_data.get(str(table_number), {
        "error": "No data found for this table number."
    })

    return JsonResponse(data)
