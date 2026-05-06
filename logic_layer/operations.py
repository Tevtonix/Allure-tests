import allure
from api_layer.api_client import APIClient

class PostOperations:
    def __init__(self, client: APIClient):
        self.client = client
        self.endpoint = "posts"
    
    @allure.step("Получение всех постов")
    def get_all_posts(self):
        return self.client.get(self.endpoint)
    
    @allure.step("Получение поста по ID: {post_id}")
    def get_post_by_id(self, post_id):
        return self.client.get(f"{self.endpoint}/{post_id}")
    
    @allure.step("Создание нового поста с заголовком: {title}")
    def create_post(self, title, body, user_id):
        data = {
            "title": title,
            "body": body,
            "userId": user_id
        }
        return self.client.post(self.endpoint, data)
    
    @allure.step("Обновление поста {post_id}")
    def update_post(self, post_id, title, body, user_id):
        data = {
            "id": post_id,
            "title": title,
            "body": body,
            "userId": user_id
        }
        return self.client.put(f"{self.endpoint}/{post_id}", data)
    
    @allure.step("Удаление поста {post_id}")
    def delete_post(self, post_id):
        return self.client.delete(f"{self.endpoint}/{post_id}")

class UserOperations:
    def __init__(self, client: APIClient):
        self.client = client
        self.endpoint = "users"
    
    @allure.step("Получение всех пользователей")
    def get_all_users(self):
        return self.client.get(self.endpoint)
    
    @allure.step("Получение пользователя по ID: {user_id}")
    def get_user_by_id(self, user_id):
        return self.client.get(f"{self.endpoint}/{user_id}")