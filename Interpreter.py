class Interpreter:
    """interpreter class"""
    def __init__(self, size=10):

        self.view = []
        self.size = size

    def get_state(self, view, direction):
        """convert snake view into state"""
        self.view = view
        forward = direction
        right = (direction + 1) % 4
        left = (direction - 1)
        view_forward = view[forward]
        view_right = view[right]
        view_left = view[left]
        state = (
            get_nearest_object(view_left, self.size),
            get_nearest_object(view_forward, self.size),
            get_nearest_object(view_right, self.size),
        )
        return state

    def print_view(self):
        indent = ''
        for i in range(len(self.view[0])):
            indent += ' '
        for i in range(len(self.view[1]) - 1, -1, -1):
            str = indent + self.view[1][i]
            print(str)
        str = ''
        for i in range(len(self.view[0]) - 1, -1, -1):
            str += self.view[0][i]
        str += 'H'
        for i in range(len(self.view[2])):
            str += self.view[2][i]
        print(str)
        for i in range(len(self.view[3])):
            str = indent + self.view[3][i]
            print(str)
        print()

    def print_dir(self, direction):
        """print moving direction of snake wrt board"""
        dirs = ['LEFT', 'UP', 'RIGHT', 'DOWN']
        print('Step taken:', dirs[direction])
        print()


def get_nearest_object(view, size):
    objects = ['W', 'S', 'R', 'G']
    for i in range(len(view)):
        if view[i] in objects:
            return get_scaled_distance(i, size), view[i]


def get_scaled_distance(d, size):
    """returning normalized distance range"""
    if size > 3:
        d_norm = d / size * 10
        if d_norm == 0:
            return 'adj'
        elif d_norm > 0 and d_norm <= 3:
            return 'near'
        elif d_norm > 3 and d_norm <= 7:
            return 'mid'
        else:
            return 'far'
    else:
        d_norm = d
        if d_norm == 0:
            return 'adj'
        elif d_norm == 1:
            return 'near'
        elif d_norm == 2:
            return 'mid'
        else:
            return 'far'