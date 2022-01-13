from picarx_improved import Picarx
import time


def vanilla_movement(px, direction, speed, duration):
    px.set_dir_servo_angle(direction)
    time.sleep(0.5)
    if speed >= 0:
        px.forward(speed)
    else:
        px.backward(abs(speed))
    time.sleep(duration)
    px.stop()
    
def parallel_park(px, initial_direction):
    if initial_direction == 'left':
        px.set_dir_servo_angle(-40)
        time.sleep(0.5)
        px.backward(30)
        time.sleep(2)

        px.set_dir_servo_angle(40)
        time.sleep(0.5)
        px.backward(30)
        time.sleep(3)

        px.set_dir_servo_angle(0)
        time.sleep(0.5)
        px.forward(20)
        time.sleep(1)
    
    elif initial_direction == 'right':
        px.set_dir_servo_angle(40)
        time.sleep(0.5)
        px.backward(30)
        time.sleep(2)

        px.set_dir_servo_angle(-40)
        time.sleep(0.5)
        px.backward(30)
        time.sleep(3)

        px.set_dir_servo_angle(0)
        time.sleep(0.5)
        px.forward(20)
        time.sleep(1)
    px.stop()


def k_turn(px, initial_direction):
    if initial_direction == 'left':
        px.set_dir_servo_angle(-40)
        time.sleep(0.5)
        px.forward(40)
        time.sleep(2)

        px.set_dir_servo_angle(20)
        time.sleep(0.5)
        px.backward(40)
        time.sleep(1)

        px.set_dir_servo_angle(-30)
        time.sleep(0.5)
        px.forward(40)
        time.sleep(3)

    elif initial_direction == 'right':
        px.set_dir_servo_angle(40)
        time.sleep(0.5)
        px.forward(40)
        time.sleep(2)

        px.set_dir_servo_angle(-20)
        time.sleep(0.5)
        px.backward(40)
        time.sleep(1)

        px.set_dir_servo_angle(30)
        time.sleep(0.5)
        px.forward(40)
        time.sleep(3)
    px.stop()


if __name__ == "__main__":
    px = Picarx()
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
            vanilla_movement(px, direction, speed, duration)
        elif movement_type == 'parallel-park':
            initial_direction = input('Enter a starting direction (left or right): ').lower()
            parallel_park(px, initial_direction)
        elif movement_type == 'k-turn':
            initial_direction = input('Enter a starting direction (left or right): ').lower()
            k_turn(px, initial_direction)
    print('Exiting program')
