class User:
    user_name: str = 'ubuntu'

    def change_user_name(self, new_user_name: str) -> None:
        self.user_name = new_user_name

    def get_user_name(self) -> str:
        return self.user_name
