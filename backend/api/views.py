from django.http import JsonResponse
from rest_framework.decorators import api_view
from .pay import PayClass
from rest_framework.response import Response
from rest_framework.views import APIView
@api_view(['POST'])
def momo_pay(request):
    amount = request.data.get("amount")
    currency = request.data.get("currency")
    txt_ref = request.data.get("txt_ref")
    phone_number = request.data.get("phone_number")
    payer_message = request.data.get("payer_message")
   
    response_data = PayClass.momopay(amount, currency, txt_ref, phone_number, payer_message)

    return Response(response_data)

@api_view(['GET'])
def verify_momo_transaction(request, txn):
    response_data = PayClass.verifymomo(txn)
    return Response(response_data)

@api_view(['GET'])
def momo_balance(request):
    response_data = PayClass.momobalance()
    return Response(response_data)

@api_view(['GET'])
def get_basic_user_info(request, account_holder_msisdn):
    try:
        data = PayClass.get_basic_user_info(account_holder_msisdn)
        return Response(data)
    except ValueError as e:
        return Response({"error": str(e)}, status=500)
    
@api_view(['POST'])
def initiate_withdrawal(request):
    data = request.data
    amount = data.get('amount')
    currency = data.get('currency')
    txt_ref = data.get('txt_ref')
    phone_number = data.get('phone_number')
    try:
        response_data = PayClass.request_to_withdraw(amount, currency, txt_ref, phone_number)
        return Response(response_data)
    except ValueError as e:
        return Response({"error": str(e)}, status=500)
    
class MoMoDisbursementView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract the required data from the request
        amount = request.data.get("amount")
        currency = request.data.get("currency")
        txt_ref = request.data.get("txt_ref")
        phone_number = request.data.get("phone_number")

        try:
            # Call the static method to initiate the disbursement
            response_data = PayClass.request_to_transfer(amount, currency, txt_ref, phone_number)
            return Response(response_data)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        
class MoMoDisbursementStatusView(APIView):
    def get(self, request, reference_id, *args, **kwargs):
        try:
            # Call the static method to check the disbursement status
            response_data = PayClass.check_disbursement_status(reference_id)
            return Response(response_data)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
