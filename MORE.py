from tkinter import *
import random

class GUIDie(Canvas):
    '''++++++++++ GUI'''

    def __init__(self, master, valueList=[1, 2, 3, 4, 5, 6], colorList=['black'] * 6):
        '''GUIDie(master,[valueList,colorList]) -> GUIDie
        creates a GUI 6-sided die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        # create a 60x60 white canvas with a 5-pixel grooved border
        Canvas.__init__(self, master, width=60, height=60, bg='white', bd=5, relief=GROOVE)
        # store the valuelist and colorlist
        self.valueList = valueList
        self.colorList = colorList
        # initialize the top value
        self.top = 1

    def get_top(self):
        '''GUIDie.get_top() -> int
        returns the value on the die'''
        return self.valueList[self.top - 1]

    def roll(self):
        '''GUIDie.roll()
        rolls the die'''
        self.top = random.randrange(1, 7)
        self.draw()

    def draw(self):
        """GUIDie.draw()
        draws the pips on the die"""
        # clear old pips first
        self.erase()
        # location of which pips should be drawn
        pipList = [
            [(1, 1)],
            [(0, 0), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 0), (0, 2), (2, 0), (2, 2)],
            [(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)],
            [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2)],
        ]
        for location in pipList[self.top - 1]:
            self.draw_pip(location, self.colorList[self.top - 1])

    def draw_pip(self, location, color):
        '''GUIDie.draw_pip(location,color)
        draws a pip at (row,col) given by location, with given color'''
        (centerx, centery) = (15 + 20 * location[1], 15 + 20 * location[0])  # center
        self.create_oval(centerx - 5, centery - 5, centerx + 5, centery + 5, fill=color)

    def erase(self):
        '''GUIDie.erase()
        erases all the pips'''
        pipList = self.find_all()
        for pip in pipList:
            self.delete(pip)



class GUIFreezeableDie(GUIDie):
    '''a GUIDie that can be "frozen" so that it can't be rolled'''

    def __init__(self, master ,valueList=[1,2,3,4,5,6],colorList=['black']*6):
        '''GUIFreezeableDie(master,[valueList,colorList]) -> GUIFreezeableDie
        creates a GUI 6-sided freeze-able die
          valueList is the list of values (1,2,3,4,5,6 by default)
          colorList is the list of colors (all black by default)'''
        # you add code here
        GUIDie.__init__(self, master, valueList, colorList)
        self.frozen = False

    def is_frozen(self):
        '''GUIFreezeableDie.is_frozen() -> bool
        returns True if the die is frozen, False otherwise'''
        # you add code here
        return self.frozen

    def toggle_freeze(self):
        '''GUIFreezeableDie.toggle_freeze()
        toggles the frozen status'''
        # you add code here
        if self.frozen:
            self.configure(bg = 'white')
            self.frozen = False
        else:
            self.configure(bg = 'gray')
            self.frozen = True

    def roll(self):
        '''GuiFreezeableDie.roll()
        overloads GUIDie.roll() to not allow a roll if frozen'''
        if not self.frozen:
            self.top = random.randrange(1, 7)
            self.draw()

class FreezeTest(Frame):
    '''a small application to test the freezeable die'''
    def __init__(self,master, name):
        Frame.__init__(self,master)
        self.grid()
        self.score = 0
        self.maxs = []
        self.attempt = 1
        # set up labels
        Label(self, text=name, font=('Arial', 13)).grid(columnspan=3, sticky=W)
        self.scoreLabel = Label(self, text='Attempt #1 Score: 0', font=('Arial', 13))
        self.scoreLabel.grid(row=0, column=2, columnspan=2)
        self.maxLabel = Label(self, text='High Score: 0', font=('Arial', 13))
        self.maxLabel.grid(row=0, column=5, columnspan=3, sticky=E)
        self.instruct = Label(self, text='Click Roll to start', font=('Arial', 13))
        self.instruct.grid(row=4, column=1, columnspan=3, sticky=E)
        # set up dice
        self.dice = []
        self.buttons = []
        self.permanant = [False, False, False, False, False]
        for n in range(5):
            self.dice.append(GUIFreezeableDie(self, [1, 2, 3, 4, 5, 6], ['red', 'black', 'red', 'black', 'red', 'black']))
            self.dice[n].grid(row=2, column=n)
            button = Button(self, text='Freeze', state=DISABLED, command=self.dice[n].toggle_freeze)
            button.grid(row=3, column=n)
            self.buttons.append(button)
        self.roll = Button(self, text='Roll', command=self.roll)
        self.roll.grid(row=2, column=5)
        self.stop = Button(self, text='Stop', state=DISABLED, command=self.stop)
        self.stop.grid(row=3, column=5)

    def roll(self):
        if self.stop['state'] == DISABLED:
            self.stop['state'] = ACTIVE
        else:
            if [True if self.dice[i].is_frozen() else False for i in range(len(self.buttons))] == self.permanant: #checks for freeze, if equals no freeze has been made YET
                self.instruct['text'] = 'You must freeze a die to reroll'
                return None
            for i in range(len(self.permanant)):
                if self.dice[i].frozen:
                    self.permanant[i] = True
                    self.buttons[i]['state'] = DISABLED

        self.instruct['text'] = 'Click Stop to keep'
        self.score = 0

        for i in range(len(self.dice)):
            self.dice[i].roll()
            if self.dice[i].get_top() % 2 == 0:
                self.score += self.dice[i].get_top()
                if not self.permanant[i]:
                    self.buttons[i]['state'] = ACTIVE
                else:
                    self.buttons[i]['state'] = DISABLED
            else:
                self.buttons[i]['state'] = DISABLED
        if True in [True if not self.permanant[i] and self.dice[i].get_top() % 2 == 0 else False for i in range(len(self.dice))]: #CHECK FOR FOUL, if true then there can be something frozen so no FOUL
            self.scoreLabel['text'] = 'Attempt #{} Score: {}'.format(self.attempt, self.score)
        else:
            self.score = 0
            self.scoreLabel['text'] = 'FOULED ATTEMPT'
            self.instruct['text'] = 'Click FOUL to continue'
            self.roll['state'] = DISABLED
            self.stop['text'] = 'FOUL'

    def stop(self):
        self.attempt += 1
        self.maxs.append(self.score)
        self.maxLabel['text'] = 'High Score: {}'.format(max(self.maxs))
        for i in range(len(self.buttons)):
            self.buttons[i]['state'] = DISABLED
            self.dice[i].erase()
            if self.dice[i].is_frozen():
                self.dice[i].toggle_freeze()

        if self.attempt < 4:
            self.score = 0
            self.permanant = [False, False, False, False, False]
            self.roll['state'] = ACTIVE
            self.stop['state'] = DISABLED
            self.stop['text'] = 'Stop'
            self.scoreLabel['text'] = 'Attempt #{} Score: {}'.format(self.attempt, self.score)
            self.instruct['text'] = 'Click Roll to start'
        else:
            self.scoreLabel['text'] = 'GAME OVER'
            self.instruct.grid_remove()
            self.roll.grid_remove()
            self.stop.grid_remove()

        # test application
name = input("Enter your name: ")

root = Tk()
test = FreezeTest(root, name)
root.mainloop()