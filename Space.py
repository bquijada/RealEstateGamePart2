class Space:
    """Space class to represent a space on the Real Estate Game. Used by the RealEstateGame class. Spaces will have a
     number, purchase price, a rental price, and a state of ownership (owned/not owned)"""

    def __init__(self, board_number, rental_price):
        self._board_number = board_number
        self._rental_price = rental_price
        self._purchase_price = 5 * rental_price
        self._ownership = False                     # initial ownership status: False (not owned).

    def get_number(self):
        """returns Space number."""
        return self._board_number

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
