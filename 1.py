import requests
import random
import time
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

key = b"LnXRHW7rDIJO12NK698wzSqQgiczQ4pS"

is_first_time_vehicle_bootup = True
vehicle_auth = None

def decrypt(ciphertext_b64,iv_b64):
    ciphertext = base64.b64decode(ciphertext_b64)
    iv = base64.b64decode(iv_b64)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

def generate_trn_id():
    timestamp = time.strftime("%d%m%y%H%M%S")
    random_number = random.randint(100000000, 999999999)
    return f"T{timestamp}{random_number}"

def generate_device_id():
    return ''.join(random.choices('0123456789abcdef', k=16))

def login_with_random_device():
    url = "https://rtovehiclesinformation.com/api/App/user/login/device"
    headers = {
        "x-api-key": "TYnv6rWz6aq2ZxaYwvXvhCxms1OOAiJB",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; sdk_gphone64_x86_64 Build/SE1A.211212.001.B1)",
        "Host": "rtovehiclesinformation.com",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br"
    }

    device_id = generate_device_id()
    payload = {
        "device_id": device_id
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        try:
            jsdata = json.loads(response.text)
            ciphertext_b64 = jsdata.get('encrypted')
            iv_b64 = jsdata.get('iv')
            decrypted = decrypt(ciphertext_b64,iv_b64)
            data = json.loads(decrypted)
            vehicle_auth = f"Bearer {data.get('token')}"
            is_first_time_vehicle_bootup = False
            return vehicle_auth
        except Exception:
            print("Response Text:", response.text)
            return None
    except requests.RequestException as e:
        print(f"[-] Request failed: {e}")
        return None

def get_details(vehicle_id):
    if is_first_time_vehicle_bootup:
        vehicle_auth = login_with_random_device()
    if not vehicle_auth:
        print('Landed into Fallback')
        vehicle_auth = login_with_random_device()
    url = "https://rtovehiclesinformation.com/api/App/vehicle/v1/information/RC"

    headers = {
        "Authorization":vehicle_auth,
        "x-api-key": "TYnv6rWz6aq2ZxaYwvXvhCxms1OOAiJB",
        "x-security-key": "A6829B176613A1917843EB3469D11",
        "Content-Type": "application/json",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; sdk_gphone64_x86_64 Build/SE1A.211212.001.B1)",
        "Host": "rtovehiclesinformation.com",
        "Connection": "keep-alive",
        "Accept-Encoding": "gzip, deflate, br"
    }

    payload = {
        "vehicleId": vehicle_id,
        "pay_type": "ads",
        "amount": 4,
        "credit": 1,
        "pay_TRN_ID": generate_trn_id(),
        "user_pay_credit": 0
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        jsdata = json.loads(response.text)
        ciphertext_b64 = jsdata.get('encrypted')
        iv_b64 = jsdata.get('iv')
        decrypted = decrypt(ciphertext_b64,iv_b64)
        data = json.loads(decrypted)
        return data
    except Exception:
        print("Response Text:", response.text)
        return None

reg_num = input("Enter Reg Num : ").strip()
datas = get_details(reg_num)
if not datas.get('status'):
    if datas.get('message') == 'No record found':
        print('Data Not Found')
    elif datas.get('message') == 'user in valid !':
        print('still in issue')
    elif datas.get('message') == 'Block user !':
        login_with_random_device()
        print('Blocked Need New Auth')
    else:
        print(datas)
else:
    data = datas.get("data")
    data = {k: v for k, v in data.items() if v is not None}
    print(f"""
    Name : {data.get("owner_name", "N/A")}
    F.Name : {data.get("father_name", "N/A")}
    Financer : {data.get("financer", "N/A")}
    Is Financed : {data.get("is_financed", "N/A")}
    Present Addr. : {data.get("present_address", "N/A")}
    Permanent Addr. : {data.get("permanent_address", "N/A")}
    Insurence Comp. : {data.get("insurance_company", "N/A")}
    Insurace Pol. : {data.get("insurance_policy", "N/A")}
    Insurence Exp. : {data.get("insurance_expiry", "N/A")}
    Class : {data.get("class", "N/A")}
    Category : {data.get("category", "N/A")}
    Reg. Date : {data.get("registration_date", "N/A")}
    Vehicle Age : {data.get("vehicle_age", "N/A")}
    PUCC Upto : {data.get("pucc_upto", "N/A")}
    PUCC Num. : {data.get("pucc_number", "N/A")}
    Chassis Num. : {data.get("chassis_number", "N/A")}
    Engine Num. : {data.get("engine_number", "N/A")}
    Fuel Type : {data.get("fuel_type", "N/A")}
    Brand Name : {data.get("brand_name", "N/A")}
    Model : {data.get("brand_model", "N/A")}
    Body Type : {data.get("body_type", "N/A")}
    Cylinders : {data.get("cylinders", "N/A")}
    Color : {data.get("color", "N/A")}
    Norms : {data.get("norms", "N/A")}
    Fit. Upto : {data.get("fit_up_to", "N/A")}
    RTO Name : {data.get("rto_name", "N/A")}
    NOC Det. : {data.get("noc_details", "N/A")}
    Seat Cap. : {data.get("seating_capacity", "N/A")}
    Owner Count : {data.get("owner_count", "N/A")}
    Tax Upto : {data.get("tax_upto", "N/A")}
    Tax Paid Upto : {data.get("tax_paid_upto", "N/A")}
    Permit Num. : {data.get("permit_number", "N/A")}
    Permit Iss. Dt. : {data.get("permit_issue_date", "N/A")}
    Permit Valid Frm. : {data.get("permit_valid_from", "N/A")}
    Permit Valid Upto : {data.get("permit_valid_upto", "N/A")}
    Permit Type : {data.get("permit_type", "N/A")}
    National Perm. Num. : {data.get("national_permit_number", "N/A")}
    National Perm. Upto. : {data.get("national_permit_upto", "N/A")}
    National Perm. iss. By : {data.get("national_permit_issued_by", "N/A")}
    RC Status : {data.get("rc_status", "N/A")}
    """)
  
