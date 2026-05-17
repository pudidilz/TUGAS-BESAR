import pygame
import sys
import subprocess
import os

# Menginisialisasi modul pygame dan mixer untuk menangani suara/audio
pygame.init()
pygame.mixer.init()

'''SOUND'''
# Memuat efek suara yang akan diputar saat tombol menu disorot/diklik
tap_menu_sound = pygame.mixer.Sound('Tap Menu.mp3')

# Memusatkan jendela game secara otomatis di tengah layar saat dalam mode windowed
os.environ['SDL_VIDEO_CENTERED'] = '1'

def draw_button(screen, text, font, pos, default_color, hover_color):
    """
    Fungsi bantuan untuk menggambar teks yang bertindak sebagai tombol.
    Fungsi ini mendeteksi kursor, mengubah warna, dan menambahkan tanda ">" jika disorot.
    """
    mouse_pos = pygame.mouse.get_pos() # Mendapatkan posisi kursor mouse
    text_surf = font.render(text, True, default_color)
    text_rect = text_surf.get_rect(topleft=pos) # Membuat area hitbox untuk teks
    is_hovering = text_rect.collidepoint(mouse_pos) # Mengecek apakah mouse berada di atas teks

    # Mengubah warna teks menjadi warna 'hover' jika sedang disorot kursor
    color = hover_color if is_hovering else default_color
    text_surf = font.render(text, True, color)

    # Mengubah teks yang ditampilkan untuk menambahkan kursor panah "> "
    display_text = text
    if is_hovering:
        display_text = "> " + text

    # Merender dan menampilkan teks akhir ke layar
    text_surf = font.render(display_text, True, color)
    screen.blit(text_surf, pos)
    
    # Mengembalikan hitbox dan status hover untuk logika selanjutnya
    return text_rect, is_hovering

