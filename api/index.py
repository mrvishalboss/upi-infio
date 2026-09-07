from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

token = "05habn4u599ywpp96estm1czy4tkf7008871"
user_id = "1442991132"

def upload_to_tmpfiles(image_url):
    try:
        img_response = requests.get(image_url)
        if img_response.status_code != 200:
            return None
        
        files = {'file': ('profile.jpg', img_response.content, 'image/jpeg')}
        upload_response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)
        upload_data = upload_response.json()
        
        if upload_data.get('status') == 'success':
            return upload_data['data']['url']
        return None
    except:
        return None

@app.route('/')
def home():
    return jsonify({
        "status": "running",
        "endpoint": "/fetch?upi=your_upi_id",
        "developer": "@Techvishalboss"
    })

@app.route('/fetch')
def fetch_mobile():
    target_upi = request.args.get('upi', '')
    
    if not target_upi:
        return jsonify({
            "success": False,
            "error": "UPI ID required",
            "usage": "/fetch?upi=example@paytm",
            "developer": "@Techvishalboss"
        })
    
    if not token or not user_id:
        return jsonify({
            "success": False,
            "error": "token and user_id not configured",
            "developer": "@Techvishalboss"
        })

    try:
        url = "https://upi.paytm.com/upi-pc-profile/ext/v1/user/details/receiver_vpa"

        params = {'deviceIdentifier': "OnePlus-CPH1234-e6b0df030376f96e",'playStore': "true",'osVersion': "16",'client': "androidapp",'lang_id': "1",'language': "en",'deviceManufacturer': "OnePlus",'networkType': "WIFI",'locale': "en-IN",'deviceName': "CPH1234",'version': "10.80.1",'child_site_id': "1",'site_id': "1"}

        headers = {'User-Agent': "Paytm Release/10.80.1/721958 (net.one97.paytm; source=com.android.vending; integrity=true; auth=true; en-IN; cronet 147.0.7727.49) Android/16 OnePlus/CPH1234 (arm64-v8a; resolution=3.0; cores=8) ",'x-id': "e6b0df030376f96e",'x-mfg': "OnePlus",'x-app-rid': "e6b0df030376f96e:1777971129165:1:13",'x-nw': "WIFI",'usertoken': token,'x-store': "1",'userid': user_id,'x-vpn': "false",'x-sim-sub-id': "1",'x-tamp': "0",'x-deb-status': "false",'request-token': "PTMc29a814de63a485610bf4233b3ae6392",'x-get-server-response-time': "true",'advertising_id': "013e7174-d740-19b8-7999-6ebc0460da6c",'x-clon': "0",'receivervpa': target_upi,'x-intg-src': "0",'x-loc': "0.0,0.0",'x-intg': "1",'x-call': "0",'x-model': "CPH1234",'x-locint': "false,0,true",'priority': "u=1, i"}

        response = requests.get(url, params=params, headers=headers).json()

        cust_id = None

        if response.get("status") == "SUCCESS":
            response_list = response.get("response", [])
            if response_list:
                cust_id = response_list[0].get("custId")

        if cust_id:
            url2 = "https://digitalapiproxy.paytm.com/pcchat/v1/api/user/registerNotify"
            
            params2 = {'deviceIdentifier': "OnePlus-CPH1234-e6b0df030376f96e",'playStore': "true",'osVersion': "16",'client': "androidapp",'lang_id': "1",'language': "en",'deviceManufacturer': "OnePlus",'networkType': "WIFI",'locale': "en-IN",'deviceName': "CPH1234",'version': "10.80.1",'child_site_id': "1",'site_id': "1"}
            
            payload = {"mobileNo": "","displayName": "","identifier": cust_id,"type": "CUSTOMER","paymentSource": "PAYTM_DISCOVERY_to_bank_upi_mt_toMobileSearch","sourceMethod": "interface"}
            
            headers2 = {'User-Agent': "Paytm Release/10.80.1/721958 (net.one97.paytm; source=com.android.vending; integrity=true; auth=true; en-IN; cronet 147.0.7727.49) Android/16 OnePlus/CPH1234 (arm64-v8a; resolution=3.0; cores=8) ",'sso_token': token,'x-id': "e6b0df030376f96e",'x-mfg': "OnePlus",'x-app-rid': "e6b0df030376f96e:1777971157592:2:16",'x-nw': "WIFI",'x-store': "1",'x-vpn': "false",'x-sim-sub-id': "1",'x-tamp': "0",'x-deb-status': "false",'advertising_id': "013e7174-d740-19b8-7999-6ebc0460da6c",'x-clon': "0",'x-intg-src': "0",'x-loc': "0.0,0.0",'x-intg': "1",'x-call': "0",'x-model': "CPH1234",'x-locint': "false,0,true",'content-type': "application/json; charset=utf-8",'priority': "u=1, i"}
            
            response2 = requests.post(url2, params=params2, data=json.dumps(payload), headers=headers2).json()
            
            if response2.get("success"):
                data = response2.get("data", {})
                user_info = data.get("userInfoByUserIdResponse", {})
                user_dto_map = user_info.get("userDTOMap", {})
                
                for uid, udata in user_dto_map.items():
                    phone = udata.get("phoneNumber")
                    name = udata.get("pfName")
                    profile_url = udata.get("imageUrl")
                    
                    if phone and name:
                        temp_url = None
                        if profile_url:
                            temp_url = upload_to_tmpfiles(profile_url)
                        
                        return jsonify({
                            "success": True,
                            "message": "UPI Details Fetched Successfully!",
                            "data": {
                                "name": name,
                                "phone": phone,
                                "upi_id": target_upi,
                                "profile_pic": temp_url
                            },
                            "developer": "@Techvishalboss"
                        })
            
            return jsonify({
                "success": False,
                "error": "Data not found",
                "developer": "@Techvishalboss"
            })
        
        return jsonify({
            "success": False,
            "error": "custId not found",
            "developer": "@Techvishalboss"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "developer": "@Techvishalboss"
        })

if __name__ == '__main__':
    app.run(debug=True)
