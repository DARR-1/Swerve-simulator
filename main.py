import pygame
import math


chassis = pygame.Rect(225, 125, 350, 350)


def vectorsSum(*vectors: list) -> list:
    vector_r = []
    vectors_length = []
    for vector in vectors:
        vectors_length.append(len(vector))

    max_length = max(vectors_length)

    for vector in vectors:
        if len(vector) < max_length:
            for i in range(max_length - len(vector)):
                vector.append(0)

    for i in range(1, len(vectors)):
        if vector_r == []:
            for j in range(len(vectors[0])):
                components_sum = vectors[0][j] + vectors[1][j]
                vector_r.append(components_sum)
        else:
            for k in range(len(vector_r)):
                vector_r[k] += vectors[i][k]

    return vector_r


def maxValue(*values: float, limit=1.0) -> list:
    max_value = max(values)
    values_r = values
    if max_value > limit:
        values_r = []
        for value in values:
            append_value = value / max_value * limit
            values_r.append(append_value)

    return values_r


def distance(point1, point2) -> float:
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def movementVectorFront(
    direction_component_x, direction_component_y, angular_velocity
) -> tuple:
    direction_vector = [direction_component_x, direction_component_y]
    movement_vector = vectorsSum(direction_vector, [angular_velocity])

    vector_length = distance([0, 0], movement_vector)
    max_values = maxValue(vector_length, movement_vector[0], movement_vector[1])

    movement_vector = [max_values[1], max_values[2]]

    return movement_vector


def movementVectorBack(
    direction_component_x, direction_component_y, angular_velocity
) -> tuple:
    direction_vector = [direction_component_x, direction_component_y]
    movement_vector = vectorsSum(direction_vector, [-angular_velocity])

    vector_length = distance([0, 0], movement_vector)
    max_values = maxValue(vector_length, movement_vector[0], movement_vector[1])

    movement_vector = [max_values[1], max_values[2]]

    return movement_vector


def drawVectors(
    screen,
    movement_vector,
    direction_component_x,
    direction_component_y,
    angular_velocity,
    coords
) -> None:

    pygame.draw.line(
        screen,
        (0, 255, 0),
        coords,
        (direction_component_x * 100 + coords[0], direction_component_y * 100 + coords[1]),
        5,
    )

    pygame.draw.line(
        screen, (0, 0, 255), coords, (angular_velocity * 100 + coords[0], coords[1]), 5
    )

    pygame.draw.line(
        screen,
        (255, 0, 0),
        coords,
        (movement_vector[0] * 100 + coords[0], movement_vector[1] * 100 + coords[1]),
        5,
    )


def drawChassis(screen) -> None:
    motor_FR = pygame.Rect(chassis.right - 37.5, chassis.top - 37.5, 75, 75)
    motor_FL = pygame.Rect(chassis.left - 37.5, chassis.top - 37.5, 75, 75)
    motor_BR = pygame.Rect(chassis.right - 37.5, chassis.bottom - 37.5, 75, 75)
    motor_BL = pygame.Rect(chassis.left - 37.5, chassis.bottom - 37.5, 75, 75)
    pygame.draw.rect(screen, (0, 0, 0), chassis, 5)

    pygame.draw.rect(screen, (255, 255, 0), motor_FR)
    pygame.draw.rect(screen, (255, 255, 0), motor_FL)
    pygame.draw.rect(screen, (255, 255, 0), motor_BR)
    pygame.draw.rect(screen, (255, 255, 0), motor_BL)


def main() -> None:
    pygame.joystick.init()
    joysticks = [
        pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())
    ]
    print(joysticks)
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((800, 600))

    direction_component_x = 0
    direction_component_y = 0
    angular_velocity = 0

    movement_vector_front = movementVectorFront(
        direction_component_x, direction_component_y, angular_velocity
    )
    movement_vector_back = movementVectorBack(
        direction_component_x, direction_component_y, angular_velocity
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.JOYAXISMOTION:
                # print(
                #    "left stick x: ",
                #    pygame.joystick.Joystick(0).get_axis(0),
                #    "left stick y:",
                #    pygame.joystick.Joystick(0).get_axis(1),
                #    "right stick x: ",
                #    pygame.joystick.Joystick(0).get_axis(2),
                # )
                direction_component_x = pygame.joystick.Joystick(0).get_axis(0)
                direction_component_y = pygame.joystick.Joystick(0).get_axis(1)
                angular_velocity = pygame.joystick.Joystick(0).get_axis(2)

                movement_vector_front = movementVectorFront(
                    direction_component_x, direction_component_y, angular_velocity
                )
                movement_vector_back = movementVectorBack(
                    direction_component_x, direction_component_y, angular_velocity
                )

                print('front: ', movement_vector_front)
                print('back: ', movement_vector_back)
            else:
                movement_vector_front = [0, 0]
                movement_vector_back = [0, 0]

            screen.fill((255, 255, 255))

            drawChassis(screen)
            drawVectors(
                screen,
                movement_vector_front,
                direction_component_x,
                direction_component_y,
                angular_velocity,
                (chassis.left, chassis.top)
            )
            drawVectors(
                screen,
                movement_vector_front,
                direction_component_x,
                direction_component_y,
                angular_velocity,
                (chassis.right, chassis.top),
            )
            drawVectors(
                screen,
                movement_vector_back,
                direction_component_x,
                direction_component_y,
                -angular_velocity,
                (chassis.left, chassis.bottom),
            )
            drawVectors(
                screen,
                movement_vector_back,
                direction_component_x,
                direction_component_y,
                -angular_velocity,
                (chassis.right, chassis.bottom),
            )

            pygame.display.update()

            clock.tick(180)


if __name__ == "__main__":
    # print(vectorsSum([5, 1, 3], [0, 1], [2, 8, 9]))
    # print(maxValue(45, 896, 2, limit=5))
    main()
