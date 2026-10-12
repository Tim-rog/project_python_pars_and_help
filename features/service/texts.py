TOTAL_STEPS = 5


def step(n: int, question: str) -> str:
    return f"➕ Новое объявление · Шаг {n}/{TOTAL_STEPS}\n\n{question}"


ACTION_CANCELED = "❌ Создание отменено"
ASK_CATEGORY = "Что отдаёшь?"
ASK_TITLE = "Напиши название."
CANCELLED = "Создание объявления отменено."