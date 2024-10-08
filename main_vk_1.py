import vk_api, json 
from vk_api.longpoll import VkLongPoll, VkEventType 
from vk_api.keyboard import VkKeyboard, VkKeyboardColor

main_token='vk1.a.07uxeaQ3ABpdvj-LhJ1nGAMS9K3Ye8flrrz2ZGBNV83EhhkyOGknJYgczRyGCHpX0plDH0ZZdMCLEr_M0-gO1HgtZFEO0Fga0fr57ZBNlZFkMiFOWmJlqa7BXIxQmnaZcfuODa03RnCDIJ4x4kN5z0tayohIDY0S8ui4XnddFpnXIV7gJKi4YDZVWFCdpz4wfiO8a6fFCbhXRwfTbX-CyQ' 

vk_session = vk_api.VkApi(token = main_token) 
Longpoll = VkLongPoll(vk_session) 

def get_keyboard(buts): 
    global get_but 
    nb = [] 
    color = '' 

    for i in range(len(buts)): 
        nb.append([]) 
        for k in range(len(buts[i])): 
            nb[i].append(None) 

    for i in range(len(buts)): 
        for k in range(len(buts[i])): 
            text = buts[i][k][0] 
            print(str(text)) 
            if buts[i][k][1] == 'p': 
                color = 'positive' 
            elif buts[i][k][1] == 'n': 
                color = 'negative' 
            nb[i][k] = {
                "action": { 
                    "type": "text", 
                    "label": str(text) 
                    },
                "color": f"{color}" 
            }

    first_keyboard = { 
        'buttons': nb 
        }
    first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8') 
    first_keyboard = str(first_keyboard.decode('utf-8')) 
    return first_keyboard 

def sender(id, text): 
    vk_session.method('messages.send', {'user_id' :id, 'message' : text, 'random_id' : 0, 'keyboard' : keyboard1}) 

names_meanings = {
    "руслан":"Происхождение имени Руслан корнями уходит в героический иранский эпос о Рустаме, сыне Залазара (поэма «Шахнамэ» персидского поэта Фирдоуси). Тюркские народы воспели его уже как Арслана Зальзара, а затем в XVII веке у славянских народов он уже фигурирует как богатырь Еруслан Залазарович, или Лазаревич.",
    "антон": "Имя Антон имеет латинские корни, происходит от римского родового имени Antonius (Антониус, Антоний). Это очень древнее римское родовое имя, поэтому точное значение не известно.",
    "никита": "Имя Никита в переводе с греческого языка означает «победитель». В Западной Европе можно услышать и женский вариант этого имени, он идентичен мужскому звучанию – Никита. Женское имя Никита (с ударением на последний слог) появилось после известного фильма Люка Бессона «Никита» («Nikita», «La Femme Nikita»), где главная героиня взяла себе этот псевдоним.",
    "александра": "Имя Александра в переводе с греческого означает «мужественная», «защитница». Парное мужское имя – Александр. В русском, украинском и белорусском языках это имя имеет различные формы: Лександра, Ляксандра, Олекса, Алекса, Алеся, Олеся, Леся."
}

keyboard1 = get_keyboard( [
[
('Руслан', 'p'), ('Антон', 'p')],
[
('Никита', 'p'), ('Александра', 'p')]
]
)

for event in Longpoll.listen(): 
    if event.type == VkEventType.MESSAGE_NEW: 
        if event.to_me: 
            msg = event.text.lower() 
            id = event.user_id 
            if msg == 'привет': 
                sender(id, 'Привет, сейчас я расскажу тебе, кто ты по масти') 
            if msg in names_meanings:
                sender(id, names_meanings[msg])
            # if msg == 'овен': sender(id,  '''
            #                         Отличный день для общения.
            #                         Можно обсуждать непростые темы, в том числе такие, из-за которых прежде возникало немало разногласий. Вы найдете нужные слова, быстро договоритесь и с близкими людьми, и с новыми знакомыми. День подойдет для того, чтобы восстановить старые связи, помириться с теми, с кем вы были в ссоре.
            #                         ''')
            # elif msg == 'телец': sender(id,  '''
            #                             День будет беспокойным, но интересным.
            #                             Появится шанс посетить места, о которых вы много слышали, побывать на необычных мероприятиях, познакомиться с людьми, чьи опыт и знания не раз будут вам полезны. Хорошо сложатся поездки, особенно если вы отправитесь в дорогу вместе с кем- то из близких.
            #                             ''')
            # elif msg == 'близнецы': sender(id,  '''
            #                                     Не горячитесь и не тревожьтесь по пустякам. В первой половине дня эмоциональный фон будет довольно напряженным, но поддаваться дурному настроению не стоит. Сосредоточьтесь на полезных делах, в которых успех зависит только от вас.
            #                                     Легко будет даваться учеба, вы быстро разберетесь в том, что прежде казалось сложным. 
            #                                 ''')