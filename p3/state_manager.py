import struct

from p3.state import State
from p3.state import PlayerType
from p3.state import Character
from p3.state import Menu
from p3.state import Stage
from p3.state import ActionState
from p3.state import BodyState

def int_handler(obj, name, shift=0, mask=0xFFFFFFFF, wrapper=None, default=0):
    """Returns a handler that sets an attribute for a given object.

    obj is the object that will have its attribute set. Probably a State.
    name is the attribute name to be set.
    shift will be applied before mask.
    Finally, wrapper will be called on the value if it is not None. If wrapper
    raises ValueError, sets attribute to default.

    This sets the attribute to default when called. Note that the actual final
    value doesn't need to be an int. The wrapper can convert int to whatever.
    This is particularly useful for enums.
    """
    def handle(value):
        transformed = (struct.unpack('>i', value)[0] >> shift) & mask
        setattr(obj, name, generic_wrapper(transformed, wrapper, default))
        if name not in ('frame', 'idle_time'):
            print('{} {} {}'.format(obj, name, transformed))
    setattr(obj, name, default)
    return handle

def float_handler(obj, name, wrapper=None, default=0.0):
    """Returns a handler that sets an attribute for a given object.

    Similar to int_handler, but no mask or shift.
    """
    def handle(value):
        as_float = struct.unpack('>f', value)[0]
        setattr(obj, name, generic_wrapper(as_float, wrapper, default))
        if name not in ('pos_y', 'pos_x', 'pos_z'):
            print('{} {} {}'.format(obj, name, as_float))
        elif name is 'pos_y' and as_float > 0.5:
            print('{} {} {}'.format(obj, name, as_float))
    setattr(obj, name, default)
    return handle

def generic_wrapper(value, wrapper, default):
    if wrapper is not None:
        try:
            value = wrapper(value)
        except ValueError:
            value = default
    return value

def add_address(x, y):
    """Returns a string representation of the sum of the two parameters.

    x is a hex string address that can be converted to an int.
    y is an int.
    """
    return "{0:08X}".format(int(x, 16) + y)

class StateManager:
    """Converts raw memory changes into attributes in a State object."""
    def __init__(self, state):
        """Pass in a State object. It will have its attributes zeroed."""
        self.state = state
        self.addresses = {}

        # Alternate frame memory addresses? Slightly different from each other for some reason...
        #self.addresses['8022345C'] = int_handler(self.state, 'frame')
        #self.addresses['80223460'] = int_handler(self.state, 'frame')
        #self.addresses['80223464'] = int_handler(self.state, 'frame')
        #self.addresses['8022615C'] = int_handler(self.state, 'frame')

        self.addresses['802775EC'] = int_handler(self.state, 'frame')
        self.addresses['8022627C'] = int_handler(self.state, 'total_rounds')

        self.state.players = []

        for player_id in range(5):
            player = State()
            self.state.players.append(player)

            # The fifth player id is the training dummy and is located further away
            if player_id > 3:
                data_pointer = add_address('80226358', 0x2BC * player_id)
            else:
                data_pointer = '802283FC'

            self.addresses[data_pointer + ' 28'] = int_handler(player, 'rounds_won', 0, 0xFF)
            self.addresses[data_pointer + ' 19C'] = float_handler(player, 'pos_x')
            self.addresses[data_pointer + ' 1A0'] = float_handler(player, 'pos_y')
            self.addresses[data_pointer + ' 1A4'] = float_handler(player, 'pos_z')
            self.addresses[data_pointer + ' 1BC'] = float_handler(player, 'direction_facing')
            self.addresses[data_pointer + ' 1DC'] = float_handler(player, 'vertical_speed')
            #self.addresses[data_pointer + ' 1E0'] = float_handler(player, 'gravitational_constant')
            #self.addresses[data_pointer + ' 1E0'] = int_handler(player, 'on_ground', 0, 0xFFFF, lambda x: x == 0, True)
            self.addresses[data_pointer + ' 1E8'] = float_handler(player, 'horizontal_air_speed')
            self.addresses[data_pointer + ' 23C'] = int_handler(player, 'body_state', 0, 0xFF, BodyState, BodyState.Normal)
            self.addresses[data_pointer + ' 258'] = int_handler(player, 'idle_time', 0, 0xFFFFFFFF)
            self.addresses[data_pointer + ' 260'] = int_handler(player, 'damage', 0, 0xFF)
            self.addresses[data_pointer + ' 28C'] = int_handler(player, 'chakra', 0, 0xFF)
            self.addresses[data_pointer + ' 294'] = int_handler(player, 'guard', 0, 0xFF)

    def handle(self, address, value):
        """Convert the raw address and value into changes in the State."""
        assert address in self.addresses
        handlers = self.addresses[address]
        if isinstance(handlers, list):
            for handler in handlers:
                handler(value)
        else:
            handlers(value)

    def locations(self):
        """Returns a list of addresses for exporting to Locations.txt."""
        return self.addresses.keys()
