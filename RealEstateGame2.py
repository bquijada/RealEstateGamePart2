# coding=utf-8
# Author: Brenda Levy
# GitHub username: bqujiada
# Date: 5/23/22 
# Description: This project is a simplified version of the Monopoly board game called RealEstateGame. Players move
# around a 25 space board, and have the option to buy property and collect rent on that space. The game is over when
# everyone except the winner has $0 in their account.

class RealEstateGame:
    """RealEstateGame class to represent Real Estate game, played by two or more players. Players start at “GO” space
    on board. Take turns moving around the 25 board spaces, arranged in a circle."""

    def __init__(self):
        self._players_list = []  # list of player objects that are playing the game
        self._board = []         # layout of the board. List of Space objects.
        self._go_money = None

    def get_players_list(self):
        return self._players_list

    def get_board(self):
        return self._board

    def create_player(self, name, initial_balance):
        """takes a name and an initial account balance, creates a new player and adds it to the list of players. checks
        if name has already been taken."""
        for x in self._players_list:
            if x.get_name() == name:
                return "Name already taken"
        new_player = Player(name, initial_balance)
        self._players_list.append(new_player)

    def create_spaces(self, go_money, rent_amounts):
        """sets the amount of money for passing go and creates the game board with 25 space objects"""
        self._go_money = go_money
        go_space = Space(0, 0)
        go_space.set_ownership_status(True)  # set "GO" space ownership to True so that it cannot be bought
        self._board.append(go_space)
        num = 1
        for rent in rent_amounts:
            another_space = Space(num, rent)
            self._board.append(another_space)
            num += 1

    def get_player_account_balance(self, p_name):
        """takes player's name as parameter and returns that player's account balance"""
        for player in self._players_list:
            if player.get_name() == p_name:
                return player.get_balance()
        return "Player does not exist"

    def get_player_current_position(self, p_name):
        """takes as parameter the name of the player and returns the player's position on the board as an integer"""
        for player in self._players_list:
            if player.get_name() == p_name:
                return player.get_position()

    def find_space(self, num_to_buy):
        for space in self._board:
            if space.get_number() == num_to_buy:
                return space

    def buy_space(self, p_name):
        """takes as parameter the name of player. If the player has an account balance more than the purchase price,
         and the space doesn't already have an owner, then the player buys space. Price will be deducted from their
         account and player is set as the owner of the current space. In this case method returns true, otherwise
         returns False."""
        for player in self._players_list:
            if player.get_name() == p_name:
                player_to_buy = player
                current_balance = player_to_buy.get_balance()
                num_to_buy = player.get_position()
                space_to_buy = self.find_space(num_to_buy)
                if not space_to_buy.get_ownership_status():                              # if space not owned
                    if player_to_buy.get_balance() > space_to_buy.get_purchase_price():  # if player can afford
                        new_balance = current_balance - space_to_buy.get_purchase_price()
                        player_to_buy.set_balance(new_balance)
                        player.add_space_to_owned(space_to_buy)
                        space_to_buy.set_owner(player_to_buy)
                        return True
                    else:
                        return "Player cannot afford space."
                return "Space Already Owned."
        return False

    def move_player(self, p_name, num_moves):
        """takes as parameter the name of player and the number of spaces to move. Moves the player that number of
        spaces. Pays rent if necessary. Collects go money if necessary."""
        for player in self._players_list:
            if player.get_name() == p_name:
                player_to_move = player
                if player_to_move.get_balance() == 0:                               # check if player is already out
                    return
                else:
                    current_pos = player_to_move.get_position()                     # move player
                    current_balance = player_to_move.get_balance()
                    if current_pos + num_moves > 24:
                        new_pos = (current_pos + num_moves) - 25
                        player_to_move.set_position(new_pos)
                        player_to_move.set_balance(current_balance + self._go_money)  # collect money for passing go
                        if new_pos == 0:                                              # if current pos is go, return
                            return
                    else:
                        new_pos = current_pos + num_moves
                        player_to_move.set_position(new_pos)
                    for space in self._board:
                        if space.get_number() == new_pos:
                            current_space = space
                            if current_space.get_ownership_status():                   # if space is owned
                                if current_space in player_to_move.get_spaces_owned(): # if player owns space return
                                    return
                                else:
                                    self.pay_rent(space, player_to_move)                # pay rent
                            else:
                                return

    def pay_rent(self, space_object, player_object):
        """takes the player object and space object as parameters and pays rent to owner of space. If player cannot afford,
        pays renter the remainder of balance and removes player from the game."""
        current_balance = player_object.get_balance()
        rent_fee = space_object.get_rental_price()
        if (current_balance - rent_fee) <= 0:                     # if renter cannot afford rent
            rent_fee = current_balance
        player_object.set_balance(current_balance - rent_fee)
        for player in self._players_list:
            for owned in player.get_spaces_owned():
                if owned == space_object:
                    owner_balance = player.get_balance()
                    player.set_balance(owner_balance + rent_fee)  # pay owner rent
        if player_object.get_balance() == 0:                      # remove all properties from renter
            player_object.reset_owner_list()

    def check_game_over(self):
        """Takes no parameters and checks to see if there is only one person with money left in their account. If so,
        the game is over. Winner will be returned. If not returns an empty string."""
        winner = 0
        winner_name = None
        for player in self._players_list:
            if player.get_balance() != 0:
                winner += 1
                winner_name = player.get_name()
        if winner == 1:
            return winner_name
        else:
            return ""

    def view_game(self):
        """prints the current standings of the game"""
        for x in self._players_list:
            print("Name: ", x.get_name())
            print("current space: ", x.get_position())
            print("Balance: $", x.get_balance())
            for space in x.get_spaces_owned():
                print("Space owned: ", space.get_number())
            print(""
                  "")
        if self.check_game_over():
            print("Game over. Winner is: ", self.check_game_over())
        else:
            print("No winner yet.")


