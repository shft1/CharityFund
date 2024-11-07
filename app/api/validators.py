from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject
from app.services.managers import charity_project_manager


async def check_project_exists(
        project_id: int,
        session: AsyncSession
):
    project = await charity_project_manager.get(
        obj_id=project_id,
        session=session
    )
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Такого проекта не существует!'
        )
    return project


async def check_project_name_duplicate(
        name: str,
        session: AsyncSession
):
    project = await charity_project_manager.get_project_by_name(
        name=name,
        session=session
    )
    if project is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_full_amount(
        invested_amount: int,
        new_full_amount: int
):
    if new_full_amount < invested_amount:
        raise HTTPException(
            status_code=400,
            detail=('Нелья установить значение '
                    'full_amount меньше уже вложенной суммы.')
        )


async def check_project_status_update(
        project: CharityProject
):
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_project_status_delete(
        project: CharityProject
):
    if project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя удалять!'
        )


async def check_project_investing(
        project: CharityProject
):
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
