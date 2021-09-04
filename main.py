import pygame as pg
from physics import *

pg.init()
pg.font.init()
screen = pg.display.set_mode((1280, 720))

clock = pg.time.Clock()

load_points('dots.txt')

right_pressed = False
left_pressed = False
simulation_mode = False

main_font = pg.font.Font(None, 50)
sim_mode_text = main_font.render('Simulation', True, (255, 255, 255), (50, 215, 65))
edit_mode_text = main_font.render('Editing', True, (255, 255, 255), (50, 130, 215))

target_point = None

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                right_pressed = True
            if event.button == 0:
                left_pressed = True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                right_pressed = False
                target_point = None
            if event.button == 0:
                left_pressed = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                simulation_mode = not simulation_mode
                set_points_to_default()

    screen.fill('black')

    if simulation_mode:
        screen.blit(sim_mode_text, (640 - sim_mode_text.get_width()//2, 0))
        cloth_update(clock.get_time() / 1000, target_point)
    else:
        screen.blit(edit_mode_text, (640 - edit_mode_text.get_width()//2, 0))

    pos = pg.mouse.get_pos()
    if right_pressed:
        if target_point:
            target_point.set_position(pos, not simulation_mode)
        else:
            target_point = find_point(pos, 5)
            if not target_point:
                create_point(pos)
    draw(screen)

    pg.display.update()
    clock.tick(60)
