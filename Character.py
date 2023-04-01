from tkinter import *
from collections import deque


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

def input_info(text_out):  # это строка, которая реагирует на введённое имя
    def button():
        new = from_user.get()
        info.destroy()
        # в принимаемой строке $ заменяется введённым именем
        Q.appendleft(Label(f, fg='grey', font=20, wraplength=500, justify=LEFT,
                           text=f"{text_out.replace('$', name)}"))

    info = Toplevel(root)
    info['bg'] = 'moccasin'
    info.title('Ввод')
    info.geometry('350x150+500+100')
    info.grab_set()
    # какой-то текст
    question = Label(info, text='Имя...', bg='moccasin',
                     fg='PeachPuff4', font=('Times New Roman', 12))
    question.pack()
    # окно ввода
    from_user = Entry(info)
    from_user.pack(anchor=NW)
    from_user.focus()  # курсор
    # кнопка, сохраняет инфу в переменную
    btn_in = Button(info, text='Принять!', bg='MediumPurple4', fg='OldLace', command=button)
    btn_in.pack(anchor=NW)


# root.bind('<Button-3>', input_info)  # правая кнопка мыши   

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
# ___________________________________________________END>_____________________________________________________________
frm1.pack(fill="both", expand=True)
frm2.pack(anchor='s')
btn.pack(anchor='ne', padx=10, pady=10)
root.mainloop()
# ___________________________________________________<END_____________________________________________________________
