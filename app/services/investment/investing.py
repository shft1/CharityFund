from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation
from app.services.investment.close_object import close_object
from app.services.investment.save_investment import save_investment


async def donation_invest(
        donation: Donation,
        projects: list[CharityProject],
        session: AsyncSession
):
    for project in projects:
        if project.fully_invested:
            continue
        free_money = donation.full_amount - donation.invested_amount
        if project.invested_amount + free_money < project.full_amount:
            project.invested_amount += free_money
            close_object(donation, free_money)
            break
        elif project.invested_amount + free_money == project.full_amount:
            close_object(project, free_money)
            close_object(donation, free_money)
            break
        elif project.invested_amount + free_money > project.full_amount:
            investing_amount = project.full_amount - project.invested_amount
            close_object(project, investing_amount)
            donation.invested_amount += investing_amount
    return await save_investment(
        target=donation,
        sources=projects,
        session=session
    )


async def project_invest(
        project: CharityProject,
        donations: list[Donation],
        session: AsyncSession
):
    for donation in donations:
        if donation.fully_invested:
            continue
        free_money = donation.full_amount - donation.invested_amount
        if project.invested_amount + free_money < project.full_amount:
            project.invested_amount += free_money
            close_object(donation, free_money)
        elif project.invested_amount + free_money == project.full_amount:
            close_object(project, free_money)
            close_object(donation, free_money)
            break
        elif project.invested_amount + free_money > project.full_amount:
            investing_amount = project.full_amount - project.invested_amount
            close_object(project, free_money)
            donation.invested_amount += investing_amount
            break
    return await save_investment(
        target=project,
        sources=donations,
        session=session
    )
