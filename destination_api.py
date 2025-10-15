import requests
import os
from dotenv import load_dotenv

load_dotenv()


class DestinationAPI:
    def __init__(self, base_url=None):
        self.base_url = base_url or os.getenv(
            "API_BASE_URL", "http://127.0.0.1:8000/api"
        )
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def store(self, destination_data):
        """
        บันทึกข้อมูลสถานที่ท่องเที่ยวใหม่

        Args:
            destination_data (dict): ข้อมูลสถานที่ท่องเที่ยว

        Returns:
            dict: ผลลัพธ์การบันทึก {'success': bool, 'message': str, 'data': dict}
        """
        url = f"{self.base_url}/destinations"

        try:
            response = requests.post(url, json=destination_data, headers=self.headers)

            if response.status_code == 201:
                return {
                    "success": True,
                    "message": "Destination created successfully.",
                    "data": response.json(),
                }
            elif response.status_code == 422:
                return {
                    "success": False,
                    "message": "Validation error",
                    "errors": response.json().get("errors", {}),
                }
            else:
                return {
                    "success": False,
                    "message": response.json().get("message", "Unknown error"),
                    "status_code": response.status_code,
                }
        except requests.exceptions.RequestException as e:
            return {"success": False, "message": f"Request failed: {str(e)}"}


# ตัวอย่างการใช้งาน
if __name__ == "__main__":
    destination_data = {
        "province_id": 1,
        "name": "วัดพระแก้ว",
        "name_en": "Temple of the Emerald Buddha",
        "short_description": "วัดพระแก้วเป็นวัดที่สำคัญที่สุดในประเทศไทย",
        "description": 'วัดพระศรีรัตนศาสดาราม หรือที่รู้จักในนาม "วัดพระแก้ว" เป็นวัดที่ตั้งอยู่ในพระบรมมหาราชวัง',
        "latitude": 13.7510,
        "longitude": 100.4927,
        "address": "ถนนหน้าพระลาน แขวงพระบรมมหาราชวัง",
        "district": "พระนคร",
        "subdistrict": "พระบรมมหาราชวัง",
        "postal_code": "10200",
        "phone": "02-224-3290",
        "website": "https://www.royalgrandpalace.th",
        "price_from": 500.00,
        "price_to": 500.00,
        "cover_image": "https://cover_image.jpg",
        "gallery_images": ["https://gallery_image1.png", "https://gallery_image2.jpg"],
        "is_active": True,
        "is_featured": True,
    }

    api = DestinationAPI()
    result = api.store(destination_data)

    if result["success"]:
        print(result["message"])
        print("Data:", result.get("data"))
    else:
        print(f"Error: {result['message']}")
        if "errors" in result:
            print("Validation errors:", result["errors"])
