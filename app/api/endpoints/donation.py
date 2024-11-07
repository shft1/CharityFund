from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models import User
from app.schemas import DonationCreate, DonationDB, DonationDBSuperuser
from app.services.investment import donation_invest
from app.services.managers import charity_project_manager, donation_manager

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDBSuperuser],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    donations = await donation_manager.get_multi(
        session=session
    )
    return donations


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    new_donation = await donation_manager.create(
        donation, session, user
    )
    projects = await charity_project_manager.get_multi(
        session=session
    )
    investing_donation = await donation_invest(
        new_donation, projects, session
    )
    return investing_donation


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    user_donations = await donation_manager.get_user_donations(
        user=user,
        session=session
    )
    return user_donations
