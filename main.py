import pygame
from OpenGL.raw.GLU import gluPerspective
from pygame.locals import *
from OpenGL.GL import *
from PIL import Image

vertices = [
    [1, 1, 1],
    [-1, -1, 1],
    [-1, 1, -1],
    [1, -1, -1]
]

edges = [
    [0, 1],
    [1, 2],
    [2, 0],
    [0, 3],
    [1, 3],
    [2, 3]
]


camera_distance = 5.0
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


def draw_triangles(level, v0, v1, v2):
    if level == 0:
        return

    glBegin(GL_TRIANGLES)
    glVertex3fv(v0, v1, v2)
    glVertex3fv(v1, v0, v2)
    glVertex3fv(v2, v1, v0)
    glVertex3fv(v0, v2, v1)
    glVertex3fv(v1, v2, v0)
    glVertex3fv(v2, v0, v1)
    glEnd()


def draw_tetrahedron():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

    level = 2

    mid01 = [(vertices[0][0] + vertices[1][0]) / 2, (vertices[0][1] + vertices[1][1]) / 2, (vertices[0][2] + vertices[1][2]) / 2]
    mid12 = [(vertices[1][0] + vertices[2][0]) / 2, (vertices[1][1] + vertices[2][1]) / 2, (vertices[1][2] + vertices[2][2]) / 2]
    mid20 = [(vertices[2][0] + vertices[0][0]) / 2, (vertices[2][1] + vertices[0][1]) / 2, (vertices[2][2] + vertices[0][2]) / 2]
    mid03 = [(vertices[0][0] + vertices[3][0]) / 2, (vertices[0][1] + vertices[3][1]) / 2, (vertices[0][2] + vertices[3][2]) / 2]
    mid13 = [(vertices[1][0] + vertices[3][0]) / 2, (vertices[1][1] + vertices[3][1]) / 2, (vertices[1][2] + vertices[3][2]) / 2]
    mid23 = [(vertices[2][0] + vertices[3][0]) / 2, (vertices[2][1] + vertices[3][1]) / 2, (vertices[2][2] + vertices[3][2]) / 2]

    draw_triangles(level, mid01, mid12, mid20)
    draw_triangles(level, mid01, mid03, mid13)
    draw_triangles(level, mid20, mid03, mid23)
    draw_triangles(level, mid12, mid13, mid23)


def change_texture(state):
    if state:
        glDisable(GL_TEXTURE_2D)
        #glDisable(GL_CULL_FACE)
    else:
        glEnable(GL_TEXTURE_2D)
        #glEnable(GL_CULL_FACE)
        glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


def main():
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
        draw_tetrahedron()
        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    main()
