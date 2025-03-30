from locust import HttpUser, task, between
import random
import os

class ApiUser(HttpUser):
    wait_time = between(1, 3)  # Интервал между запросами
    
    # Для эндпоинтов с авторизацией
    def on_start(self):
        response = self.client.post("/api/auth/login/", {
            "username": "testuser",
            "password": "testpass123"
        })
        self.token = response.json().get("token")
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    @task(3)  # Частота выполнения (вес)
    def get_products(self):
        self.client.get("/api/products/", headers=self.headers)
    
    @task(2)
    def create_product(self):
        self.client.post("/api/products/", 
            json={"name": "Test", "price": 100},
            headers=self.headers)
    
    @task(1)
    def upload_file(self):
        files = {
            "file": ("test.txt", b"Test file content", "text/plain")
        }
        self.client.post(
            "/api/upload/", 
            files=files,
            headers=self.headers,
            data={"description": "Test file"}
        )
    
    @task(1)
    def download_file(self):
        with self.client.get("/api/files/1/download/", 
                          headers=self.headers,
                          stream=True,
                          catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure("File download failed")