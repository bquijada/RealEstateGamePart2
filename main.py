import random
from tkinter import *
from RealEstateGame2 import *
from tkinter import messagebox
import itertools as IT

root = Tk()
root.title("Real Estate Game")

# this is  a test for git

# Ask the user if they want to start a new game. Initiate new real estate game object with already determined rents

frame = LabelFrame(root, text="Real Estate Game", padx=50, pady=50)
frame.pack(padx=10, pady=10)

label_start = Label(frame, text="Do you want to start a new RealEstate Game?")
label_start.grid(row=0, column=0)

global new_game
global e
global button_1
global button_2
global current_player
global pay_rent

def button_new_game():
    """Allows the user to start a new game. Asks for the player's names."""
    global new_game
    global e
    new_game = RealEstateGame()
    game_rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300,
                  350,
                  350, 350]
    new_game.create_spaces(50, game_rents)
    label_entry = Label(frame, text="Enter each player's name individually (min. 2 players max. 4 players)")
    label_entry.grid(row=2, column=0)
    e = Entry(frame, width=20, borderwidth=5, bg="green", fg="white")
    e.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    button_1 = Button(frame, text="Submit player's name", padx=40, pady=20, command=button_enter_player)
    button_1.grid(row=4, column=0)
    button_2 = Button(frame, text="Players complete, start game", padx=40, pady=20, command=start_game, state=DISABLED)
    button_2.grid(row=4, column=2)


def button_enter_player():
    """Submits players names. Validates names are unique. After min. 2 players submitted, allows users to begin game"""
    global new_game
    global e
    initial_balance = 2000
    if not e.get():
        messagebox.showwarning("Name Error", "No name entered")
        return
    new_player = e.get()
    start = new_game.create_player(new_player, initial_balance)
    e.delete(0, END)
    if start == "Name already taken":
        messagebox.showwarning("Name Error", "Name taken already, please enter another name")
    label_accepted = Label(frame, text="Accepted Players:")
    label_accepted.grid(row=5, column=0)
    label_player = Label(frame, text=new_player)
    row_num = 6 + len(new_game.get_players_list())
    label_player.grid(row=row_num, column=0)
    if row_num == 10:  # if player's list is 6 players long
        button_1 = Button(frame, text="Submit player's name", padx=40, pady=20, command=button_enter_player,
                          state=DISABLED)
        button_1.grid(row=4, column=0)
    if row_num == 8:  # if player's list is at least 2 players long
        button_2 = Button(frame, text="Players complete, start game", padx=40, pady=20, command=start_game)
        button_2.grid(row=4, column=2)


button_0 = Button(frame, foreground='#54FA9B', text="Start New Game", padx=40, pady=20, command=button_new_game)
button_0.grid(row=1, column=0)

name_label = Label(frame)
label_ask = Label(frame)
label_roll = Label(frame)
button_continue = Button(frame)
label_no_buy = Label(frame)
button_yes = Button(frame)
button_no = Button(frame)
global money_label
global position_label
global label_list
global pos_list
global colors
global board_spaces_


