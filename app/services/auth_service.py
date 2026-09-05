from pwdlib import PasswordHash
from app.repositories.user_repository import user_repository
from app.core.security import create_access_token
from bson import ObjectId

from app.schemas import user

password_hash = PasswordHash.recommended()

class AuthService:

    async def register_user(self, user_data):
        # Check if email already exists
        existing_user = await user_repository.find_by_email(user_data.email)

        if existing_user:
            raise ValueError("User with this email already exists")

        # Hash password before storing it
        hashed_password = password_hash.hash(user_data.password)

        # Prepare user document
        user_document = {
            "name": user_data.name,
            "email": user_data.email,
            "password": hashed_password,
            "role": "CUSTOMER"
        }

        # Save user to MongoDB
        user_id = await user_repository.create(user_document)

        # Return user details without password
        return {
            "id": str(user_id),
            "name": user_data.name,
            "email": user_data.email,
            "role": "CUSTOMER"
        }

    async def login_user(self, user_data):
        # Find user by email
        user = await user_repository.find_by_email(user_data.email)

        if not user:
            raise ValueError("Invalid email or password")

        # Verify password
        password_valid = password_hash.verify(
            user_data.password,
            user["password"]
        )

        if not password_valid:
            raise ValueError("Invalid email or password")

        # Generate JWT access token
        access_token = create_access_token(
            user_id=str(user["_id"]),
            role=user["role"]
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    async def update_user_role(self, user_id: str, role: str):

        user = await user_repository.find_by_id(
        ObjectId(user_id)
        )

        if not user:
            raise ValueError("User not found")

        updated = await user_repository.update_role(
            ObjectId(user_id),
            role
        )

        if updated == 0:
            raise ValueError("Role was not updated")

        return {
            "message": "User role updated successfully",
            "user_id": user_id,
            "role": role
        }

auth_service = AuthService()