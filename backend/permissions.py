from fastapi import Request, HTTPException


class BasePermission:
    @classmethod
    def has_permission(cls, request: Request, *args, **kwargs) -> bool:
        return True

    @classmethod
    def has_object_permission(cls, request: Request, obj) -> bool:
        return cls.has_permission(request)

    @classmethod
    def check_permissions(cls, request: Request, obj=None, *args, **kwargs):
        if not cls.has_permission(request, *args, **kwargs):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to access this page."
            )

        if obj is not None and not cls.has_object_permission(request, obj):
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to access this object."
            )


class IsAuthorized(BasePermission):
    @classmethod
    def has_permission(cls, request: Request, *args, **kwargs) -> bool:
        user = getattr(request.state, 'user', None)
        return bool(user)


class UserIsOwner(BasePermission):
    @classmethod
    def has_object_permission(cls, request: Request, obj) -> bool:
        user = getattr(request.state, "user", None)
        return user and obj.user_id == user.id


class UserIsPublisher(BasePermission):
    @classmethod
    def has_object_permission(cls, request: Request, obj) -> bool:
        user = getattr(request.state, "user", None)
        return user and obj.publisher_id == user.id
