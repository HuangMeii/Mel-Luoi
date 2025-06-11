from typing import Dict, Optional
from src.model.user import User
from src.repository.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        user = self.user_repository.get_user(username)
        if user and user.password == password:
            return user
        return None

    def register_user(self, username: str, password: str, role: str = 'user') -> Optional[User]:
        if self.user_repository.user_exists(username):
            return None

        user = User(
            username=username,
            password=password,
            role=role,
            assigned_events=[]
        )
        self.user_repository.create_user(user.username, user.password, user.role)
        return user

    def get_user(self, username: str) -> Optional[User]:
        return self.user_repository.get_user(username)

    def get_all_users(self) -> Dict[str, User]:
        return self.user_repository.get_all_users()

    def update_user(self, username: str, password: str, role: str) -> Optional[User]:
        user = self.user_repository.get_user(username)
        if user:
            updated_user = User(
                username=username,
                password=password,
                role=role,
                assigned_events=user.assigned_events
            )
            self.user_repository.update_user(updated_user)
            return updated_user
        return None

    def delete_user(self, username: str) -> bool:
        if self.user_repository.user_exists(username):
            self.user_repository.delete_user(username)
            return True
        return False 