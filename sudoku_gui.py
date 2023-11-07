import sudoku as s
from tkinter import *
import copy
import time
import random


class Sudoku():

    def __init__ (self, master):
        # initialize the window
        self.master = master
        self.master.title("Sudoku")
        self.master.configure(bg="#E6BF83")
        self.master.geometry("650x700+600+100")
        self.master.resizable(False, False)

        # initialize the attributes
        self.board = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
        self.board_template = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
        self.board_answer = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
        self.entry_var = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
        self.block = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
        self.lbframe = [[0,0,0] for i in range(3)]
        self.sequence = ["1","2","3","4","5","6","7","8","9"]
        self.mode = IntVar()
        self.game_start = 0
        self.start_time = 0
        self.time_Val = 0
        self.hint_num = 0
        self.get_solution = 0
        
        # load the methods
        self.initialize_page()
        self.GameTimer()
        self.board_processing()


    def initialize_page (self):
        # title block
        lb1 = Label(self.master, text="Sudoku", width=10, font="Times 20 bold", bg="#E6BF83")
        lb1.grid (row=0, column=1)

        # start and stop buttons
        self.btn1 = Button(self.master, text ="Start", width=7, fg='white', bg='#6F4E37', font="Times 11 bold", padx=2, command=self.StartGame)
        self.btn1.grid(row=1, column=0)
        btn2 = Button(self.master, text ="Stop", width=7, fg='white', bg='#6F4E37', font="Times 11 bold", padx=2, command=self.StopGame)
        btn2.grid(row=1, column=2)

        # mode selection
        lb2 = Label(self.master, text="Select\nDifficulty:", width=7, height=4, font="Times 11 bold", bg="#E6BF83", justify="center")
        lb2.place(x=0, y=70)
        easy_mode = Radiobutton(self.master, text="Easy", variable=self.mode, value=1, bg="#E6BF83", font="Times 10 bold")
        medium_mode = Radiobutton(self.master, text="Medium", variable=self.mode, value=2, bg="#E6BF83", font="Times 10 bold")
        hard_mode = Radiobutton(self.master, text="Hard", variable=self.mode, value=3, bg="#E6BF83", font="Times 10 bold")
        easy_mode.place(x=0, y=130)
        medium_mode.place(x=0, y=160)
        hard_mode.place(x=0, y=190)
        easy_mode.select()

        # create grid
        self.create_9x9grid()

        # timer
        self.clock_lb = Label(self.master, font="Times 11 bold", bg="#E6BF83", justify="center")
        self.clock_lb.grid(row=3, column=1, sticky=E)

        # get answer
        btn3 = Button(self.master, text ="Hint", width=7, fg='white', bg='#6F4E37', font="Times 11 bold", command=self.get_hint)
        btn3.grid(row=3, column=0)
        btn4 = Button(self.master, text ="Solution", width=7, fg='white', bg='#6F4E37', font="Times 11 bold", command=self.print_solution)
        btn4.grid(row=4, column=0)

        # testing button - print board
        # btn5 = Button(self.master, text ="Print", width=7, fg='white', bg='#6F4E37', font="Times 11 bold", command=self.printt)
        # btn5.grid(row=5, column=0)


    def create_9x9grid (self):
       
        self.grid99 = Frame(self.master, bg="#E2A76F", bd=4, relief = "ridge")
        for i in range(0,9):
            for j in range(0,9):
                if i%3 == 0 and j%3 == 0:
                    self.lbframe[i//3][j//3] = LabelFrame(self.grid99, bd=3, relief="solid")
                    self.lbframe[i//3][j//3].grid(row=i//3, column=j//3)

                self.entry_var[i][j] = StringVar()
                if self.board_template[i][j] != 0:
                    self.block[i][j] = Entry(self.lbframe[i//3][j//3], fg="white", bg="#835C3B", font="Times 35 bold", width=2, bd=1, relief="solid", justify="center")
                    self.block[i][j].insert(0,str(self.board_template[i][j]))
                    self.block[i][j]["state"] = "disabled"
                    self.block[i][j].grid(row=i%3, column=j%3)
                else:
                    self.block[i][j] = Entry(self.lbframe[i//3][j//3], fg="white", bg="#DEB887", font="Times 35 bold", width=2, bd=1, relief="solid", justify="center")
                    self.block[i][j].grid(row=i%3, column=j%3)
                    self.block[i][j]['textvariable'] = self.entry_var[i][j]
        
        self.grid99.grid(row=2, column=1)

  
    def StartGame(self):
        self.game_start = 1
        self.start_time = time.time()
        self.btn1['state'] = "disabled"
        self.get_solution = 0
        self.hint_num = 0 

        # generate board
        num_of_space = 0
        mode = self.mode.get()
        match mode:
            case 1: num_of_space = 20
            case 2: num_of_space = 50
            case 3: num_of_space = 70
        self.board_template = s.generate_board(num_of_space)
        self.board = copy.deepcopy(self.board_template)
        board_temp = copy.deepcopy(self.board_template)
        self.board_answer = s.no_print_solve(board_temp)

        # recreate grid
        self.create_9x9grid()

    def StopGame(self):
        self.game_start = 0

        # stop menu window
        self.stop_menu = Tk()
        self.stop_menu.title("Stop menu")
        self.stop_menu.geometry("145x200+830+300")
        self.stop_menu.resizable(False,False)
        self.stop_menu.configure(bg="#E6BF83")

        btn_resume = Button(self.stop_menu, text="Resume", width=10, fg='white', bg="#6F4E37", font="Times 11 bold", command=self.Resume_btn)
        btn_resume.place(x=25, y=30, height=40)
        btn_restart = Button(self.stop_menu, text="Restart", width=10, fg='white', bg="#6F4E37", font="Times 11 bold", command=self.Restart_btn)
        btn_restart.place(x=25, y=80, height=40)    
        btn_exit = Button(self.stop_menu, text="Exit", width=10, fg='white', bg="#6F4E37", font="Times 11 bold", command=self.Exit_btn)
        btn_exit.place(x=25, y=130, height=40)


    def GameTimer(self):
        if self.game_start == 1:
            self.time_Val = round(time.time() - self.start_time, 0)
            seconds = int(self.time_Val % 60)
            minutes = int(self.time_Val // 60)
            self.clock_lb ['text'] = f'Timer: {minutes}min {seconds}s'
        self.master.after(1000, self.GameTimer)    


    def Resume_btn(self):
        # get back to game
        self.start_time = round(time.time(),0) - self.time_Val
        self.game_start = 1
        self.stop_menu.destroy()


    def Restart_btn(self):
        # restart a new game
        self.board = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
        self.board_template = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
        self.time_Val = 0
        self.stop_menu.destroy()
        self.btn1['state'] = "normal"

        # recreate grid
        self.create_9x9grid()

    def Exit_btn(self):
        # exit the game
        self.stop_menu.destroy()
        self.master.destroy()


    def board_processing(self):
        # link the variables to board
        if self.game_start == 1 and self.get_solution == 0:
            for i in range(0,9):
                for j in range(0,9):
                    if self.board_template[i][j] == 0:
                        num = self.entry_var[i][j].get()
                        if num in self.sequence:
                            if s.is_Valid(self.board, (i,j), int(num)):
                                self.board[i][j] = num
                                self.block[i][j]["bg"] = "#DEB887"
                            else:
                                self.block[i][j]["bg"] = "#FF6347"

        # game complete pop-up
            if s.find_empty(self.board) == 0:
                self.CompleteMenu()

            # call the function again
        self.master.after(500, self.board_processing)
            

    def CompleteMenu(self):
        #game complete pop-up
        self.complete_menu = Tk()
        self.complete_menu.title("Win!")
        self.complete_menu.geometry("120x170+830+300")
        self.complete_menu.resizable(False,False)
        self.complete_menu.configure(bg="#E6BF83")

        lb3 = Label(self.complete_menu, text="You Win!", width=7, height=4, font="Times 11 bold", bg="#E6BF83", justify="center", fg='#6F4E37')
        lb3.pack()

        btn_complete = Button(self.complete_menu, text="Restart", width=10, fg='white', bg="#6F4E37", font="Times 11 bold", command=self.Restart_btn_win)
        btn_complete.pack()

        lb4 = Label(self.complete_menu, text=f'\nYou used hint\n{self.hint_num} times', width=15, height=4, font="Times 11 bold", bg="#E6BF83", justify="center", fg='#6F4E37')
        lb4.pack()

        self.game_start = 0


    def Restart_btn_win(self):
        # restart a new game
        self.board = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
        self.board_template = [[0,0,0,0,0,0,0,0,0] for i in range(9)]
        self.time_Val = 0
        self.complete_menu.destroy()
        self.btn1['state'] = "normal"

        # recreate grid
        self.create_9x9grid()


    def get_hint(self):
        # give one answer to a random unanswered block
        self.hint_num += 1
        hint = 0

        while not hint:
            i = int(random.randint(0,8))
            j = int(random.randint(0,8))
            if self.board[i][j] == 0:
                self.block[i][j].delete(0)
                self.block[i][j].insert(0,str(self.board_answer[i][j]))
                self.block[i][j]["bg"] = "#DEB887"
                hint = 1

        
    def print_solution(self):
        # print solution on board
        self.get_solution = 1
        
        for i in range(9):
            for j in range(9):
                if self.board_template[i][j] == 0:
                    self.board[i][j] = self.board_answer[i][j]
                    self.block[i][j].delete(0)
                    self.block[i][j].insert(0,str(self.board_answer[i][j]))
                    self.block[i][j]["bg"] = "#DEB887"

'''
    def printt(self):
        print("board:")
        s.print_board(self.board)
        print("board template")
        s.print_board(self.board_template)
        print("board answer:")
        s.print_board(self.board_answer)
'''

if __name__ == "__main__":
    root = Tk()
    my_sudoku = Sudoku(root)
    root.mainloop()
