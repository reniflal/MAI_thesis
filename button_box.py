from psychopy import visual
class button_box:

    def __init__(self, window):
        self.color_one = 'red'
        self.color_two = 'green'
        self.color_three = 'blue'
        self.win = window
        self.size = 70
        self.pos1 = (-300,100)
        self.pos2 = (-200,100)
        self.pos3 = (-100,100)
        self.pos4 = (0,100)
        self.pos5 = (100,100)
        self.pos6 = (200,100)
        self.pos7 = (300,100)
        self.pos8 = (-300,0)
        self.pos9 = (-200,0)
        self.pos10 = (-100,0)
        self.pos11 = (0,0)
        self.pos12 = (100,0)
        self.pos13 = (200,0)
        self.pos14 = (300,0)
        self.pos15 = (0,-100)
        self.pos16 = (0,-200)
        
       
    def create_all(self):
        self.rect_one = visual.Rect( win=self.win, name="one", fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos1, opacity=1)
        self.text_one = visual.TextStim(win=self.win, text='Box 1', color='black', height=20, pos=self.pos1)
        self.rect_two = visual.Rect( win=self.win, name="two",fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos2, opacity=1)
        self.text_two = visual.TextStim(win=self.win, text='Box 2', color='black', height=20, pos=self.pos2)
        self.rect_three = visual.Rect( win=self.win, name="three",fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos3, opacity=1)
        self.text_three = visual.TextStim(win=self.win, text='Box 3', color='black', height=20, pos=self.pos3)
        self.rect_four = visual.Rect( win=self.win, name="four",fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos4, opacity=1)
        self.text_four = visual.TextStim(win=self.win, text='Box 4', color='black', height=20, pos=self.pos4)

        self.rect_five = visual.Rect( win=self.win, name="five", fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos5, opacity=1)
        self.text_five = visual.TextStim(win=self.win, text='Box 5', color='black', height=20, pos=self.pos5)
        self.rect_six = visual.Rect( win=self.win, name="six",fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos6, opacity=1)
        self.text_six = visual.TextStim(win=self.win, text='Box 6', color='black', height=20, pos=self.pos6)
        self.rect_seven = visual.Rect( win=self.win, name="seven",fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos7, opacity=1)
        self.text_seven = visual.TextStim(win=self.win, text='Box 7', color='black', height=20, pos=self.pos7)
        self.rect_eight = visual.Rect( win=self.win, name="eight",fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos8, opacity=1)
        self.text_eight = visual.TextStim(win=self.win, text='Box 8', color='black', height=20, pos=self.pos8)

        self.rect_nine = visual.Rect( win=self.win, name="nine", fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos9, opacity=1)
        self.text_nine = visual.TextStim(win=self.win, text='Box 9', color='black', height=20, pos=self.pos9)
        self.rect_ten = visual.Rect( win=self.win, name="ten",fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos10, opacity=1)
        self.text_ten = visual.TextStim(win=self.win, text='Box 10', color='black', height=20, pos=self.pos10)
        self.rect_eleven = visual.Rect( win=self.win, name="eleven",fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos11, opacity=1)
        self.text_eleven = visual.TextStim(win=self.win, text='Box 11', color='black', height=20, pos=self.pos11)
        self.rect_twelve = visual.Rect( win=self.win, name="twelve",fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos12, opacity=1)
        self.text_twelve = visual.TextStim(win=self.win, text='Box 12', color='black', height=20, pos=self.pos12)

        self.rect_thirteen = visual.Rect( win=self.win, name="thirteen", fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos13, opacity=1)
        self.text_thirteen = visual.TextStim(win=self.win, text='Box 13', color='black', height=20, pos=self.pos13)
        self.rect_fourteen = visual.Rect( win=self.win, name="fourteen",fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos14, opacity=1)
        self.text_fourteen = visual.TextStim(win=self.win, text='Box 14', color='black', height=20, pos=self.pos14)
        self.rect_fifteen = visual.Rect( win=self.win, name="fifteen",fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos15, opacity=1)
        self.text_fifteen = visual.TextStim(win=self.win, text='Box 15', color='black', height=20, pos=self.pos15)
        self.rect_sixteen = visual.Rect( win=self.win, name="sixteen",fillColor=self.color_one, lineColor=self.color_one,  size=self.size,
                                pos=self.pos16, opacity=1)
        self.text_sixteen = visual.TextStim(win=self.win, text='Box 16', color='black', height=20, pos=self.pos16)
    def draw_all(self):
        self.rect_one.draw()
        self.text_one.draw()
        self.rect_two.draw()
        self.text_two.draw()
        self.rect_three.draw()
        self.text_three.draw()
        self.rect_four.draw()
        self.text_four.draw()

        self.rect_five.draw()
        self.text_five.draw()
        self.rect_six.draw()
        self.text_six.draw()
        self.rect_seven.draw()
        self.text_seven.draw()
        self.rect_eight.draw()
        self.text_eight.draw()

        self.rect_nine.draw()
        self.text_nine.draw()
        self.rect_ten.draw()
        self.text_ten.draw()
        self.rect_eleven.draw()
        self.text_eleven.draw()
        self.rect_twelve.draw()
        self.text_twelve.draw()

        self.rect_thirteen.draw()
        self.text_thirteen.draw()
        self.rect_fourteen.draw()
        self.text_fourteen.draw()
        self.rect_fifteen.draw()
        self.text_fifteen.draw()
        self.rect_sixteen.draw()
        self.text_sixteen.draw()

    def update_button_color(self, button_number, color):
        if(button_number == 1):
            self.rect_one.fillColor = color
            self.rect_one.lineColor = color
        elif (button_number == 2):
            self.rect_two.fillColor = color
            self.rect_two.lineColor = color
        elif (button_number == 3):
            self.rect_three.fillColor = color
            self.rect_three.lineColor = color
        elif (button_number == 4):
            self.rect_four.fillColor = color
            self.rect_four.lineColor = color
        elif (button_number == 5):
            self.rect_five.fillColor = color
            self.rect_five.lineColor = color
        elif (button_number == 6):
            self.rect_six.fillColor = color
            self.rect_six.lineColor = color
        elif (button_number == 7):
            self.rect_seven.fillColor = color
            self.rect_seven.lineColor = color
        elif (button_number == 8):
            self.rect_eight.fillColor = color
            self.rect_eight.lineColor = color
        elif (button_number == 9):
            self.rect_nine.fillColor = color
            self.rect_nine.lineColor = color
        elif (button_number == 10):
            self.rect_ten.fillColor = color
            self.rect_ten.lineColor = color
        elif (button_number == 11):
            self.rect_eleven.fillColor = color
            self.rect_eleven.lineColor = color
        elif (button_number == 12):
            self.rect_twelve.fillColor = color
            self.rect_twelve.lineColor = color
        elif (button_number == 13):
            self.rect_thirteen.fillColor = color
            self.rect_thirteen.lineColor = color
        elif (button_number == 14):
            self.rect_fourteen.fillColor = color
            self.rect_fourteen.lineColor = color
        elif (button_number == 15):
            self.rect_fifteen.fillColor = color
            self.rect_fifteen.lineColor = color
        elif (button_number == 16):
            self.rect_sixteen.fillColor = color
            self.rect_sixteen.lineColor = color

    def check_button_gaze(self, button_number,eye_position):
        if(button_number == 1):
           return  (self.rect_one.contains(eye_position))
        elif (button_number == 2):
           return  (self.rect_two.contains(eye_position))
        elif (button_number == 3):
           return  (self.rect_three.contains(eye_position))
        elif (button_number == 4):
           return  (self.rect_four.contains(eye_position))
        elif (button_number == 5):
           return  (self.rect_five.contains(eye_position))
        elif (button_number == 6):
           return  (self.rect_six.contains(eye_position))
        elif (button_number == 7):
           return  (self.rect_seven.contains(eye_position))
        elif (button_number == 8):
           return  (self.rect_eight.contains(eye_position))
        elif (button_number == 9):
           return  (self.rect_nine.contains(eye_position))
        elif (button_number == 10):
           return  (self.rect_ten.contains(eye_position))
        elif (button_number == 11):
           return  (self.rect_eleven.contains(eye_position))
        elif (button_number == 12):
           return  (self.rect_twelve.contains(eye_position))
        elif (button_number == 13):
           return  (self.rect_thirteen.contains(eye_position))
        elif (button_number == 14):
           return  (self.rect_fourteen.contains(eye_position))
        elif (button_number == 15):
           return  (self.rect_fifteen.contains(eye_position))
        elif (button_number == 16):
           return  (self.rect_sixteen.contains(eye_position))


        

