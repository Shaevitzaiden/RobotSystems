from picarx_improved import Picarx


def vanilla_movement(direction, speed, duration):
    pass

def parallel_park():
    pass

def k_turn(initial_direction):
    pass


if __name__ == "__main__":
    movement_type = input('Enter movement type (vanilla, parallel-park, k-turn, terminate): ').lower()
    while movement_type != 'terminate':
        while movement_type != ('vanilla' or 'parallel-park' or 'k-turn' or 'terminate'):
            movement_type = input('Try again!!! Enter movement type (vanilla, parallel-park, k-turn, terminate): ').lower()
        if movement_type == 'terminate':
            continue
        elif movement_type == 'vanilla':
            direction = int(input('Enter turn angle ([-40:40] degrees): '))
            speed = int(input('Enter a negative or positve value for velocity: '))
            duration = float(input('Enter a drive duration (seconds): '))
            vanilla_movement(direction, speed, duration)
        elif movement_type == 'parallel-park':
            parallel_park()
        elif movement_type == 'k-turn':
            initial_direction = input('Enter a starting direction (left or right): ')
            k_turn(initial_direction)
