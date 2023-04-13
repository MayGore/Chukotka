from tkinter import *
from collections import deque


class Window_class:

    def __init__(self, size, title, text, btn_list: list, field_for_input = None):
        self.wind = Toplevel(root)
        self.wind['bg'] = 'LightCyan'
        self.wind.title(title)
        self.wind.geometry(size)
        self.wind.grab_set()
        self.wind.resizable(False, False)
        self.wind

        self.quest = Label(self.wind, text=text, bg='LightCyan', fg='SteelBlue',
                                font=('Times New Roman', 18))
        self.quest.pack(padx=95, pady=30)

        if field_for_input:
            self.field = Entry(self.wind)
            self.field.pack(anchor=NW)
            self.field.focus()

        self.frame = Frame(self.wind, width=600, height=50, bg='LightCyan')
        self.frame.pack()

        for btn in btn_list:
            Button(self.frame, text=btn[0], bg='Plum', fg='purple', command=btn[1]).pack(side=LEFT, padx=10)

    def crash(self):
        self.wind.destroy()

def OUT():
    global canv
    if Q:
        line = Q.popleft()
        line_text = line['text']
        canv.configure(height=canv.winfo_height() + 20)
        if line_text[-1] == '#':
            # вызов окна с кнопками
            res = 0
            line.config(text=line_text[:-1])
            line.pack(anchor='nw')
            return res
        if line_text[-1] == '@':
            # вызов окна с вводом имени
            line.config(text=line_text[:-1])
            line.pack(anchor='nw')
            input_info("$? Отличное имя!")
        if line_text[-1] == '^':
            # вызов окна для выбора союзников в бой
            line.config(text=line_text[:-1])
            line.pack(anchor='nw')
            choose_your_fighter('~ выбраны для боя')
        line.pack(anchor='nw')
        canv.yview_scroll(6, 'units')


def tell(line):
    Q.append(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT, text=line))


buff_count = 0
shield_count = 0


def FIGHT_with_morphology(fighter1, fighter2):
    global buff_count
    global shield_count
    base = 0
    # choose who is going to take action
    # затычка:
    chosen = DAN
    if chosen.name == 'Даня':
        fighter1.atk += chosen.buff + chosen.morph
        fighter2.atk += chosen.buff + chosen.morph
        PLAYER.atk += chosen.buff + chosen.morph
        buff_count = 2
    elif chosen.name == 'Лиза':
        fighter1.hp += chosen.heal + chosen.morph
        fighter2.hp += chosen.heal + chosen.morph
        PLAYER.hp += chosen.heal + chosen.morph
    elif chosen.name == 'Федя':
        fighter1.defence += chosen.shield + chosen.morph
        fighter2.defence += chosen.shield + chosen.morph
        PLAYER.defence += chosen.shield + chosen.morph
    elif chosen.name == 'Моня':
        base = chosen.kill + chosen.morph
    damage_dealt = base + chosen.atk
    damage_taken = 4 - chosen.defence
    tell(f'{chosen.name} наносит Морфологии {damage_dealt} урона!!')
    MORPH.hp -= damage_dealt
    if MORPH.hp <= 0:
        return
    chosen.hp -= damage_taken
    if chosen.hp <= 0:
        tell(f'{chosen.name} больше не может выдержать. {chosen.name} уходит в академ.')
        chosen.is_alive = False
    FIGHT_with_morphology()


class Character:
    def __init__(self, name: str, color='green'):
        self.name = name
        self.color = color

    # for all
    def utter(self, line):
        lab = Label(f, fg=self.color, font=20, wraplength=500, justify=LEFT, text=self.name + ': ' + line)
        Q.append(lab)

    # добавила вывод строки
    def __str__(self):
        return self.name


class Monster(Character):
    def __init__(self, name: str, hp=0):
        self.name = name
        self.color = 'red'
        self.hp = hp


class Friends(Character):
    heal = 0
    shield = 0
    buff = 0
    kill = 0
    # battle
    friendship_with_player = 0
    atk = 2
    hp = 10
    defence = 0
    is_alive = True
    # knowledge
    morph = 0
    sem = 0
    synth = 0

    def rise_friendship(self):
        self.friendship_with_player += 1

    def take_academic_leave(self):
        self.is_alive = False


class Player(Friends):
    # inherited from all npc
    pass


# _________________________________________________BEGINNING>________________________________________________________
root = Tk()
root.geometry('800x600')
root.resizable(False, False)
root.title('имя позже придумаем')

frm1 = LabelFrame(root, width=800, height=500)

canv = Canvas(frm1, width=800, height=500)
canv.pack(fill="both", expand=True)

scrlbar = Scrollbar(canv, orient="vertical", command=canv.yview)
scrlbar.pack(side="right", fill="y")

canv.configure(yscrollcommand=scrlbar.set)

canv.bind('<Configure>', lambda e: canv.configure(scrollregion=canv.bbox('all')))

f = Frame(canv, width=800, height=500)
canv.create_window((0, 0), window=f, anchor='nw')

frm2 = Frame(root, width=800, height=70)
btn = Button(frm2, text='Продолжить', bg='PaleGreen', fg='ForestGreen', command=OUT)

Q = deque()


# ______________________________________________window for input_____________________________________________________

