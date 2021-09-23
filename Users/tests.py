from rest_framework.test import APITestCase

from .models import Users


class UsersTestCases(APITestCase):
    def setUp(self):
        data = {
            "first_name": "Juancho",
            "last_name": "Molina",
            "date_birth": "1989-11-12",
            "address": "calle 45",
            "password": "unacontraseña",
            "mobile_phone": "3157634321",
            "email": "Juancho@gmail.com"
        }
        response = self.client.post("/api/v1/users/", data )

    def test_add_user(self):
        data = {
            "first_name": "jose",
            "last_name": "antonio",
            "date_birth": "1987-09-01",
            "address": "calle 15",
            "password": "lalluviacae",
            "mobile_phone": "3024576844",
            "email": "joseantonio@gmail.com"
        }
        response = self.client.post("/api/v1/users/", data)
        result = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(result['first_name'], "jose")
        self.assertEqual(result['email'], "joseantonio@gmail.com")
    
    def test_get_users(self):
        response = self.client.get("/api/v1/users/")
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(result[0]['first_name'], "Juancho")
        self.assertIn('email', result[0])
    
    def test_update_user(self):
        data = {
            "email": 'JuanchoMolina@gmail.com'
        }
        response = self.client.patch("/api/v1/users/1/", data)    
        result = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(result['email'], 'Juancho@gmail.com')
        self.assertEqual(result['email'], 'JuanchoMolina@gmail.com')

    def test_delete_user(self):
        response_delete = self.client.delete("/api/v1/users/1/")
        response_get = self.client.get("/api/v1/users/1/")  

        self.assertEqual(response_delete.status_code, 200)
        self.assertEqual(response_get.status_code, 404)

