import pytest
import allure
from api_layer.api_client import APIClient
from logic_layer.operations import PostOperations, UserOperations

@allure.feature("Posts API")
class TestPosts:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.posts = PostOperations(self.client)
    
    @allure.title("Получение всех постов")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Просмотр постов")
    def test_get_all_posts(self):
        """Проверка получения всех постов"""
        with allure.step("Получаем список всех постов"):
            response = self.posts.get_all_posts()
        
        with allure.step("Проверяем статус код"):
            assert response.status_code == 200
        
        with allure.step("Проверяем, что посты возвращены"):
            posts = response.json()
            assert len(posts) > 0
            assert isinstance(posts, list)
    
    @allure.title("Получение поста по ID")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Просмотр постов")
    def test_get_post_by_id(self):
        """Проверка получения конкретного поста"""
        with allure.step("Получаем пост с ID 1"):
            response = self.posts.get_post_by_id(1)
        
        with allure.step("Проверяем статус код"):
            assert response.status_code == 200
        
        with allure.step("Проверяем данные поста"):
            post = response.json()
            assert post['id'] == 1
            assert 'title' in post
            assert 'body' in post
    
    @allure.title("Создание нового поста")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story("Управление поставами")
    def test_create_post(self):
        """Проверка создания нового поста"""
        with allure.step("Создаем новый пост"):
            response = self.posts.create_post(
                title="New Test Post",
                body="This is test body",
                user_id=1
            )
        
        with allure.step("Проверяем статус код"):
            assert response.status_code == 201
        
        with allure.step("Проверяем данные созданного поста"):
            post = response.json()
            assert post['title'] == "New Test Post"
            assert post['body'] == "This is test body"
            assert post['userId'] == 1
            assert 'id' in post
    
    @allure.title("Обновление поста")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Управление поставами")
    def test_update_post(self):
        """Проверка обновления существующего поста"""
        with allure.step("Обновляем пост с ID 1"):
            response = self.posts.update_post(
                post_id=1,
                title="Updated Title",
                body="Updated Body",
                user_id=1
            )
        
        with allure.step("Проверяем статус код"):
            assert response.status_code == 200
        
        with allure.step("Проверяем обновленные данные"):
            post = response.json()
            assert post['title'] == "Updated Title"
            assert post['body'] == "Updated Body"
    
    @allure.title("Удаление поста")
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Управление поставами")
    def test_delete_post(self):
        """Проверка удаления поста"""
        with allure.step("Удаляем пост с ID 1"):
            response = self.posts.delete_post(1)
        
        with allure.step("Проверяем статус код"):
            assert response.status_code == 200

@allure.feature("Users API")
class TestUsers:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.users = UserOperations(self.client)
    
    @allure.title("Получение всех пользователей")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Просмотр пользователей")
    def test_get_all_users(self):
        """Проверка получения всех пользователей"""
        with allure.step("Получаем список всех пользователей"):
            response = self.users.get_all_users()
        
        with allure.step("Проверяем статус код"):
            assert response.status_code == 200
        
        with allure.step("Проверяем, что пользователи возвращены"):
            users = response.json()
            assert len(users) > 0
    
    @allure.title("Получение пользователя по ID")
    @allure.severity(allure.severity_level.MINOR)
    @allure.story("Просмотр пользователей")
    def test_get_user_by_id(self):
        """Проверка получения конкретного пользователя"""
        with allure.step("Получаем пользователя с ID 1"):
            response = self.users.get_user_by_id(1)
        
        with allure.step("Проверяем статус код"):
            assert response.status_code == 200
        
        with allure.step("Проверяем данные пользователя"):
            user = response.json()
            assert user['id'] == 1
            assert 'name' in user
            assert 'email' in user