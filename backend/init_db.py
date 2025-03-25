from repositories.user_repository import UserRepository
from utils.db_utils import get_db_session
from schemas.user_schema import UserUpsert
from config import config


if __name__ == "__main__":
    session = next(get_db_session())
    user_data = UserUpsert(
        username=config.ADMIN_USERNAME,
        email=config.ADMIN_EMAIL,
        password=config.ADMIN_PASSWORD
    )

    admin_user = UserRepository.get_or_create_admin_user(session, user_data)

    if admin_user:
        print(f"Admin user created.\n"
              f"username: {admin_user.username}, email: {admin_user.email}")