def input_info(text_out):  # это строка, которая реагирует на введённое имя
    def button():
        name = info.field.get()
        info.crash()
        # в принимаемой строке $ заменяется введённым именем
        Q.appendleft(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT,
                           text=f"{text_out.replace('$', name)}"))
        
    info = Window_class(size='350x150+500+100', title='Ввод', text='Имя...', field_for_input=True, btn_list=([('Принять!', button)]))


# ______________________________________________choose your fighter__________________________________________________
def choose_your_fighter(fighters):
    global fighter1, fighter2, button_chosen
    button_chosen = 0
    fighter1 = ''
    fighter2 = ''

    def lisa():
        global fighter1, fighter2, button_chosen
        if button_chosen == 0:
            fighter1 = LISA
            button_chosen = 1

        elif button_chosen == 1:
            fighter2 = LISA
            if fighter1 != fighter2:
                button_chosen = 0
                fight_choice.crash()
                Q.appendleft(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT,
                                   text=f"{fighters.replace('~', f'{fighter1} и {fighter2}')}"))
            else:
                fight_choice.quest['text'] = 'Пожалуйста, выберите\nдругого персонажа'

    def dan():
        global fighter1, fighter2, button_chosen
        if button_chosen == 0:
            fighter1 = DAN
            button_chosen = 1

        elif button_chosen == 1:
            fighter2 = DAN
            if fighter1 != fighter2:
                button_chosen = 0
                fight_choice.crash()
                Q.appendleft(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT,
                                   text=f"{fighters.replace('~', f'{fighter1} и {fighter2}')}"))
            else:
                fight_choice.quest['text'] = 'Пожалуйста, выберите\nдругого персонажа'

    def fedya():
        global fighter1, fighter2, button_chosen
        if button_chosen == 0:
            fighter1 = FEDYA
            button_chosen = 1

        elif button_chosen == 1:
            fighter2 = FEDYA
            if fighter1 != fighter2:
                button_chosen = 0
                fight_choice.crash()
                Q.appendleft(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT,
                                   text=f"{fighters.replace('~', f'{fighter1} и {fighter2}')}"))
            else:
                fight_choice.quest['text'] = 'Пожалуйста, выберите\nдругого персонажа'

    def monya():
        global fighter1, fighter2, button_chosen
        if button_chosen == 0:
            fighter1 = MONYA
            button_chosen = 1

        elif button_chosen == 1:
            fighter2 = MONYA
            if fighter1 != fighter2:
                button_chosen = 0
                fight_choice.crash()
                Q.appendleft(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT,
                                   text=f"{fighters.replace('~', f'{fighter1} и {fighter2}')}"))
            else:
                fight_choice.quest['text'] = 'Пожалуйста, выберите\nдругого персонажа'
                
    fight_choice = Window_class(size='500x190+500+100', title='Пора в бой!', text='Кого возьмешь в команду?', 
                                btn_list=([('Лиза', lisa), ('Федя', fedya), ('Даня', dan), ('Моня', monya)]))


# _________________________________________________<BEGINNING________________________________________________________

# MASHA = Character('Masha')
tell('story')
# for i in range(10):
#     tell('this is a story - jhyghwehb jkfjidhjbew nmdflgjhejwnmfd lkjihebwenmfsmdjkb hnemf ,ekjhfbnmkvjhfvb '
#          'nmnvkjhfjmr kmsjbvfrmkjs bhvffnmrks fjrmv#')
#     MASHA.utter('I am Masha. I like iuhgyhjbjnk flfbhnksvjih ufjenkvfbhenk nvjsfkmcnfd jre grejk gewrug erukg '
#                 'erkugerwuguiewrg er ugre gu egue')
#     tell('story@')
LISA = Friends('Лиза', 'green')
LISA.heal = 4
LISA.synth = 1
DAN = Friends('Даня', 'blue')
DAN.buff = 2
DAN.morph = 1
MONYA = Friends('Моня', 'red')
MONYA.kill = 2
MONYA.synth = 1
FEDYA = Friends('Федя', 'orange')
FEDYA.shield = 2
FEDYA.sem = 1
PLAYER = Player('=', 'black')
# сделала у Инны цвет поярче, чтобы лучше видно было
IB = Character('Инна Бисер', 'HotPink')
YL = Character('Юрий Ландыш', 'purple')
tell('это история 4 ребят и вас')
tell('это Лиза Андреева')
LISA.utter('здравствуйте')
tell('это Даня Михаэль')
DAN.utter('приввввввввввеееееееееееет роакупущ шкгсаьку чгшсарсь шучфугрч ашщйгкя ьашыкпаьшйк нщчпаькйайц шщкчп '
          'аькушнп аьшапйуц шгчпцгшап ьцгшщачпькйшща пчтуцншщапчкща')
tell('это Федя Сосся')
FEDYA.utter("Я Фердинанд")
tell('это Моня Мохская')
MONYA.utter('йоу')
tell("познакомимсся также с Инной Бисер и Юрием Ландышем")
IB.utter('здравствуйте детишки')
YL.utter('здравствуйте детишки')
tell('теперь введите ваше имя:@')
tell('Пора в бой!^')

MORPH = Monster('Морфология', 100)
# ___________________________________________________END>_____________________________________________________________
frm1.pack(fill="both", expand=True)
frm2.pack(anchor='s')
btn.pack(anchor='ne', padx=10, pady=10)
root.mainloop()
# ___________________________________________________<END_____________________________________________________________
