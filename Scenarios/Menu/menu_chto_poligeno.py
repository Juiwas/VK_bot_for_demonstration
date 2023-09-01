"""
Сценарий для меры Универсальное пособие. Не зависит от темы. 

Меню и сам сценарий имеет такую иерархию:
├── Уже оформил
│ ├── Оформил, но получил от вас тоже
│ └── Иной вопрос
│
├── Подаю или отказ
│ ├── Как оформить? ── Ответ
│ ├── Почему мне отказали? ── Ответ
│ ├── Если офрмить, то нам отменят? ── Ответ
│ ├── Мне стоит переходить? ── Ответ
│ ├── Подавал, но передумал ── Ответ
│ └── Назад
└── Не переходил
  ├── Мне придет как обычно? ── Ответ
  ├── Вопрос не про единое пособие ── Ответ
  └── Назад

"""

from vk_api.keyboard import VkKeyboard, VkKeyboardColor

#keyboard_1.add_callback_button( label='Уже оформил', color=VkKeyboardColor.SECONDARY, payload={"type": "show_snackbar", "text": "unified_manual_PFR_1"})

# Настройки для обоих клавиатур
settings = dict(one_time=True, inline=False)

keyboard = VkKeyboard.get_empty_keyboard()


# №1. Клавиатура с 3 кнопками: "показать всплывающее сообщение", "открыть URL" и изменить меню (свой собственный тип)
keyboard_1 = VkKeyboard(**settings)
keyboard_1.add_button( label='Да', color=VkKeyboardColor.SECONDARY, payload={"type": "show_snackbar", "text": "unified_manual_PFR_1"})
keyboard_1.add_line()
keyboard_1.add_button(label='Нет', color=VkKeyboardColor.SECONDARY, payload={"type": "unified_manual_1_3"})

# №2. Клавиатура с одной красной callback-кнопкой. Нажатие изменяет меню на предыдущее.
keyboard_2 = VkKeyboard(**settings)
keyboard_2.add_button('Ниже прожиточного минимума', color=VkKeyboardColor.SECONDARY, payload={"type": "unified_manual_PFR"})
keyboard_2.add_line()
keyboard_2.add_button('Выше прожиточного минимума', color=VkKeyboardColor.SECONDARY, payload={"type": "unified_manual_PFR"})

keyboard_4 = VkKeyboard(**settings)
keyboard_4.add_button('Федеральная', color=VkKeyboardColor.SECONDARY, payload={"type": "unified_manual_3_1"})
keyboard_4.add_line()
keyboard_4.add_button('Региональная', color=VkKeyboardColor.SECONDARY, payload={"type": "unified_manual_3_2"})


keyboard_5 = VkKeyboard(**settings)
keyboard_5.add_button('Меньше 3', color=VkKeyboardColor.SECONDARY, payload={"type": "unified_manual_3_1"})
keyboard_5.add_line()
keyboard_5.add_button('3 и более', color=VkKeyboardColor.SECONDARY, payload={"type": "unified_manual_3_2"})


keyboard_6 = VkKeyboard(**settings)
keyboard_6.add_button( label='Пройти опрос заново', color=VkKeyboardColor.SECONDARY, payload={"type": "show_snackbar", "text": "unified_manual_PFR_1"})



"""
(x, y)
x - уровень меню
y - ветка в меню. Если нет, значит на этом уровне не зависит
"""
chto_poligeno_menu = {(0): keyboard,
					   (1): keyboard_1,
					   (2): keyboard_2,
					   (3): keyboard_1,
					   (4): keyboard_4,
					   (5): keyboard_1,
					   (6): keyboard_1,
					   (7): keyboard_5,
					   (8): keyboard_1,
					   (9): keyboard_1,
					   (10): keyboard_1
					   }

