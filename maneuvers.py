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
        px.set_dir_servo_angle(-39)
        time.sleep(0.5)
        px.backward(60)
        time.sleep(0.75)

        px.set_dir_servo_angle(39)
        time.sleep(0.5)
        px.backward(60)
        time.sleep(0.5)

        px.set_dir_servo_angle(0)
        time.sleep(0.5)
        px.forward(60)
        time.sleep(0.5)
    
    elif initial_direction == 'right':
        px.set_dir_servo_angle(39)
        time.sleep(0.5)
        px.backward(60)
        time.sleep(0.75)

        px.set_dir_servo_angle(-39)
        time.sleep(0.5)
        px.backward(60)
        time.sleep(0.5)

        px.set_dir_servo_angle(0)
        time.sleep(0.5)
        px.forward(60)
        time.sleep(0.5)
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
    movement_type = 'enterloop'
    movements = ['vanilla', 'parallel-park', 'k-turn', 'terminate', 'v', 'pp', 'k', 't']
    while movement_type != 'terminate':
        movement_type = input('Enter movement type (vanilla, parallel-park, k-turn, terminate): ').lower()
        print(movement_type)
        while not True in [m == movement_type for m in movements]:
            movement_type = input('Try again!!! Enter movement type (vanilla, parallel-park, k-turn, terminate): ').lower()
        if (movement_type == 'terminate') or (movement_type == 't'):
            continue
        elif (movement_type == 'vanilla') or (movement_type == 'v'):
            direction = int(input('Enter turn angle ([-40:40] degrees): '))
            speed = int(input('Enter a negative or positve value for velocity: '))
            duration = float(input('Enter a drive duration (seconds): '))
            vanilla_movement(px, direction, speed, duration)
        elif (movement_type == 'parallel-park') or (movement_type == 'pp'):
            initial_direction = input('Enter a starting direction (left or right): ').lower()
            parallel_park(px, initial_direction)
        elif (movement_type == 'k-turn') or (movement_type == 'k'):
            initial_direction = input('Enter a starting direction (left or right): ').lower()
            k_turn(px, initial_direction)
    print('Exiting program')