def main_menu():
    pygame.init()
    # Memuat dan memutar musik latar menu utama
    pygame.mixer.music.load("MainMenuTheme.mp3")
    pygame.mixer.music.play(-1) # Parameter -1 membuat musik berulang tanpa henti (loop)

    # --- Pengaturan Menu (Menu Settings) ---
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AEROFIGHTER")
    
    # Memuat gambar latar belakang dan menyesuaikannya dengan resolusi layar
    background = pygame.image.load("BackgroundMenu.png").convert()
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Menyesuaikan ukuran Font secara proporsional dengan lebar layar (WIDTH)
    font_size = int(WIDTH * 0.06)
    title_size = int(WIDTH * 0.09)
    font = pygame.font.SysFont("Courier New", font_size)
    title_font = pygame.font.SysFont("Courier New", title_size)
    
    # Pengaturan Warna (RGB)
    TEXT_COLOR = (255, 255, 255) # Putih
    
    # Menentukan posisi koordinat (X, Y) untuk tombol Play dan Quit
    play_pos = (WIDTH * 0.08, HEIGHT/2.5)
    quit_pos = (WIDTH * 0.08, HEIGHT/2)

    # Variabel Boolean untuk status loop dan untuk mencegah efek suara dimainkan berulang-ulang saat di-hover
    running = True
    fullscreen = False
    play_hovered = False
    quit_hovered = False
    
    # --- Main Loop (Perulangan Utama Menu) ---
    while running:
        # Menampilkan gambar latar belakang ke layar
        screen.blit(background, (0, 0))
        
        # Membuat lapisan transparansi (Overlay) menggunakan format SRCALPHA
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        # Warna overlay dalam format RGBA (Hitam, dengan tingkat transparansi 200)
        overlay_color = (0, 0, 0, 200) # Transparansi dari 0 - 255

        # Titik-titik koordinat untuk menggambar bidang poligon (untuk memberi efek visual potongan diagonal)
        cut_polygon = [
            (0, 0),             # Titik kiri atas
            (WIDTH/1.3, 0),     # Titik kanan atas
            (WIDTH/2, HEIGHT),  # Titik kanan bawah
            (0, HEIGHT)         # Titik kiri bawah
        ]

        # Menggambar garis batas (outline) untuk poligon tersebut
        pygame.draw.line(
            screen,
            (180, 60, 60),      # Warna RGB garis (Merah redup)
            (WIDTH/1.3, 0),     # Koordinat awal (X, Y)
            (WIDTH/2, HEIGHT),  # Koordinat akhir (X, Y)
            3                   # Ketebalan garis
        )

        # Menggambar area berbayang poligon pada overlay, lalu menempelkannya ke layar utama
        pygame.draw.polygon(overlay, overlay_color, cut_polygon)
        screen.blit(overlay, (0, 0))

        # Menggambar Judul Game (AEROFIGHTER)
        title_surf = title_font.render("AEROFIGHTER", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(topleft=(WIDTH * 0.08, HEIGHT / 4))
        screen.blit(title_surf, title_rect)
        
        # Menggambar Tombol dengan memanggil fungsi draw_button
        play_btn, _ = draw_button(
            screen,
            "PLAY",
            font,
            play_pos,
            TEXT_COLOR,
            (255, 60, 60) # Warna teks saat di-hover (Merah)
        )

        quit_btn, _ = draw_button(
            screen,
            "QUIT",
            font,
            quit_pos,
            TEXT_COLOR,
            (255, 60, 60)
        )
        
        mouse_pos = pygame.mouse.get_pos()

        # LOGIKA HOVER UNTUK TOMBOL PLAY (agar suara klik hanya berbunyi sekali saat disorot)
        if play_btn.collidepoint(mouse_pos):
            if not play_hovered:
                tap_menu_sound.play()
                play_hovered = True
        else:
            play_hovered = False


        # LOGIKA HOVER UNTUK TOMBOL QUIT
        if quit_btn.collidepoint(mouse_pos):
            if not quit_hovered:
                tap_menu_sound.play()
                quit_hovered = True
        else:
            quit_hovered = False

        # Memperbarui tampilan layar (Wajib dipanggil di akhir setiap frame)
        pygame.display.flip()
        
        # --- Penanganan Event (Event Handling) ---
        for event in pygame.event.get():
            # Event jika user mengklik tombol silang [X] di jendela aplikasi
            if event.type == pygame.QUIT:
                running = False
              
            # Event jika user menekan tombol di keyboard
            if event.type == pygame.KEYDOWN:
    
                # Pintasan ALT + ENTER untuk mengganti mode Layar Penuh (Fullscreen)
                if event.key == pygame.K_RETURN and (
                    event.mod & pygame.KMOD_ALT
                ):
                    fullscreen = not fullscreen # Membalik status fullscreen

                    if fullscreen:
                        # Masuk ke Fullscreen, resolusi (0,0) akan mengikuti resolusi bawaan monitor
                        screen = pygame.display.set_mode(
                            (0, 0),
                            pygame.FULLSCREEN
                        )
                    else:
                        # Kembali ke Windowed mode dengan ukuran 800x600
                        screen = pygame.display.set_mode(
                            (800, 600)
                        )

                    # Mengambil dimensi layar yang baru setelah perubahan mode
                    WIDTH, HEIGHT = screen.get_size()

                    # Menyesuaikan kembali ukuran font
                    font_size = int(WIDTH * 0.06)
                    title_size = int(WIDTH * 0.09)

                    font = pygame.font.SysFont(
                        "Courier New",
                        font_size
                    )

                    title_font = pygame.font.SysFont(
                        "Courier New",
                        title_size
                    )

                    # Menghitung ulang koordinat teks berdasarkan resolusi yang baru
                    play_pos = (WIDTH * 0.08, HEIGHT/2.5)
                    quit_pos = (WIDTH * 0.08, HEIGHT/2)

                    # Menyesuaikan kembali ukuran (scale) gambar latar belakang
                    background = pygame.image.load(
                        "BackgroundMenu.png"
                    ).convert()

                    background = pygame.transform.scale(
                        background,
                        (WIDTH, HEIGHT)
                    )  
                    
            # Event jika mouse diklik (button 1 = klik kiri)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                
                # JIKA TOMBOL PLAY DIKLIK
                if play_btn.collidepoint(event.pos):
                    pygame.mixer.Sound.play(tap_menu_sound)
                    
                    # 1. Keluar dari module pygame milik menu agar memori/layar/audio dilepaskan untuk game
                    pygame.quit()
                    
                    # 2. Menjalankan file game utama secara terpisah menggunakan subprocess
                    # Ganti "Test_1.py" dengan nama file game yang ingin dieksekusi!
                    subprocess.run([sys.executable, "Test_1.py"])
                    
                    # 3. Baris ini dieksekusi setelah game selesai/ditutup. 
                    # Memulai (init) ulang Pygame untuk mengembalikan tampilan menu utama
                    pygame.init()
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    pygame.display.set_caption("AEROFIGHTER")
                    pygame.mixer.music.load("MainMenuTheme.mp3")
                    pygame.mixer.music.play(-1)

                    # 4. Inisialisasi ulang font (Sangat penting agar program tidak crash setelah pygame.init ulang)
                    font = pygame.font.SysFont("Courier New", 48)
                    title_font = pygame.font.SysFont("Courier New", 72)
                
                # JIKA TOMBOL QUIT DIKLIK
                elif quit_btn.collidepoint(event.pos):
                    pygame.mixer.Sound.play(tap_menu_sound)
                    running = False # Menghentikan loop utama

    # Keluar dari pygame dan sistem saat perulangan 'running' bernilai False
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main_menu()
