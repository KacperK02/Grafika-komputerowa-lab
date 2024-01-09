import pygame
from OpenGL.raw.GLU import gluPerspective
from pygame.locals import *
from OpenGL.GL import *
from PIL import Image

points = [
            [-1, -1, 1],
            [1, -1, 1],
            [0, 1, 1],
            [0, 0.02, -1]
        ]

camera_speed = 0.05
zoom_speed = 0.1


def set_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)  # Kierunkowe źródło światła
    glEnable(GL_LIGHT1)  # Punktowe źródło światła

    glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 1.0, 1.0, 0.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])

    glLightfv(GL_LIGHT1, GL_POSITION, [2.0, 2.0, 0.0, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 0.0, 0.0, 1.0])

    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT, GL_AMBIENT_AND_DIFFUSE)


def draw_tetrahedron(v1, v2, v3, v4):
    draw_triangle(v1, v2, v3)
    draw_triangle(v1, v3, v4)
    draw_triangle(v2, v3, v4)
    draw_triangle(v1, v2, v4)


def draw_triangle(point_a, point_b, point_c):
    glBegin(GL_TRIANGLES)

    glColor3f(1, 1, 1)
    glVertex3f(*point_a)

    glColor3f(0.75, 0.75, 0.75)
    glVertex3f(*point_b)

    glColor3f(0.5, 0.5, 0.5)
    glVertex3f(*point_c)

    glEnd()


def draw_pyramid(v1, v2, v3, v4, level):
    if level == 0:
        draw_tetrahedron(v1, v2, v3, v4)
        return
    else:
        v12 = [
            (v1[0] + v2[0]) / 2,
            (v1[1] + v2[1]) / 2,
            (v1[2] + v2[2]) / 2
        ]

        v23 = [
            (v2[0] + v3[0]) / 2,
            (v2[1] + v3[1]) / 2,
            (v2[2] + v3[2]) / 2
        ]

        v31 = [
            (v1[0] + v3[0]) / 2,
            (v1[1] + v3[1]) / 2,
            (v1[2] + v3[2]) / 2
        ]

        v14 = [
            (v1[0] + v4[0]) / 2,
            (v1[1] + v4[1]) / 2,
            (v1[2] + v4[2]) / 2
        ]

        v24 = [
            (v2[0] + v4[0]) / 2,
            (v2[1] + v4[1]) / 2,
            (v2[2] + v4[2]) / 2
        ]

        v34 = [
            (v3[0] + v4[0]) / 2,
            (v3[1] + v4[1]) / 2,
            (v3[2] + v4[2]) / 2
        ]

        draw_pyramid(v1, v12, v31, v14, level - 1)
        draw_pyramid(v12, v2, v23, v24, level - 1)
        draw_pyramid(v31, v23, v3, v34, level - 1)
        draw_pyramid(v14, v24, v34, v4, level - 1)


def change_texture(state):
    if state:
        glDisable(GL_TEXTURE_2D)
    else:
        glEnable(GL_TEXTURE_2D)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


def main():
    while True:
        try:
            level = int(input("Podaj liczbę: "))
            if level > 0:
                break
            else:
                print("Podaj liczbe dodatnia")
        except ValueError:
            print("To nie jest liczba. Wpisz ponownie.")

    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)
    glEnable(GL_DEPTH_TEST)

    set_lighting()

    image = Image.open("tekstura.tga")
    glTexImage2D(
        GL_TEXTURE_2D, 0, 3, image.size[0], image.size[1], 0,
        GL_RGB, GL_UNSIGNED_BYTE, image.tobytes("raw", "RGB", 0, -1)
    )
    texture_enabled = False

    print("Generowanie zakonczone")

    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            glTranslatef(0, -camera_speed, 0)
        if keys[pygame.K_DOWN]:
            glTranslatef(0, camera_speed, 0)
        if keys[pygame.K_LEFT]:
            glTranslatef(camera_speed, 0, 0)
        if keys[pygame.K_RIGHT]:
            glTranslatef(-camera_speed, 0, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    change_texture(texture_enabled)
                    texture_enabled = not texture_enabled
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll Up (Zoom In)
                    glTranslatef(0, 0, zoom_speed)
                elif event.button == 5:  # Scroll Down (Zoom Out)
                    glTranslatef(0, 0, -zoom_speed)

        glRotatef(0.25, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_pyramid(points[0], points[1], points[2], points[3], level - 1)

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
