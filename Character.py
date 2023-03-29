from tkinter import *
from collections import deque


# кроме как через кучу глобальных переменных я пока не придумала, как сделать
fighter1 = None
fighter2 = None
button_chosen = 0

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
            res = 0
            line.config(text=line_text[:-1])
            line.pack(anchor='nw')
            return res
        line.pack(anchor='nw')
        canv.yview_scroll(6, 'units')


def tell(line):
    Q.append(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT, text=line))


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


class Friends(Character):
    heal = 0
    shield = 0
    buff = 0
    kill = 0
    # battle
    friendship_with_player = 0
    hp = 10
    defence = 0
    is_alive = True
    # knowledge
    morph = 0
    sem = 0
    synth = 0

    def use_skill(self):
        if self.heal != 0:
            pass
        elif self.shield != 0:
            pass
        elif self.buff != 0:
            pass
        elif self.kill != 0:
            pass

    def rise_friendship(self):
        self.friendship_with_player += 1

    def take_academic_leave(self):
        self.is_alive = False
        
    def chosen_for_fight1(self):
        global button_chosen
        global fighter1
        global fighter2

        if button_chosen == 0:
            fighter1 = self
            button_chosen = 1
            
        elif button_chosen == 1:
            fighter2 = self
            button_chosen = 0
            fight_choice.destroy()
            # принт пока просто для проверки, что работает
            print(fighter1, fighter2)


class Player(Friends):
    # inherited from all npc
    pass


def choose_your_fighter():
    global fight_choice
    fight_choice = Toplevel(root)
    fight_choice['bg'] = 'LightCyan'
    fight_choice.title('Пора в бой!')
    fight_choice.geometry('500x150+500+100')
    fight_choice.grab_set()
    fight_choice.resizable(False, False)

    question = Label(fight_choice, text='Кого возьмешь в команду?', bg='LightCyan', fg='SteelBlue', font=('Times New Roman', 18))
    question.pack(padx=95, pady=30)

    frame = Frame(fight_choice, width=600, height=50, bg='LightCyan')
    frame.pack()

    btn1 = Button(frame, text='Лиза', bg='Plum', fg='purple', command=LISA.chosen_for_fight1)
    btn1.pack(side=LEFT, padx=10)

    btn2 = Button(frame, text='Даня', bg='MediumPurple', fg='Navy', command=DAN.chosen_for_fight1)
    btn2.pack(side=RIGHT, padx=10)

    btn3 = Button(frame, text='Федя', bg='PeachPuff', fg='Coral', command=FEDYA.chosen_for_fight1)
    btn3.pack(side=LEFT, padx=10)

    btn4 = Button(frame, text='Моня', bg='Pink', fg='MediumVioletRed', command=MONYA.chosen_for_fight1)
    btn4.pack(side=LEFT, padx=10)


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


# ______________________________________________window for choice_____________________________________________________

def dialogue(event):
    def first_button():
        MASHA.rise_friendship()
        dial.destroy()

    def second_button():
        MASHA.tell_skill_details()
        dial.destroy()

    dial = Toplevel(root)
    dial['bg'] = 'LightCyan'
    dial.title('Что будем делать?')
    dial.geometry('300x150+500+100')
    dial.grab_set()
    dial.resizable(False, False)
    question = Label(dial, text='???', bg='LightCyan', fg='SteelBlue', font=('Times New Roman', 18))
    question.pack(padx=95, pady=30)
    frame = Frame(dial, width=300, height=50, bg='LightCyan')
    frame.pack()
    btn1 = Button(frame, text='Подружимся!', bg='Orchid', fg='purple', command=first_button)
    btn1.pack(side=LEFT, padx=10)
    btn2 = Button(frame, text='Узнаем скиллы!', bg='SlateBlue', fg='Navy', command=second_button)
    btn2.pack(side=RIGHT, padx=10)


root.bind('<Return>', dialogue)


# ______________________________________________window for input_____________________________________________________

def input_info(event):
    def button():
        new = from_user.get()
        info.destroy()
        print(new)  # контроль

    info = Toplevel(root)
    info['bg'] = 'moccasin'
    info.title('Ввод')
    info.geometry('350x150+500+100')
    info.grab_set()
    # какой-то текст
    question = Label(info, text='Введите паспортные данные и номер карты', bg='moccasin',
                     fg='PeachPuff4', font=('Times New Roman', 12))
    question.pack()
    # окно ввода
    from_user = Entry(info)
    from_user.pack(anchor=NW)
    from_user.focus()  # курсор
    # кнопка, сохраняет инфу в переменную
    btn_in = Button(info, text='Принять!', bg='MediumPurple4', fg='OldLace', command=button)
    btn_in.pack(anchor=NW)


root.bind('<Button-3>', input_info)  # правая кнопка мыши

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
MONYA.kill = 4
MONYA.synth = 1
FEDYA = Friends('Федя', 'orange')
FEDYA.shield = 2
FEDYA.sem = 1
IB = Character('Инна Бисер', 'pink')
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

# пока все-таки напишу сюда, но оно выскочит сразу с основным окном, причем в основном не потыкаться, пока с диалоговым не закончить
fight_choice()
# ___________________________________________________END>_____________________________________________________________
frm1.pack(fill="both", expand=True)
frm2.pack(anchor='s')
btn.pack(anchor='ne', padx=10, pady=10)
root.mainloop()
# ___________________________________________________<END_____________________________________________________________
