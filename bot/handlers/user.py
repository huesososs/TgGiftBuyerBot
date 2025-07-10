from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Transaction
from sqlalchemy import select

router = Router()

@router.message(Command("my_transactions"))
async def cmd_my_transactions(
    message: types.Message,
    session: AsyncSession
):
    # Получаем все транзакции пользователя
    result = await session.execute(
        select(Transaction)
        .where(Transaction.user_id == message.from_user.id)
        .order_by(Transaction.created_at.desc())
    )
    transactions = result.scalars().all()

    if not transactions:
        await message.answer("📭 У вас нет транзакций.")
        return

    # Формируем сообщение
    response = ["📊 Ваши транзакции:"]
    for tr in transactions:
        response.append(
            f"├ {tr.created_at.strftime('%d.%m.%Y %H:%M')}\n"
            f"├ ID: `{tr.telegram_payment_charge_id}`\n"
            f"├ Сумма: {tr.amount} звёзд\n"
            f"└ Статус: {tr.status}\n"
        )

    await message.answer("\n".join(response), parse_mode="Markdown")
