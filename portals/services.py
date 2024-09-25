import jwt
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def generate_token(mobile_number):
    payload = {
        "mobile_number" :mobile_number
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


def user_verification_email(mail, otp):
    subject = "Vecto Password  Reset OTP "
    msg = "Your one time password for resetting the password at <strong> Vecto </strong> is as follows: <strong>{}</strong> <br>\nPlease do not share this with anyone.".format(otp)
    # Create an EmailMultiAlternatives object to support HTML content 
    email = EmailMultiAlternatives(subject, msg, '33azharoddin@gmail.com', [mail])
    email.attach_alternative(msg, "text/html")  # Specify HTML content type
    
    try:
        res = email.send()
        if res == 1:
            msg = 1
        else:
            print("no")
            msg = 0
    except Exception as e:
        print(e)
        msg = 0
    
    return msg




from django.core.paginator import Paginator, EmptyPage
def paginate_model_data(model, serializer, request, filter_key=None):
    try:
        limit = max(int(request.GET.get('limit', 0)), 1)
        page_number = max(int(request.GET.get('page', 0)), 1)
        if filter_key:
            filter_value = request.GET.get(filter_key)
            data = model.objects.filter(**{filter_key: filter_value})
        else:
            data = model.objects.all()
        paginator = Paginator(data, limit)
        try:
            current_page_data = paginator.get_page(page_number)
        except EmptyPage:
             return Response({"error": True, "message": "Page not found"}, status=status.HTTP_404_NOT_FOUND)
        serialized_data = serializer(current_page_data, many=True).data
        response_data = {
            "error": False,
            "pages_count": paginator.num_pages,
            "count": paginator.count,
            "rows": serialized_data
        }
        return response_data
    except Exception as e:
        return Response({"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


from django.db.models import Q
def paginate_data(model, serializer, request,data):
    try:
        limit = int(request.GET.get('limit', 1))
        page_number = int(request.GET.get('page', 1))
        search   = request.GET.get('search')
        data = data
        if search:
                q_objects = Q()
                for field in model._meta.fields:
                    if not field.is_relation:
                        q_objects |= Q(**{f"{field.name}__icontains": search})
                    elif hasattr(field, 'related_model'):
                        related_model = field.related_model
                        if related_model:
                            for related_field in related_model._meta.fields:
                                if not related_field.is_relation:
                                    q_objects |= Q(**{f"{field.name}__{related_field.name}__icontains": search})
                data = model.objects.filter(q_objects)  
        else :   
                data = data
        print("azhar is here ----------------")
        print("data",data)         
        paginator = Paginator(data, limit)

        try:
            current_page_data = paginator.get_page(page_number)
        except EmptyPage:
            return Response({"error": True, "message": "Page not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            serialized_data = serializer(current_page_data, many=True).data
        except Exception as e:
            return Response({"error": True, "message": f"Serialization error: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        response_data = {
            "error": False,
            "pages_count": paginator.num_pages,
            "count": paginator.count,
            "rows": serialized_data
        }
        return response_data
    except Exception as e:
        return Response({"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    


from datetime import datetime, timedelta
def generate_one_hour_time_slots(opening_time, closing_time):
    slots = []
    current_time = opening_time
    while current_time + timedelta(minutes=30) <= closing_time:
        start_time_str = current_time.strftime('%I:%M %p')
        end_time_str = (current_time + timedelta(minutes=30)).strftime('%I:%M %p')
        slots.append((start_time_str, end_time_str))
        current_time += timedelta(minutes=30)
    return slots



import datetime
def find_available_slots(booked_slots, generated_slots):
  available_slots = generated_slots.copy()  # Copy generated slots to avoid modifying original data
  for booked_slot in booked_slots:
    booked_start_time = booked_slot[0]
    booked_end_time = booked_slot[1]
    for i in range(len(available_slots)):
      available_start_time = available_slots[i][0]
      available_end_time = available_slots[i][1]
      # Check if booked slot overlaps with available slot
      if is_overlapping(booked_start_time, booked_end_time, available_start_time, available_end_time):
        del available_slots[i]  
        break  

  return available_slots

def is_overlapping(start1, end1, start2, end2):
  # Convert times to datetime objects for comparison
  datetime_start1 = datetime.datetime.strptime(start1, "%I:%M %p")
  datetime_end1 = datetime.datetime.strptime(end1, "%I:%M %p")
  datetime_start2 = datetime.datetime.strptime(start2, "%I:%M %p")
  datetime_end2 = datetime.datetime.strptime(end2, "%I:%M %p")
  # Check if one slot starts before the other ends
  return (datetime_start1 < datetime_end2) and (datetime_start2 < datetime_end1)


# from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
# from phonepe.sdk.pg.env import Env
# from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest

# def check_payment_status(transaction_id):
#     try:
#         merchant_id = settings.TEST_MERCHANT_ID 
#         salt_key = settings.TEST_SALT_KEY 
#         salt_index = settings.TEST_SALT_INDEX
#         env = settings.TEST_ENV
#         phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)
#         print("transaction_id", transaction_id)
#         transaction_status_response = phonepe_client.check_status(merchant_transaction_id=transaction_id)
#         transaction_state = transaction_status_response.data.state
#         invoice  = Invoice.objects.filter(transaction_id=transaction_id)
#         current_status = {
#             "status": transaction_status_response.code,
#             "message": transaction_status_response.message,
#             "transaction_state": transaction_status_response.data.state
#         }
        
#         return current_status
#     except Exception as e:
#         return {'error': str(e)}
    
