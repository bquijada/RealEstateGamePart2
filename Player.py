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
