class RealEstateGame:
    """RealEstateGame class to represent Real Estate game, played by two or more players. Players start at “GO” space
    on board. Take turns moving around the 25 board spaces, arranged in a circle."""

    def __init__(self):
        self._players_list = []  # list of player objects that are playing the game
        self._board = []         # layout of the board. List of Space objects.
        self._go_money = None

    def get_players_list(self):
        return self._players_list

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
                for space in self._board:
                    if space.get_number() == num_to_buy:
                        space_to_buy = space
                        if not space_to_buy.get_ownership_status():                              # if space not owned
                            if player_to_buy.get_balance() > space_to_buy.get_purchase_price():  # if player can afford
                                new_balance = current_balance - space_to_buy.get_purchase_price()
                                player_to_buy.set_balance(new_balance)
                                player.add_space_to_owned(space_to_buy)
                                return True
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

