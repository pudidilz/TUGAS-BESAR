    hits = pygame.sprite.groupcollide(ufo_group, playerbullet_group, False, True)
            for i in hits:
            self.count_hit2 +=1
            if self.count_hit2 == 30:
                expl_x = i.rect.x + 50
                expl_y = i.rect.y + 60
                explosion = Explosion(expl_x, expl_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = -200
                self.count_hit2 = 0
