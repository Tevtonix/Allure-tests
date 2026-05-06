import pytest
import allure
from api_layer.api_client import APIClient

@allure.feature("Comments API")
class TestComments:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.endpoint = "comments"
    
    @allure.title("Получение комментариев для поста")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story("Просмотр комментариев")
    def test_get_comments_by_post_id(self):
        """Проверка получения комментариев для конкретного поста"""
        with allure.step("Получаем комментарии для поста 1"):
            response = self.client.get(f"{self.endpoint}", params={"postId": 1})
        
        with allure.step("Проверяем статус код"):
            assert response.status_code == 200
        
        with allure.step("Проверяем комментарии"):
            comments = response.json()
            assert len(comments) > 0
            assert all(comment['postId'] == 1 for comment in comments)