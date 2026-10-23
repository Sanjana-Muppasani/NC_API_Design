from fastapi import APIRouter, HTTPException
from db.connection import get_db_connection
from src.models.auth_models import LoginRequest, RegisterRequest, RegisterRequestResponse
from src.auth_helper import create_hashed_passwords

router = APIRouter()

@router.post(
    "/api/auth/register",
    response_model=RegisterRequestResponse, 
    status_code=201
)
def user_register(register_request: RegisterRequest) -> dict:
    conn = get_db_connection()

    try:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id
            FROM users
            WHERE email = %s
            """,
            (register_request.email,)
        )

        if cur.fetchone() is not None:
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

        hashed_password = create_hashed_passwords(
            register_request.password
        )

        cur.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
            RETURNING id, name, email, created_at
            """,
            (
                register_request.name,
                register_request.email,
                hashed_password
            )
        )

        user_details = cur.fetchone()
        conn.commit()

        return {
                "user": {
                    "id": user_details[0],
                    "name": user_details[1],
                    "email": user_details[2],
                    "created_at": user_details[3]
                }
            }

    finally:
        conn.close()