from pwdlib import PasswordHash

from app.repositories.user_repository import user_repository
password_hash = PasswordHash.recommended()

class AuthService:

    async def register_user(self, user_data):
        # Check if email already exists
        existing_user = await user_repository.find_by_email(user_data.email)

        if existing_user:
            raise ValueError("User with this email already exists")

        # Hash password before storing it
        hashed_password = password_hash.hash(user_data.password)

        # Prepare data for MongoDB
        user_document = {
            "name": user_data.name,
            "email": user_data.email,
            "password": hashed_password,
            "role": user_data.role
        }

        # Save user
        user_id = await user_repository.create(user_document)

        return {
            "id": str(user_id),
            "name": user_data.name,
            "email": user_data.email,
            "role": user_data.role
        }

auth_service = AuthService()