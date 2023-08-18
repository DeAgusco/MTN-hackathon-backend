
import requests
import json
import uuid
from basicauth import encode


class PayClass():
    # ================================================================================ Variables & Keys

    # Collections Subscription Key:
    collections_subkey = "92f5c0ede8e143c1b91b093482f200da"

    # Disbursement subscription key
    disbursements_subkey = "bddbeffef9b44de79849ab5fd4effa0e"

    # Production collections basic authorisation key(Leave it blank if in sandbox mode)
    basic_authorisation_collections = ""

    # Production disbursement basic authorisation key(Leave it blank if in sandbox mode)
    basic_authorisation_disbursments = ""

    # API user and Key(Note: Only use this when in production mode)
    collections_apiuser = ""
    api_key_collections = ""

    # API user and Key(Note: Only use this when in production mode)
    disbursements_apiuser = ""
    api_key_disbursements = ""

    # Application mode
    environment_mode = "sandbox"
    accurl = "https://proxy.momoapi.mtn.com"
    if environment_mode == "sandbox":
        accurl = "https://sandbox.momodeveloper.mtn.com"

    # Generate Basic authorization key when it test mode
    if environment_mode == "sandbox":
        collections_apiuser = str(uuid.uuid4())
        disbursements_apiuser = str(uuid.uuid4())

    # ================================================================================ Collections Code

    # ============= Create API user

    url = ""+str(accurl)+"/v1_0/apiuser"

    payload = json.dumps({
        "providerCallbackHost": "URL of host ie google.com"
    })

    headers = {
        'X-Reference-Id': collections_apiuser,
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': collections_subkey
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # ============= Create API key

    url = ""+str(accurl)+"/v1_0/apiuser/"+str(collections_apiuser)+"/apikey"

    payload = {}
    headers = {
        'Ocp-Apim-Subscription-Key': collections_subkey
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print("The response is: \n"+str(response))
    response = response.json()

    # Auto generate when in test mode
    if environment_mode == "sandbox":
        api_key_collections = str(response["apiKey"])

    # Create basic key for Collections
    username, password = collections_apiuser, api_key_collections

    basic_authorisation_collections = encoded_str = str(
        encode(username, password))
    # print(basic_authorisation_collections)

    # API User
    #print("Api user:"+collections_apiuser+"\n")
    #print("Api Key:"+api_key_collections)

    # ============= Action Functions for collections
    @staticmethod
    def check_disbursement_status(reference_id):
        url = f"{PayClass.accurl}/disbursement/v1_0/transfer/{reference_id}"
        headers = {
            'Authorization': "Bearer " + str(PayClass.momotokendisbursement().get("access_token")),
            'X-Target-Environment': PayClass.environment_mode,
            'Ocp-Apim-Subscription-Key': PayClass.disbursements_subkey,
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data
            else:
                # Handle error or return an error response
                error_message = f"Failed to check disbursement status. Status Code: {response.status_code}, Response: {response.text}"
                raise ValueError(error_message)
        except Exception as e:
            # Handle error or return an error response
            error_message = f"Failed to check disbursement status. Error: {str(e)}"
            raise ValueError(error_message)

    @staticmethod
    def request_to_transfer(amount, currency, txt_ref, phone_number):
        uuidgen = str(uuid.uuid4())
        url = ""+str(PayClass.accurl)+"/disbursement/v1_0/transfer"
        headers = {
            'Authorization': "Bearer " + str(PayClass.momotokendisbursement().get("access_token")),
            'X-Reference-Id': uuidgen,
            'X-Target-Environment': PayClass.environment_mode,
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': PayClass.disbursements_subkey,
        }
        payload = json.dumps({
            "amount": amount,
            "currency": currency,
            "externalId": txt_ref,
            "payee": {
                "partyIdType": "MSISDN",
                "partyId": phone_number
            },
            "payerMessage": "Disbursement from virtual wallet",
            "payeeNote": "Disbursement from virtual wallet"
        })

        try:
            response = requests.post(url, headers=headers, data=payload)
            if response.status_code == 202:
                data = response.status_code
                return {"status":data, "ref":uuidgen}
            else:
                # Handle error or return an error response
                error_message = f"Failed to initiate disbursement. Status Code: {response.status_code}, Response: {response.text}"
                raise ValueError(error_message)
        except Exception as e:
            # Handle error or return an error response
            error_message = f"Failed to initiate disbursement. Error: {str(e)}"
            raise ValueError(error_message)
    @staticmethod
    def request_to_withdraw(amount, currency, txt_ref, phone_number):
        uuidgen = str(uuid.uuid4())
        url = ""+str(PayClass.accurl)+"/collection/v1_0/requesttowithdraw"
        headers = {
            'Authorization': "Bearer " + str(PayClass.momotoken().get("access_token")),
            'X-Reference-Id': uuidgen,
            'X-Target-Environment': PayClass.environment_mode,
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': PayClass.collections_subkey,
        }
        payload = json.dumps({
            "amount": amount,
            "currency": currency,
            "externalId": txt_ref,
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": phone_number
            },
            "payerMessage": "Withdrawal from virtual wallet",  
            "payeeNote": "Withdrawal from virtual wallet"  
        })

        try:
            response = requests.post(url, headers=headers, data=payload)
            d = response.status_code
            return d
        except Exception as e:
            # Handle error, raise an exception, or return an error response
            error_message = f"Failed to initiate withdrawal. Error: {str(e)}"
            raise ValueError(error_message)
    @staticmethod
    def get_basic_user_info(account_holder_msisdn):
        url = f"{PayClass.accurl}/collection/v1_0/accountholder/msisdn/{account_holder_msisdn}/basicuserinfo"
        headers = {
            'Authorization': "Bearer " + str(PayClass.momotoken().get("access_token")),
            'X-Target-Environment': PayClass.environment_mode,
            'Ocp-Apim-Subscription-Key': PayClass.collections_subkey,
        }

        try:
            response = requests.get(url, headers=headers)
            data = response.json()
            return data
        except Exception as e:
            # Handle error, raise an exception, or return an error response
            error_message = f"Failed to fetch basic user information. Error: {str(e)}"
            raise ValueError(error_message)
   # Add 'staticmethod' decorator to make it a static method
    @staticmethod
    def momotoken():
        url = f"{PayClass.accurl}/collection/token/"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': PayClass.collections_subkey,
            'Authorization': str(PayClass.basic_authorisation_collections)
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        # Check if the response is successful
        if response.status_code == 200:
            authorization_token = response.json()
            return authorization_token
        else:
            # Handle error, raise an exception, or return an error response
            return response.json()
            

    def momopay(amount, currency, txt_ref, phone_number, payermessage):
        # UUID V4 generator
        uuidgen = str(uuid.uuid4())
        url = ""+str(PayClass.accurl)+"/collection/v1_0/requesttopay"

        payload = json.dumps({
            "amount": amount,
            "currency": currency,
            "externalId": txt_ref,
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": phone_number
            },
            "payerMessage": payermessage,
            "payeeNote": payermessage
        })
        headers = {
            'X-Reference-Id': uuidgen,
            'X-Target-Environment': PayClass.environment_mode,
            'Ocp-Apim-Subscription-Key': PayClass.collections_subkey,
            'Content-Type': 'application/json',
            'Authorization': "Bearer "+str(PayClass.momotoken()["access_token"])
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        context = {"response": response.status_code, "ref": uuidgen}

        return context

    def verifymomo(txn):
        url = ""+str(PayClass.accurl) + \
            "/collection/v1_0/requesttopay/"+str(txn)+""

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': PayClass.collections_subkey,
            'Authorization':  "Bearer "+str(PayClass.momotoken()["access_token"]),
            'X-Target-Environment': PayClass.environment_mode,
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        json_respon = response.json()

        return json_respon

    # Check momo collections balance
    def momobalance():
        url = ""+str(PayClass.accurl)+"/collection/v1_0/account/balance"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': PayClass.collections_subkey,
            'Authorization':  "Bearer "+str(PayClass.momotoken()['access_token']),
            'X-Target-Environment': PayClass.environment_mode,
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        
        json_respon = response.json()

        return json_respon

    # ================================================================================ Disbursements Code

    # ============= Create API user

    url = ""+str(accurl)+"/v1_0/apiuser"

    payload = json.dumps({
        "providerCallbackHost": "URL of host ie google.com"
    })

    headers = {
        'X-Reference-Id': disbursements_apiuser,
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': disbursements_subkey
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # ============= Create API key

    url = ""+str(accurl)+"/v1_0/apiuser/"+str(disbursements_apiuser)+"/apikey"

    payload = {}
    headers = {
        'Ocp-Apim-Subscription-Key': disbursements_subkey
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    #print("The response is: \n"+str(response))
    response = response.json()

    # Auto generate when in test mode
    if environment_mode == "sandbox":
        api_key_disbursements = str(response["apiKey"])

    # Create basic key for Collections
    username, password = disbursements_apiuser, api_key_disbursements

    basic_authorisation_disbursments = encoded_str = str(
        encode(username, password))

    # print(basic_authorisation_disbursments)

    # API User
    #print("Api user:"+collections_apiuser+"\n")
    # print("Api Key:" + api_key_disbursements)

    # ============= Action Functions for disbursements

    # Momo disbursement token generation
    def momotokendisbursement():
        url = ""+str(PayClass.accurl)+"/disbursement/token/"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': PayClass.disbursements_subkey,
            'Authorization': str(PayClass.basic_authorisation_disbursments)
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        authorization_token = response.json()

        return authorization_token

    # Check Disubursement balance
    def momobalancedisbursement():
        url = ""+str(PayClass.accurl)+"/disbursement/v1_0/account/balance"

        payload = {}
        headers = {
            'Ocp-Apim-Subscription-Key': PayClass.disbursements_subkey,
            'Authorization':  "Bearer "+str(PayClass.momotokendisbursement()["access_token"]),
            'X-Target-Environment': PayClass.environment_mode,
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        json_respon = response.json()

        return json_respon

    # Withdraw money Disbursement
    def withdrawmtnmomo(amount, currency, txt_ref, phone_number, payermessage):
        # UUID V4 generator
        uuidgen = str(uuid.uuid4())
        url = ""+str(PayClass.accurl)+"/disbursement/v1_0/transfer"

        payload = json.dumps({
            "amount": amount,
            "currency": currency,
            "externalId": txt_ref,
            "payee": {
                "partyIdType": "MSISDN",
                "partyId": phone_number
            },
            "payerMessage": payermessage,
            "payeeNote": payermessage
        })

        headers = {
            'X-Reference-Id': uuidgen,
            'X-Target-Environment': PayClass.environment_mode,
            'Ocp-Apim-Subscription-Key': PayClass.disbursements_subkey,
            'Content-Type': 'application/json',
            'Authorization': "Bearer "+str(PayClass.momotokendisbursement()["access_token"])
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        context = {"response": response.status_code, "ref": uuidgen}

        return context

    # Check transfer status disbursment
    def checkwithdrawstatus(txt_ref):

        # UUID V4 generator
        uuidgen = str(uuid.uuid4())

        url = str(PayClass.accurl) + \
            "/disbursement/v1_0/transfer/" + str(txt_ref)

        payload = {}

        headers = {
            'X-Reference-Id': uuidgen,
            'X-Target-Environment': PayClass.environment_mode,
            'Ocp-Apim-Subscription-Key': PayClass.disbursements_subkey,
            'Content-Type': 'application/json',
            'Authorization': "Bearer " + str(PayClass.momotokendisbursement()["access_token"])
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        returneddata = response.json()

        print(returneddata)

        context = {
            "response": response.status_code,
            "ref": txt_ref,
            "data": returneddata
        }

        return context