def start_game():
    """Allows the users to begin the game. Shows chart showing the status of everyone's balance and position."""
    global new_game
    global current_player
    global name_label
    global money_label
    global position_label
    global label_list
    global pos_list
    global colors
    global board_spaces_

    colors = ['red', 'blue', 'yellow', 'green']

    # create the game board
    game_board_top = Toplevel()
    cols, rows = 7, 8
    board = [[None] * cols for _ in range(rows)]
    nums = ['GO', 1, 2, 3, 4, 5, 6, 25, 7, 24, 8, 23, 9, 22, 10, 21, 11, 20, 12, 19, 18, 17, 16, 15, 14, 13]
    x = 0

    for i, j in IT.product(range(rows), range(cols)):
        if i == 0 or i == 7:
            board[i][j] = L = Label(game_board_top, text=str(nums[x]), bg='light green', font=('Times', 24))
            x += 1
            L.grid(row=i, column=j, padx=3, pady=3)
        elif j == 0 or j == 6:
            board[i][j] = L = Label(game_board_top, text=str(nums[x]), bg='light green', font=('Times', 24))
            x += 1
            L.grid(row=i, column=j, padx=3, pady=3)

    # loop through all children in each frame and delete them.
    for widget in frame.winfo_children():
        widget.destroy()
    yaxis = 80
    pos_list = []
    label_list = []
    label_title = Label(frame, text="Player's Status")
    label_title.place(x=150, y=0)

    label_title = Label(frame, text="Color")
    label_title.place(x=0, y=20)

    label_title = Label(frame, text="Name")
    label_title.place(x=50, y=20)

    label_title = Label(frame, text="Balance ($)")
    label_title.place(x=150, y=20)

    label_title = Label(frame, text="Position")
    label_title.place(x=250, y=20)

    for player, color in zip(new_game.get_players_list(), colors):

        color_label = Label(frame, text='color', font='bold, 16', fg=color, bg=color)
        color_label.place(x=0, y=yaxis)

        name = player.get_name()
        name_label = Label(frame, text=name, font='bold, 16')
        name_label.place(x=50, y=yaxis)

        balance = player.get_balance()
        money_label = Label(frame, text=balance, font='bold, 16')
        money_label.place(x=150, y=yaxis)
        label_list.append(money_label)

        pos = str(player.get_position())
        position_label = Label(frame, text=pos, font='bold, 16')
        position_label.place(x=250, y=yaxis)
        pos_list.append(position_label)

        yaxis = yaxis + 35

    def update():
        """updates all balance and position chart for users to see"""
        global money_label
        global position_label
        global label_list
        global pos_list
        for label in label_list:
            label.destroy()
        for label in pos_list:
            label.destroy()
        yaxis = 80
        for player_obj in new_game.get_players_list():
            money = player_obj.get_balance()
            money_label = Label(frame, text=money, font='bold, 16')
            money_label.place(x=150, y=yaxis)
            label_list.append(money_label)

            pos = str(player_obj.get_position())
            position_label = Label(frame, text=pos, font='bold, 16')
            position_label.place(x=250, y=yaxis)
            pos_list.append(position_label)

            yaxis += 35

    def buy_space():
        """checks if player can buy space, and purchases it if possible. User is updated."""
        global button_yes
        global button_no
        global current_player
        global button_continue
        global label_no_buy
        button_yes.destroy()
        button_no.destroy()
        button_yes = Button(frame, text="Yes", padx=20, pady=20, command=buy_space, state=DISABLED)
        button_yes.place(x=360, y=220)
        button_no = Button(frame, text="No", padx=20, pady=20, command=dont_buy, state=DISABLED)
        button_no.place(x=450, y=220)
        button_continue.destroy()
        answer = new_game.buy_space(current_player.get_name())
        if answer is True:
            label_no_buy = Label(frame, text="Congrats you bought space " + str(current_player.get_position()) + "! "
                                              + "Your new balance is: " + str(current_player.get_balance()))
            label_no_buy.place(x=360, y=300)
            update()
        else:
            label_no_buy = Label(frame, text="Purchase unsuccessful. " + answer)
            label_no_buy.place(x=360, y=300)
        button_continue = Button(frame, text="Next Player", command=next_player, padx=20, pady=20)
        button_continue.place(x=560, y=220)

    def dont_buy():
        """if the user decides not to purchase the space the landed on. Informs player their turn is over"""
        global button_continue
        global label_no_buy
        update()
        button_continue.destroy()
        label_no_buy = Label(frame, text="No purchase made, turn over. Press next player to continue")
        label_no_buy.place(x=360, y=300)
        button_continue = Button(frame, text="Next Player", command=next_player, padx=20, pady=20)
        button_continue.place(x=560, y=220)
        return

    def roll_dice():
        """allows the user to roll the dice and move on the board. Asks what they would like to do on their new space"""
        global label_ask
        global label_roll
        global button_continue
        global button_yes
        global button_no
        global pay_rent
        roll = random.randint(1, 8)
        new_game.move_player(current_player.get_name(), roll)
        label_roll = Label(frame, text="You rolled " + str(roll) + ". Your new position is " + str(
            current_player.get_position()))
        label_roll.place(x=360, y=100)
        space_obj = new_game.find_space(current_player.get_position())
        update()  # updated player's balance to account for passing go
        if current_player.get_position() == 0:
            label_ask = Label(frame, text="You landed on GO. Nothing to buy here, collect GO $. Turn over.")
            label_ask.place(x=360, y=150)
            button_continue = Button(frame, text="Next Player", command=next_player, padx=20, pady=20)
            button_continue.place(x=560, y=220)
        elif current_player.check_if_player_owns_space(current_player.get_position()):  # if user already owns space
            label_ask = Label(frame, text="Welcome home! You already own this space. Turn over.")
            label_ask.place(x=360, y=150)
            button_continue = Button(frame, text="Next Player", command=next_player, padx=20, pady=20)
            button_continue.place(x=560, y=220)
            return
        elif space_obj.get_ownership_status():  # if someone else owns space
            label_ask = Label(frame, text="Space already owned by " + space_obj.get_owner().get_name() + ". Please pay rent. "
                                          "Rent is $" +
                                          str(space_obj.get_rental_price()))
            label_ask.place(x=360, y=125)
            pay_rent = Button(frame, text="Pay Rent: -$" + str(space_obj.get_rental_price()), padx=20, pady=20,
                              command=lambda: rental_payment(space_obj, current_player))
            pay_rent.place(x=370, y=160)
        else:
            label_ask = Label(frame, text="Do you want to buy this space for " + str(
                space_obj.get_purchase_price()) + " dollars ?")
            label_ask.place(x=360, y=150)
            button_yes = Button(frame, text="Yes", padx=20, pady=20, command=buy_space)
            button_yes.place(x=360, y=220)
            button_no = Button(frame, text="No", padx=20, pady=20, command=dont_buy)
            button_no.place(x=450, y=220)

    roll_dice_button = Button(frame, text="Click to Roll Dice", padx=40, pady=20, command=roll_dice)
    roll_dice_button.place(x=360, y=40)

    def rental_payment(space_, player_):
        """user pays owed rent to the property owner"""
        global button_continue
        global pay_rent
        new_game.pay_rent(space_, player_)
        update()
        button_continue = Button(frame, text="Next Player", command=next_player, padx=20, pady=20)
        button_continue.place(x=560, y=220)
        pay_rent.destroy()

    def destroy_all():
        """destroys all widgets in list_"""
        global name_label
        global label_ask
        global label_roll
        global button_yes
        global button_no
        list_ = [name_label, label_roll, label_ask, label_no_buy, button_no, button_yes]
        for label in list_:
            label.destroy()

    def next_player():
        """gives the next player their turn. If there is already a winner, changes to winner screen"""
        global current_player
        global name_label
        destroy_all()
        button_continue = Button(frame, text="Next Player", command=next_player, padx=20, pady=20, state=DISABLED)
        button_continue.place(x=560, y=220)
        if new_game.check_game_over() == "":
            player_list = new_game.get_players_list()
            index = player_list.index(current_player) + 1
            if index == len(player_list):
                index = 0
            current_player = player_list[index]
            name_label = Label(frame, text="It is " + current_player.get_name() + "'s turn!", font='bold, 16')
            name_label.place(x=420, y=0)
        else:
            for widget in frame.winfo_children():
                widget.destroy()
            label_winner = Label(frame, text="GAME OVER WINNER IS: " + new_game.check_game_over(), font='bold, 30')
            label_winner.pack()

    current_player = new_game.get_players_list()[0]
    name_label = Label(frame, text="It is " + current_player.get_name() + "'s turn!", font='bold, 16')
    name_label.place(x=420, y=0)


root.mainloop()
