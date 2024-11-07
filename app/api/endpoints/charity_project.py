from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_project_exists,
                                check_project_full_amount,
                                check_project_investing,
                                check_project_name_duplicate,
                                check_project_status_delete,
                                check_project_status_update)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.schemas import (CharityProjectCreate, CharityProjectDB,
                         CharityProjectUpdate)
from app.services.investment import project_invest
from app.services.managers import charity_project_manager, donation_manager

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session)
):
    charity_projects = await charity_project_manager.get_multi(session)
    return charity_projects


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_project_name_duplicate(
        name=charity_project.name,
        session=session
    )
    new_project = await charity_project_manager.create(
        obj=charity_project,
        session=session
    )
    donations = await donation_manager.get_multi(
        session=session
    )
    investing_project = await project_invest(
        project=new_project,
        donations=donations,
        session=session
    )
    return investing_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def update_charity_project(
    project_id: int,
    charity_project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exists(
        project_id=project_id,
        session=session
    )
    await check_project_status_update(project)

    if charity_project_in.name is not None:
        await check_project_name_duplicate(
            name=charity_project_in.name,
            session=session
        )
    if charity_project_in.full_amount is not None:
        await check_project_full_amount(
            invested_amount=project.invested_amount,
            new_full_amount=charity_project_in.full_amount
        )
    update_project = await charity_project_manager.update(
        obj_model=project,
        obj_in=charity_project_in,
        session=session
    )
    return update_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exists(
        project_id=project_id,
        session=session
    )
    await check_project_status_delete(project)
    await check_project_investing(project)
    delete_project = await charity_project_manager.delete(
        obj_model=project,
        session=session
    )
    return delete_project
