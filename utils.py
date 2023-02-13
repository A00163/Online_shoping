from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('41443864613346764B494D70387A3775306F4A4B3979763972444C6F6751593637306179627037626C70553D')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'Your verification code: {code}'
        }
        response = api.sms_send(params)
        # print(response)
        print(params.message)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
