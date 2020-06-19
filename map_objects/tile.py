class Tile:
    """
    This class represents a tile on a map. It can block player movement or view, or it can have a trap on it.
    """

    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # The default for a tile that blocks movement is that it also blocks sight (ie. a Wall)
        if block_sight is None:
            block_sight = blocked
        
        self.block_sight = blocked
        self.explored = False
        self.trap = None