from enum import Enum
from typing import Dict, Optional

from fastapi import Depends, HTTPException, status, Security
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from httpx import AsyncClient


class UsersEndpoints(Enum):
    ME = "users/me"


class ApplicationsEndpoints(Enum):
    TOKEN_VALIDATE = "applications/token/validate"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name="application_token")
unauthorized_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)

invalid_application_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid Application Token",
)
PAGINATION = Dict[str, Optional[int]]
max_limit = 25


class CurrentUserBase:
    def __init__(self, service_url: str):
        self.service_url = service_url

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        async with AsyncClient() as client:
            url = self.service_url + UsersEndpoints.ME.value
            headers = {
                "Authorization": f"Bearer {token}"
            }
            response = await client.get(url, headers=headers)
            if response.status_code == 401:
                raise unauthorized_exception
            user = response.json()
        return user


class CurrentUser(CurrentUserBase):
    async def __call__(self, token: str = Depends(oauth2_scheme)):
        return await self.get_current_user(token)


class CurrentSuperUser(CurrentUserBase):
    async def __call__(self, token: str = Depends(oauth2_scheme)):
        user = await self.get_current_user(token)
        if not user['is_superuser']:
            raise unauthorized_exception
        return user


class ApplicationToken:
    def __init__(self, applications_service_url: str):
        self.applications_service_url = applications_service_url

    async def __call__(self, application_token=Security(api_key_header)):
        async with AsyncClient() as client:
            url = self.applications_service_url + ApplicationsEndpoints.TOKEN_VALIDATE.value
            headers = {
                "application_token": application_token
            }
            response = await client.get(url, headers=headers)
            if response.status_code != 200:
                raise invalid_application_token
            application = response.json()
        return application


def create_query_validation_exception(field: str, msg: str) -> HTTPException:
    return HTTPException(
        422,
        detail={
            "detail": [
                {"loc": ["query", field], "msg": msg, "type": "type_error.integer"}
            ]
        },
    )


def pagination(skip: int = 0, limit: Optional[int] = max_limit) -> PAGINATION:
    if skip < 0:
        raise create_query_validation_exception(
            field="skip",
            msg="skip query parameter must be greater or equal to zero",
        )

    if limit is not None:
        if limit <= 0:
            raise create_query_validation_exception(
                field="limit", msg="limit query parameter must be greater then zero"
            )

        elif max_limit and max_limit < limit:
            raise create_query_validation_exception(
                field="limit",
                msg=f"limit query parameter must be less then {max_limit}",
            )

    return {"skip": skip, "limit": limit}
