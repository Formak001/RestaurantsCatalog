from fastapi import APIRouter

# Создаем изолированный роутер специально для ресторанов
router = APIRouter()

# Обратите внимание: путь здесь просто "/", так как префиксы мы добавим позже
@router.get("/get_restaurants")
async def get_restaurants():
    # Здесь будет логика фильтрации и обращения к БД
    return [{"id": 1, "name": "La Trattoria"}]