class Player:
    """layer class to represent a player of the Real Estate Game. Used by the RealEstateGame class. Players initialized
    to start at “GO”, they will have a unique name, and an account balance"""

    def __init__(self, name, balance):
        self._name = name
        self._balance = balance
        self._position = 0
        self._spaces_owned = []

    def get_name(self):
        """returns player’s name."""
        return self._name

    def get_balance(self):
        """returns player’s account balance."""
        return self._balance

    def set_balance(self, new_balance):
        """sets a player’s account balance."""
        self._balance = new_balance

    def get_position(self):
        """returns player’s position on the board."""
        return self._position

    def set_position(self, new_position):
        """sets a player’s position on the board."""
        self._position = new_position

    def get_spaces_owned(self):
        """returns list of spaces owned by player"""
        return self._spaces_owned

    def add_space_to_owned(self, space_object):
        """adds space to list of spaces owned by player"""
        self._spaces_owned.append(space_object)
        space_object.set_ownership_status(True)

    def reset_owner_list(self):
        """sets owner list"""
        for space in self._spaces_owned:
            space.set_ownership_status(False)
        self._spaces_owned = []

    def check_if_player_owns_space(self, space_name):
        """checks is space is owned by player"""
        if not self._spaces_owned:
            return False
        else:
            for space_obj in self._spaces_owned:
                num = space_obj.get_number()
                if num == space_name:
                    return True
            return False


class Space:
    """Space class to represent a space on the Real Estate Game. Used by the RealEstateGame class. Spaces will have a
     number, purchase price, a rental price, and a state of ownership (owned/not owned)"""

    def __init__(self, board_number, rental_price):
        self._board_number = board_number
        self._rental_price = rental_price
        self._purchase_price = 5 * rental_price
        self._ownership = False                     # initial ownership status: False (not owned).
        self._owner = None

    def get_number(self):
        """returns Space number."""
        return self._board_number

    def get_owner(self):
        """returns owner of space if there is one, otherwise returns None"""
        return self._owner

    def set_owner(self, owner):
        """sets the owner of a space"""
        self._owner = owner

    def get_rental_price(self):
        """returns player’s rental cost."""
        return self._rental_price

    def get_purchase_price(self):
        """returns space’s purchase price."""
        return self._purchase_price

    def get_ownership_status(self):
        """returns space’s ownership status. True for owned, False if not owned."""
        return self._ownership

    def set_ownership_status(self, status):
        """sets a space's ownership status, True for owned False for not owned."""
        self._ownership = status

    def space_from_number(self, num):
        """returns a space object given the number"""
        if self._board_number == num:
            return self

game = RealEstateGame()

rents = [50, 50, 50, 75, 75, 75, 100, 100, 100, 150, 150, 150, 200, 200, 200, 250, 250, 250, 300, 300, 300, 350, 350, 350]
game.create_spaces(50, rents)

game.create_player("Player 1", 1000)
game.create_player("Player 2", 10000)
game.create_player("Player 3", 1000)
game.create_player("Player 4", 251)

