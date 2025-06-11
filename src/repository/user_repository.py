import json
from typing import Dict, Optional
from src.model.user import User

class UserRepository:
    def __init__(self):
        self.users_file = "users.json"
        self.load_users()

    def load_users(self):
        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.users = {}
                for username, user_data in data.items():
                    user = User(
                        username=username,
                        password=user_data.get('password', ''),
                        role=user_data.get('role', 'user'),
                        assigned_events=user_data.get('assigned_events', [])
                    )
                    self.users[username] = user
        except FileNotFoundError:
            self.users = {}
            self.save_users()

    def save_users(self):
        data = {
            username: {
                'password': user.password,
                'role': user.role,
                'assigned_events': user.assigned_events
            }
            for username, user in self.users.items()
        }
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_user(self, username: str) -> Optional[User]:
        return self.users.get(username)

    def get_all_users(self) -> Dict[str, User]:
        return self.users

    def create_user(self, username: str, password: str, role: str = "user") -> User:
        user = User(
            username=username,
            password=password,
            role=role,
            assigned_events=[]
        )
        self.users[username] = user
        self.save_users()
        return user

    def update_user(self, user: User) -> User:
        self.users[user.username] = user
        self.save_users()
        return user

    def delete_user(self, username: str) -> bool:
        if username in self.users:
            del self.users[username]
            self.save_users()
            return True
        return False

    def user_exists(self, username: str) -> bool:
        return username in self.users 