
from django.http import HttpResponse
# from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse



def kitchen_home(request):
    table_numbers=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    context={'table_numbers':table_numbers}
    return render(request,'kitchen/kitchen_home.html',context)

def tableList(request):
    tab=request.GET.get('tab','recent')
    table_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15]  # Example: Replace with your logic to get table numbers
    if tab == 'all':
        template_name = 'kitchen/tableList.html'
        context = {'table_numbers': table_numbers}
    else:
        template_name = 'kitchen/kitchen_home.html'
        context = {'table_numbers': table_numbers}

    return render(request, template_name, context)



def get_table_receipt(request, table_number):
    receipt_data = {
        "1": {
            "customer_name": "John Doe",
            "order_no": "123456",
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
    data = receipt_data.get(str(table_number), {
        "error": "No data found for this table number."
    })

    return JsonResponse(data)
