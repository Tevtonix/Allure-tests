import requests
import allure

class APIClient:
    def __init__(self, base_url="https://jsonplaceholder.typicode.com"):
        self.base_url = base_url
        self.session = requests.Session()
    
    @allure.step("Выполнение GET запроса к {endpoint}")
    def get(self, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        with allure.step(f"Отправка GET запроса: {url}"):
            response = self.session.get(url, **kwargs)
            allure.attach(
                body=f"Request URL: {url}\nResponse: {response.text}",
                name=f"GET {endpoint}",
                attachment_type=allure.attachment_type.JSON
            )
            return response
    
    @allure.step("Выполнение POST запроса к {endpoint}")
    def post(self, endpoint, data, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        with allure.step(f"Отправка POST запроса: {url}"):
            response = self.session.post(url, json=data, **kwargs)
            allure.attach(
                body=f"Request URL: {url}\nRequest Body: {data}\nResponse: {response.text}",
                name=f"POST {endpoint}",
                attachment_type=allure.attachment_type.JSON
            )
            return response
    
    @allure.step("Выполнение PUT запроса к {endpoint}")
    def put(self, endpoint, data, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        with allure.step(f"Отправка PUT запроса: {url}"):
            response = self.session.put(url, json=data, **kwargs)
            allure.attach(
                body=f"Request URL: {url}\nRequest Body: {data}\nResponse: {response.text}",
                name=f"PUT {endpoint}",
                attachment_type=allure.attachment_type.JSON
            )
            return response
    
    @allure.step("Выполнение DELETE запроса к {endpoint}")
    def delete(self, endpoint, **kwargs):
        url = f"{self.base_url}/{endpoint}"
        with allure.step(f"Отправка DELETE запроса: {url}"):
            response = self.session.delete(url, **kwargs)
            allure.attach(
                body=f"Request URL: {url}\nResponse Status: {response.status_code}",
                name=f"DELETE {endpoint}",
                attachment_type=allure.attachment_type.TEXT
            )
            return response