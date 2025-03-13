from fastapi import APIRouter

router = APIRouter()


@router.get("/users", response_model=list[User])
async def get_users():
    try:
        return await format_users_response()
    except disnake.errors.HTTPException as exception:
        raise HTTPException(status_code=exception.status, detail=str(exception.text))
    except Exception as exception:
        raise HTTPException(status_code=500, detail=str(exception))

