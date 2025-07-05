import sys, pygame
from bullet import Bullet
from alien import Alien

def draw_dashed_line(screen, y_pos, color=(255, 0, 0), dash_length=10, gap=10):
    screen_width = screen.get_rect().width
    x = 0
    draw = True
    while x < screen_width:
        if draw:
            pygame.draw.line(screen, color, (x, y_pos), (x + dash_length, y_pos), 2)
        draw = not draw
        x += dash_length + gap

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button,
                 ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                              ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button,
                      ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)

def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    ai_settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True
    sb.prep_images()

    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        bullet = Bullet(ai_settings, screen, ship)
        bullets.add(bullet)

def update_bullets(ai_settings, screen, stats, sb,
                   ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb,
                                  ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(
        bullets, aliens, True, True)

    if collisions:
        for aliens_hit in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens_hit)
        sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2*alien_width
    return int(available_space_x / (2*alien_width))

def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height -
                         (3*alien_height) - ship_height)
    return int(available_space_y / (3*alien_height))

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)
    for row in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens,
                         alien_number, row)

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, screen, sb,
                        ship, aliens, bullets)

def ship_hit(ai_settings, stats, screen, sb,
             ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        pygame.time.delay(500)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb,
                        ship, aliens, bullets):
    boundary_y = int(ai_settings.screen_height * ai_settings.boundary_y_ratio)
    for alien in aliens.sprites():
        if alien.rect.bottom >= boundary_y:
            ship_hit(ai_settings, stats, screen, sb,
                     ship, aliens, bullets)
            break

def update_screen(ai_settings, screen, stats, sb, ship,
                  aliens, bullets, play_button, bg_image):
    screen.blit(bg_image, (0, 0))
    boundary_y = int(ai_settings.screen_height * ai_settings.boundary_y_ratio)
    draw_dashed_line(screen, boundary_y)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    sb.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()
