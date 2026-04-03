import requests
import json
import sys

API_URL = "https://digital.cholainsurance.com/api/v1/masterdata/vehicle_class_validation"

HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9,en-IN;q=0.8,hi;q=0.7',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Origin': 'https://digital.cholainsurance.com',
    'Pragma': 'no-cache',
    'Referer': 'https://digital.cholainsurance.com/cscportal/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/134.0.0.0',
}

def fetch_vehicle_info(vehicle_number: str):
    payload = {
        'vehicleNumber': vehicle_number,
        'journeyChannel': 'CSC',
        'partnerShortCode': '',
        'productName': 'Two Wheeler',
        'signzyState': 'UTTAR PRADESH STATE OFFICE',
        'signzySelPolicytype': 'Liability',
    }

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=30
    )

    response.raise_for_status()
    return response.json()

def main():
    print("🚗 Vehicle Info CLI Tool")
    print("Type 'exit' to quit\n")

    while True:
        vehicle_number = input("Enter Vehicle Number: ").strip().upper()

        if vehicle_number.lower() == "exit":
            print("👋 Exiting...")
            sys.exit(0)

        if not vehicle_number:
            print("❌ Empty input\n")
            continue

        print("\n🔍 Fetching data...\n")

        try:
            data = fetch_vehicle_info(vehicle_number)

            # 🔥 FULL RAW JSON OUTPUT
            print(json.dumps(data, indent=4, ensure_ascii=False))

        except requests.exceptions.HTTPError as e:
            print(f"❌ HTTP Error: {e}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Network Error: {e}")

        except Exception as e:
            print(f"❌ Error: {e}")

        print("\n" + "-" * 60 + "\n")

if __name__ == "__main__":
    main()
