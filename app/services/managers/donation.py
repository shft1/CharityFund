from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Donation, User

from .base import ManagerBase


class ManagerDonation(ManagerBase):
    @staticmethod
    async def get_donation_by_id(
        donation_id: int,
        session: AsyncSession
    ):
        donation = session.execute(
            select(Donation).where(Donation.id == donation_id)
        )
        return donation.scalars().first()

    @staticmethod
    async def get_user_donations(
        user: User,
        session: AsyncSession
    ):
        user_donations = await session.execute(
            select(Donation).where(Donation.user_id == user.id)
        )
        return user_donations.scalars().all()


donation_manager = ManagerDonation(Donation)
