import sys
import random
import os
import pygame
from pygame.locals import *

# Inisialisasi semua modul pygame yang diperlukan
pygame.init()

# Mengatur agar jendela game berada di tengah layar secara otomatis jika dalam mode windowed
os.environ['SDL_VIDEO_CENTERED'] = '1'

'''ASSET GAMBAR'''
# Mendefinisikan nama file untuk aset gambar yang akan digunakan
player_ship = 'plyshp.png'
enemy_ship = 'enemyshp.png'
ufo_ship = 'ufoshp.png'
player_bullet = 'pbullet.png'
enemy_bullet = 'enemybullet.png'
ufo_bullet = 'ufobullet.png'

'''ASSET SUARA'''
# Memuat aset suara dan musik latar
# Pastikan file-file ini berada di direktori yang sama dengan script
laser_sound = pygame.mixer.Sound('laser.wav')
explosion_sound = pygame.mixer.Sound('expl sound.mp3')
game_over_sound = pygame.mixer.Sound('game_over.wav')
game_over_music = pygame.mixer.Sound('game over.mp3')
background_music = pygame.mixer.Sound('latar musik.mp3')

# Inisialisasi modul mixer pygame untuk memutar suara
pygame.mixer.init()

# Pengaturan default layar (mulai dengan mode Fullscreen)
fullscreen = True
screen = pygame.display.set_mode((0, 0), FULLSCREEN)
pygame.display.set_caption("AEROFIGHTER") # Judul jendela aplikasi
s_width, s_height = screen.get_size() # Mengambil ukuran lebar dan tinggi layar saat ini

# Pengaturan waktu dan Framerate
clock = pygame.time.Clock()
FPS = 60

# --- INISIALISASI SPRITE GROUPS ---
# Sprite group sangat berguna di Pygame untuk mengelola dan memperbarui banyak objek sekaligus (seperti peluru atau musuh)
bacground_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
ufo_group = pygame.sprite.Group()
playerbullet_group = pygame.sprite.Group()
enemybullet_group = pygame.sprite.Group()
ufobullet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()

# Grup utama yang menampung hampir semua sprite untuk dirender bersamaan
sprite_group = pygame.sprite.Group()

# Menyembunyikan kursor mouse saat berada di dalam layar game
pygame.mouse.set_visible(False)

def toggle_fullscreen():
    """Fungsi untuk beralih antara mode Fullscreen dan Windowed (Resolusi 1280x720)"""
    global screen
    global s_width
    global s_height
    global fullscreen

    fullscreen = not fullscreen

    if fullscreen:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((1280, 720))

    s_width, s_height = screen.get_size()

