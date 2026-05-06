import allure
import pytest
from fastapi.testclient import TestClient
from main import app

@allure.feature("API Tests")
class TestAPI:
    
    @pytest.fixture(autouse=True)
    def setup(self, client, clean_db):
        """Инициализация тестового клиента"""
        self.client = client
        self.base_url = "http://testserver"
    
    @allure.title("Проверка корневого эндпоинта")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.story("Health Check")
    def test_root_endpoint(self):
        """Проверка доступности API"""
        with allure.step("Отправка GET запроса на /"):
            response = self.client.get("/")
            allure.attach(
                body=f"Response: {response.json()}",
                name="Root Response",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверка содержимого ответа"):
            assert response.json() == {"message": "Welcome to Workshop API"}
    
    @allure.title("Получение списка всех items")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Items Management")
    def test_get_items_empty(self):
        """Проверка получения пустого списка items"""
        with allure.step("Отправка GET запроса на /items"):
            response = self.client.get("/items")
            allure.attach(
                body=f"Status: {response.status_code}, Response: {response.json()}",
                name="Get Items Response",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверка что список пуст"):
            assert response.json() == []
    
    @allure.title("Создание нового item")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Items Management")
    def test_create_item(self):
        """Проверка создания нового item"""
        item_data = {
            "name": "Test Item",
            "description": "Test Description",
            "price": 99.99
        }
        
        with allure.step("Подготовка данных для создания item"):
            allure.attach(
                body=str(item_data),
                name="Request Body",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Отправка POST запроса на /items"):
            response = self.client.post("/items", json=item_data)
            allure.attach(
                body=f"Status: {response.status_code}, Response: {response.json()}",
                name="Create Item Response",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 201
        
        with allure.step("Проверка данных созданного item"):
            created_item = response.json()
            assert created_item["name"] == item_data["name"]
            assert created_item["description"] == item_data["description"]
            assert created_item["price"] == item_data["price"]
            assert "id" in created_item
    
    @allure.title("Получение item по ID")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Items Management")
    def test_get_item_by_id(self):
        """Проверка получения item по ID"""
        # Сначала создаем item
        item_data = {"name": "Item 1", "description": "Desc 1", "price": 50.0}
        create_response = self.client.post("/items", json=item_data)
        item_id = create_response.json()["id"]
        
        with allure.step(f"Отправка GET запроса на /items/{item_id}"):
            response = self.client.get(f"/items/{item_id}")
            allure.attach(
                body=f"Status: {response.status_code}, Response: {response.json()}",
                name="Get Item By ID Response",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверка данных item"):
            item = response.json()
            assert item["id"] == item_id
            assert item["name"] == item_data["name"]
    
    @allure.title("Получение несуществующего item")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Items Management")
    def test_get_nonexistent_item(self):
        """Проверка получения несуществующего item"""
        with allure.step("Отправка GET запроса на /items/9999"):
            response = self.client.get("/items/9999")
            allure.attach(
                body=f"Status: {response.status_code}, Response: {response.json()}",
                name="Get Nonexistent Item Response",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Проверка статуса 404"):
            assert response.status_code == 404
        
        with allure.step("Проверка сообщения об ошибке"):
            assert response.json()["detail"] == "Item not found"
    
    @allure.title("Обновление item")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Items Management")
    def test_update_item(self):
        """Проверка обновления item"""
        # Создаем item
        item_data = {"name": "Original", "description": "Original Desc", "price": 100.0}
        create_response = self.client.post("/items", json=item_data)
        item_id = create_response.json()["id"]
        
        # Данные для обновления
        updated_data = {
            "name": "Updated",
            "description": "Updated Desc",
            "price": 199.99
        }
        
        with allure.step(f"Отправка PUT запроса на /items/{item_id}"):
            response = self.client.put(f"/items/{item_id}", json=updated_data)
            allure.attach(
                body=f"Status: {response.status_code}, Response: {response.json()}",
                name="Update Item Response",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверка обновленных данных"):
            updated_item = response.json()
            assert updated_item["name"] == updated_data["name"]
            assert updated_item["description"] == updated_data["description"]
            assert updated_item["price"] == updated_data["price"]
    
    @allure.title("Удаление item")
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Items Management")
    def test_delete_item(self):
        """Проверка удаления item"""
        # Создаем item
        item_data = {"name": "To Delete", "description": "Will be deleted", "price": 10.0}
        create_response = self.client.post("/items", json=item_data)
        item_id = create_response.json()["id"]
        
        with allure.step(f"Отправка DELETE запроса на /items/{item_id}"):
            response = self.client.delete(f"/items/{item_id}")
            allure.attach(
                body=f"Status: {response.status_code}, Response: {response.json()}",
                name="Delete Item Response",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверка что item удален"):
            get_response = self.client.get(f"/items/{item_id}")
            assert get_response.status_code == 404
    
    @allure.title("Создание пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Users Management")
    def test_create_user(self):
        """Проверка создания нового пользователя"""
        user_data = {
            "username": "testuser",
            "email": "test@example.com"
        }
        
        with allure.step("Подготовка данных пользователя"):
            allure.attach(
                body=str(user_data),
                name="User Request Body",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Отправка POST запроса на /users"):
            response = self.client.post("/users", json=user_data)
            allure.attach(
                body=f"Status: {response.status_code}, Response: {response.json()}",
                name="Create User Response",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 201
        
        with allure.step("Проверка данных созданного пользователя"):
            created_user = response.json()
            assert created_user["username"] == user_data["username"]
            assert created_user["email"] == user_data["email"]
            assert "id" in created_user
    
    @allure.title("Получение списка всех пользователей")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Users Management")
    def test_get_users(self):
        """Проверка получения списка всех пользователей"""
        # Создаем несколько пользователей
        self.client.post("/users", json={"username": "user1", "email": "user1@test.com"})
        self.client.post("/users", json={"username": "user2", "email": "user2@test.com"})
        
        with allure.step("Отправка GET запроса на /users"):
            response = self.client.get("/users")
            allure.attach(
                body=f"Status: {response.status_code}, Response: {response.json()}",
                name="Get Users Response",
                attachment_type=allure.attachment_type.JSON
            )
        
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200
        
        with allure.step("Проверка количества пользователей"):
            users = response.json()
            assert len(users) == 2