class Background(pygame.sprite.Sprite):
    """Kelas untuk membuat efek background bintang yang bergerak ke bawah"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([x,y])
        self.image.fill('white') # Warna kotak/bintang
        self.image.set_colorkey('black') # Membuat warna hitam menjadi transparan
        self.rect = self.image.get_rect()

    def update(self):
        # Menggerakkan background secara diagonal (kanan bawah)
        self.rect.y += 1
        self.rect.x += 1
        # Jika melewati batas bawah layar, reset posisi ke atas dengan lokasi X acak
        if self.rect.y > s_height:
            self.rect.y = random.randrange(-10, 0)
            self.rect.x = random.randrange(-400, s_width)

class Particle(Background):
    """Kelas untuk partikel tambahan (layer background kedua) yang bergerak lebih cepat"""
    def __init__(self, x, y):
        super().__init__(x,y)
        self.rect.x = random.randrange(0, s_width)
        self.rect.y = random.randrange(0, s_height)
        self.image.fill('grey')
        self.vel = random.randint(3,8) # Kecepatan jatuh acak agar terlihat dinamis

    def update(self):
        self.rect.y += self.vel
        # Jika melewati batas bawah layar, reset posisi secara acak
        if self.rect.y > s_height:
            self.rect.x = random.randrange(0, s_width) # Diperbaiki dari s_height ke s_width untuk X
            self.rect.y = random.randrange(-50, 0) # Mulai dari sedikit di luar layar atas

class player(pygame.sprite.Sprite):
    """Kelas untuk pesawat pemain yang dikontrol dengan mouse"""
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black') # Menghilangkan background hitam pada gambar pesawat
        self.alive = True
        self.count_to_live = 0
        self.activate_bullet = True
        self.alpha_duration = 0 # Digunakan untuk efek invincibility (kebal sementara) saat respawn

    def update(self):
        if self.alive:
            # Jika baru respawn, beri efek transparan dan invincibility (kebal) sementara
            self.image.set_alpha(80) 
            self.alpha_duration += 1
            if self.alpha_duration > 170:
                self.image.set_alpha(255) # Kembali solid setelah durasi tertentu
            
            # Posisi pesawat selalu mengikuti posisi mouse
            mouse = pygame.mouse.get_pos()
            self.rect.x = mouse[0] - 20
            self.rect.y = mouse[1] + 40
        else:
            # Logika saat pemain mati
            self.alpha_duration = 0
            expl_x = self.rect.x + 20
            expl_y = self.rect.y + 40
            explosion = Explosion(expl_x, expl_y)
            explosion_group.add(explosion)
            sprite_group.add(explosion)
            pygame.time.delay(22)
            
            # Sembunyikan pesawat di luar layar
            self.rect.y = s_height + 200 
            self.count_to_live += 1
            
            # Waktu jeda sebelum respawn kembali
            if self.count_to_live > 100:
                self.alive = True
                self.count_to_live = 0
                self.activate_bullet = True

    def shoot(self):
        """Fungsi untuk menembakkan peluru dari pemain"""
        if self.activate_bullet:   
            bullet = PlayerBullet(player_bullet)
            mouse = pygame.mouse.get_pos()
            bullet.rect.x = mouse[0]
            bullet.rect.y = mouse[1]
            playerbullet_group.add(bullet)
            sprite_group.add(bullet)

    def dead(self):
        """Dipanggil saat pemain terkena serangan musuh"""
        pygame.mixer.Sound.play(explosion_sound)
        self.alive = False
        self.activate_bullet = False
  
class Enemy(player):
    """Kelas untuk pesawat musuh biasa"""
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(80, s_width - 80)
        self.rect.y = random.randrange(-500, 0)
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        # Bergerak terus ke bawah
        self.rect.y += 1
        if self.rect.y > s_height:
            self.rect.x = random.randrange(0, s_width)
            self.rect.y = random.randrange(-2000, 0) # Loop kembali dari atas
        self.shoot()

    def shoot(self):
        # Musuh menembak HANYA saat berada di titik koordinat Y tertentu (pola tembakan statis)
        if self.rect.y in (0, 30, 90, 290, 300, 700):
            enemybullet = EnemyBullet(enemy_bullet)
            enemybullet.rect.x = self.rect.x
            enemybullet.rect.y = self.rect.y
            enemybullet_group.add(enemybullet)
            sprite_group.add(enemybullet)

class Ufo(Enemy):
    """Kelas untuk musuh tipe UFO yang bergerak ke kiri dan kanan di bagian atas layar"""
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = -200
        self.rect.y = 200
        self.move = 1 # Kecepatan dan arah gerak (1 = kanan, -1 = kiri)

    def update(self):
        self.rect.x += self.move
        # Memantul dari ujung ke ujung layar
        if self.rect.x > s_width + 200:
            self.move *= -1
        elif self.rect.x < -200:
            self.move *= -1
        self.shoot()

    def shoot(self):
        # UFO menembak berdasarkan posisi X nya secara konsisten
        if self.rect.x % 80 == 0:
            ufobullet = EnemyBullet(ufo_bullet)
            ufobullet.rect.x = self.rect.x + 50
            ufobullet.rect.y = self.rect.y + 60
            ufobullet_group.add(ufobullet)
            sprite_group.add(ufobullet)

class PlayerBullet(pygame.sprite.Sprite):
    """Kelas dasar peluru pemain"""
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')

    def update(self):
        self.rect.y -= 10 # Bergerak cepat ke atas
        if self.rect.y < 0:
            self.kill() # Hapus dari memori jika keluar batas atas layar

class EnemyBullet(PlayerBullet):
    """Kelas peluru musuh (mewarisi PlayerBullet tapi arah baliknya)"""
    def __init__(self, img):
        super().__init__(img)

    def update(self):
        self.rect.y += 3 # Bergerak ke bawah
        if self.rect.y > s_height:
            self.kill() # Hapus dari memori jika keluar batas bawah layar

class Explosion(pygame.sprite.Sprite):
    """Kelas untuk efek animasi ledakan berurutan"""
    def __init__(self, x, y):
        super().__init__()
        self.img_list = []
        # Memuat 5 frame gambar ledakan secara berurutan (exp1.png sampai exp5.png)
        for i in range(1,6):
            img = pygame.image.load(f'exp{i}.png').convert()
            img.set_colorkey('black')
            img = pygame.transform.scale(img, (120, 120))
            self.img_list.append(img)
            
        self.index = 0
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.count_delay = 0

    def update(self):
        # Mengatur kecepatan pergantian frame animasi ledakan
        self.count_delay += 1
        if self.count_delay >= 12:
            if self.index < len(self.img_list) - 1:
                self.count_delay = 0
                self.index += 1
                self.image = self.img_list[self.index]
        
        # Hapus objek jika animasi ledakan sudah selesai di frame terakhir
        if self.index >= len(self.img_list) - 1:
            if self.count_delay >= 12:
                self.kill()

class Game:
    """Kelas Utama yang mengatur jalannya Game, logika menu, dan sistem tabrakan (Collision)"""
    def __init__(self):
        self.count_hit = 0  # Health/HP dari musuh biasa
        self.count_hit2 = 0 # Health/HP dari musuh UFO
        self.lives = 3      # Nyawa pemain
        self.score = 0
        self.init_create = True
        self.game_over_sound_delay = 0

        self.run_game()

    def pause_text(self):
        # Menampilkan Teks Pause
        font = pygame.font.SysFont('calibri', 50)
        text = font.render('PAUSED', True, 'blue')
        text_rect = text.get_rect(center=(s_width/2, s_height/2))
        screen.blit(text, text_rect)

    def pause_screen(self):
        """Looping yang membekukan permainan saat tombol Space ditekan"""
        self.init_create = False
        while True:
            self.pause_text()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    # ALT + ENTER
                    if event.key == K_RETURN and (event.mod & pygame.KMOD_ALT):
                        toggle_fullscreen()
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_SPACE: # Tekan spasi lagi untuk lanjut
                        self.run_game()

            pygame.display.update()

    def game_over_text(self):
        # Menampilkan Teks Game Over
        font = pygame.font.SysFont('calibri', 50)
        text = font.render('GAME OVER', True, 'red')
        text_rect = text.get_rect(center=(s_width/2, s_height/2))
        screen.blit(text, text_rect)

    def game_over_screen(self):
        """Looping yang berjalan saat nyawa pemain habis"""
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(game_over_sound)
        while True:
            self.game_over_text()
            # Delay sebelum memutar musik game over
            self.game_over_sound_delay += 1
            if self.game_over_sound_delay > 2000:
                pygame.mixer.Sound.play(game_over_music)
                
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_RETURN and (event.mod & pygame.KMOD_ALT):
                        toggle_fullscreen()
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_SPACE:
                        # Tekan spasi untuk mereset dan mengulang game dari awal
                        sprite_group.empty()
                        enemy_group.empty()
                        playerbullet_group.empty()
                        ufo_group.empty()
                        explosion_group.empty()
                        pygame.mixer.Sound.stop(game_over_music)
                        self.__init__() # Panggil constructor ulang untuk reset state

            pygame.display.update()

    def tutorial_screen(self):
        """Menampilkan panduan bermain di awal secara bertahap (subtitle)"""
        tutorial_lines = [
            "PRESS Z TO SHOOT",
            "PRESS SPACE TO PAUSE",
            "PRESS ESC TO QUIT",
            "GET READY"
        ]

        font = pygame.font.SysFont('calibri', 40)
        current_line = 0
        timer = 0

        while True:
            screen.fill((0,0,0))

            # Render latar belakang, partikel, pemain, dan ledakan tanpa merender musuh
            bacground_group.draw(screen)
            bacground_group.update()
            particle_group.draw(screen)
            particle_group.update()
            player_group.draw(screen)
            player_group.update()
            playerbullet_group.draw(screen)
            playerbullet_group.update()
            explosion_group.draw(screen)
            explosion_group.update()

            # Render teks subtitle tutorial
            text = font.render(tutorial_lines[current_line], True, 'white')
            rect = text.get_rect(center=(s_width//2, s_height - 100))
            screen.blit(text, rect)

            pygame.display.update()
            clock.tick(FPS)

            timer += 1
            # Ubah teks setiap 3 detik (berdasarkan konversi FPS)
            if timer > FPS * 3:
                current_line += 1
                timer = 0

            # Jika tutorial selesai, keluar dari fungsi dan mulai game sebenarnya
            if current_line >= len(tutorial_lines):
                return

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_RETURN and (event.mod & pygame.KMOD_ALT):
                        toggle_fullscreen()
                    elif event.key == K_RETURN:
                        return # Skip tutorial langsung
                    elif event.key == K_z:
                        pygame.mixer.Sound.play(laser_sound)
                        self.player.shoot()
                    elif event.key == K_SPACE:
                        self.pause_screen()
                    elif event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    # --- FUNGSI SPAWNING (PEMBUATAN OBJEK) ---
    def create_background(self):
        for i in range(30):
            x = random.randint(1,8)
            background_image = Background(x,x)
            background_image.rect.x = random.randrange(0, s_width)
            background_image.rect.y = random.randrange(0, s_height)
            bacground_group.add(background_image)
            sprite_group.add(background_image)

    def create_particles(self):
        for i in range(60):
            x = 1
            y = random.randint(1,7)
            particle = Particle(x,y)
            particle_group.add(particle)
            sprite_group.add(particle)

    def create_player(self):
        self.player = player(player_ship)
        player_group.add(self.player)
        sprite_group.add(self.player)

    def create_enemy(self):
        for i in range(10):
            self.enemy = Enemy(enemy_ship)
            enemy_group.add(self.enemy)
            sprite_group.add(self.enemy)

    def create_ufo(self):
        for i in range(5):
            self.ufo = Ufo(ufo_ship)
            self.ufo.rect.x = -200 - (i * 300)
            ufo_group.add(self.ufo)
            sprite_group.add(self.ufo)

    # --- SISTEM DETEKSI TABRAKAN (COLLISION) ---
    
    def playerbullet_hits_enemy(self):
        """Deteksi jika peluru pemain mengenai musuh biasa"""
        # groupcollide mengecek tabrakan antara 2 grup sprite (Musuh dan Peluru)
        # False, True berarti Musuh tidak langsung hilang (False), tapi peluru langsung hilang (True)
        hits = pygame.sprite.groupcollide(enemy_group, playerbullet_group, False, True)
        for i in hits:
            self.count_hit += 1
            # Butuh 3 kali hit untuk membunuh musuh biasa
            if self.count_hit == 3:
                self.score += 10
                expl_x = i.rect.x + 20
                expl_y = i.rect.y + 40
                explosion = Explosion(expl_x, expl_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                # Respawn musuh jauh di atas layar
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-3000, -100)
                self.count_hit = 0
                pygame.mixer.Sound.play(explosion_sound)

    def playerbullet_hits_ufo(self):
        """Deteksi jika peluru pemain mengenai UFO"""
        hits = pygame.sprite.groupcollide(ufo_group, playerbullet_group, False, True)
        for i in hits:
            self.count_hit2 += 1
            # UFO lebih kuat, butuh 40 hit
            if self.count_hit2 == 40:
                self.score += 40
                expl_x = i.rect.x + 50
                expl_y = i.rect.y + 60
                explosion = Explosion(expl_x, expl_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = -199
                self.count_hit2 = 0
                pygame.mixer.Sound.play(explosion_sound)

    def enemybullet_hits_player(self):
        """Deteksi jika peluru musuh mengenai pemain"""
        # Pengecekan alpha == 255 memastikan pemain tidak kena tembak saat sedang kebal (respawning)
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, enemybullet_group, True)
            if hits:
                self.lives -= 1
                self.player.dead()
                if self.lives < 0: # Nyawa di bawah 0 (Habis)
                    self.game_over_screen()

    def ufobullet_hits_player(self):
        """Deteksi jika peluru UFO mengenai pemain"""
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, ufobullet_group, True)
            if hits:
                self.lives -= 1
                self.player.dead()
                if self.lives < 0:
                    self.game_over_screen()

    def player_enemy_crash(self):
        """Deteksi jika pemain menabrak badan musuh secara langsung"""
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, enemy_group, False)
            if hits:
                for i in hits:
                    # Reset musuh yang ditabrak
                    i.rect.x = random.randrange(0, s_width)
                    i.rect.y = random.randrange(-3000, -100)
                    self.lives -= 1
                    self.player.dead()
                    if self.lives < 0:
                        self.game_over_screen()

    def player_ufo_crash(self):
        """Deteksi jika pemain menabrak badan UFO secara langsung"""
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, ufo_group, False)
            if hits:
                for i in hits:
                    i.rect.x = -200
                    self.lives -= 1
                    self.player.dead()
                    if self.lives < 0:
                        self.game_over_screen()

    def create_lives(self):
        """Menggambar ikon indikator nyawa di sudut kiri bawah"""
        self.live_img = pygame.image.load(player_ship)
        self.live_img = pygame.transform.scale(self.live_img, (30, 30))
        n = 0
        for i in range(self.lives):
            screen.blit(self.live_img, (20+n , s_height - 60))
            n += 80

    def create_score(self):
        """Menggambar skor pemain di sudut kanan bawah"""
        score = self.score
        font = pygame.font.SysFont('calibri', 30)
        text = font.render("Score:"+str(score), True, 'green')
        text_rect = text.get_rect(topright=(s_width - 20, s_height- 60))
        screen.blit(text, text_rect)

    def run_update(self):
        """Membungkus logika rendering sprite utama"""
        sprite_group.draw(screen)
        sprite_group.update()

    def run_game(self):
        """Fungsi Loop Utama Game (Game Loop)"""
        pygame.mixer.music.load("latar musik.mp3")
        pygame.mixer.music.play(-1) # -1 berarti putar berulang-ulang tanpa batas (looping music)
        
        # Panggil pembuatan objek hanya sekali di awal
        if self.init_create:
            self.create_background()
            self.create_particles()
            self.create_player() 
            self.tutorial_screen() # Tampilkan tutorial SEBELUM musuh muncul
            self.create_enemy()
            self.create_ufo()
            
        while True:
            screen.fill((0, 0, 0)) # Bersihkan layar tiap frame
            
            # Cek semua kondisi interaksi dan tabrakan
            self.playerbullet_hits_enemy()
            self.playerbullet_hits_ufo()
            self.enemybullet_hits_player()
            self.ufobullet_hits_player()
            self.player_enemy_crash()
            self.player_ufo_crash()
            
            self.run_update() # Render & perbarui status semua sprite
            
            # Buat bar hitam di bawah untuk tempat skor dan nyawa
            pygame.draw.rect(screen, 'black', (0, s_height-70, s_width, 70)) 
            self.create_lives()
            self.create_score()

            # Event listener input keyboard & mouse
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == KEYDOWN:
                    if event.key == K_RETURN and (event.mod & pygame.KMOD_ALT):
                        toggle_fullscreen()

                    if event.key == K_z: # Tembak dengan tombol Z
                        pygame.mixer.Sound.play(laser_sound)
                        self.player.shoot()
                        
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

                    if event.key == K_SPACE: # Tombol Pause
                        self.pause_screen()

            pygame.display.update() # Update frame layar yang sudah digambar
            clock.tick(FPS)         # Batasi perulangan agar berjalan maksimal 60 Frame Per Second


def main():
    """Fungsi entri utama yang menginisiasi instance permainan"""
    game = Game()

# Perintah dasar Python untuk mengeksekusi block kode jika file ini dipanggil secara langsung
if __name__ == "__main__":
    main()
