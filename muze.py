"""
Şanlı Türkiye Sanal Müzesi - pygame sürümü (3D "raycasting" motoru)
Kurulum : pip install pygame
Çalıştır: python muze.py

Kontroller: W ileri | S geri | A sola | D sağa | fare ya da ok tuşları ile bak
            E eseri incele | L dil (TR/EN) | Esc kapat/çık
Fotoğraflar: ataturk.jpg, fatih.jpg, inonu.jpg dosyalarını bu dosyanın yanına koy.
"""
import math
import os
import sys

import pygame

W, H = 960, 600
RAYS = 480                    # 3D görüntünün yatay çözünürlüğü
COLW = W // RAYS
FOV = math.radians(66)
HERE = os.path.dirname(os.path.abspath(__file__))

HL = 12                       # salon uzunluğu (hücre)
MAPW = 9
NH = 4                        # 3 lider salonu + galeri
MAPH = HL * NH + 2
SPEED, TURN, MOUSE = 3.0, 2.2, 0.0025

HALLS = [
    dict(name=("Atatürk Salonu", "Atatürk Hall"), short="Atatürk",
         color=(226, 208, 170), img="ataturk.jpg", items=[
        ("1881", ("Selanik'te doğuş", "Born in Salonica"),
         ("Ali Rıza Efendi ile Zübeyde Hanım'ın oğlu olarak doğdu. Matematik öğretmeni Mustafa Efendi, başarısı nedeniyle ona “Kemal” adını verdi.",
          "Born to Ali Rıza Efendi and Zübeyde Hanım. His maths teacher Mustafa Efendi gave him the name “Kemal” for his success.")),
        ("1915", ("Çanakkale", "Gallipoli"),
         ("Anafartalar Grubu Komutanı olarak Arıburnu ve Conkbayırı'nda düşmanı durdurdu. Çanakkale Boğazı geçilemedi.",
          "As commander of the Anafartalar Group he held the enemy at Arıburnu and Conkbayırı. The Dardanelles was never forced.")),
        ("1919", ("Samsun'a çıkış", "Landing at Samsun"),
         ("19 Mayıs 1919'da Samsun'a ayak bastı. Amasya Genelgesi, Erzurum ve Sivas Kongreleri ile milli mücadele örgütlendi.",
          "He landed at Samsun on 19 May 1919. The Amasya Circular and the Erzurum and Sivas Congresses organised the national struggle.")),
        ("1920", ("TBMM açılıyor", "Opening of Parliament"),
         ("23 Nisan 1920'de Ankara'da Türkiye Büyük Millet Meclisi açıldı. Egemenlik millete verildi.",
          "The Grand National Assembly of Türkiye opened in Ankara on 23 April 1920. Sovereignty was given to the nation.")),
        ("1923", ("Cumhuriyet", "The Republic"),
         ("29 Ekim 1923'te Cumhuriyet ilan edildi, Atatürk ilk Cumhurbaşkanı oldu. Sonra Harf İnkılabı (1928) ve kadınlara seçme ve seçilme hakkı (1934) geldi.",
          "The Republic was proclaimed on 29 October 1923 and Atatürk became its first President. The alphabet reform (1928) and women's right to vote and be elected (1934) followed.")),
    ]),
    dict(name=("Fatih Sultan Mehmet Salonu", "Fatih Sultan Mehmet Hall"), short="Fatih",
         color=(40, 120, 80), img="fatih.jpg", items=[
        ("1432", ("Edirne'de doğuş", "Born in Edirne"),
         ("30 Mart 1432'de Edirne'de doğdu. Akşemseddin ve Molla Gürani gibi hocalardan ders aldı. 1451'de tahta çıktı.",
          "Born in Edirne on 30 March 1432. He studied under teachers such as Akşemseddin and Molla Gürani and took the throne in 1451.")),
        ("1452", ("Rumeli Hisarı", "Rumeli Fortress"),
         ("İstanbul Boğazı'nın en dar yerine, kuşatma öncesinde kısa sürede yaptırıldı. Boğaz geçişini kontrol altına aldı.",
          "Built at the narrowest point of the Bosphorus in a short time before the siege, it controlled passage through the strait.")),
        ("Top", ("Büyük toplar", "The great cannons"),
         ("Macar usta Urban'ın döktüğü dev toplar, surları döverek kuşatmada belirleyici oldu.",
          "The giant cannons cast by the Hungarian founder Urban pounded the walls and were decisive in the siege.")),
        ("1453", ("Gemiler karadan", "Ships over land"),
         ("Nisan 1453'te gemiler Galata arkasından karadan çekilerek Haliç'e indirildi. Savunma şaşırdı.",
          "In April 1453 ships were hauled overland behind Galata into the Golden Horn. The defenders were caught off guard.")),
        ("1463", ("Hoşgörü", "Tolerance"),
         ("29 Mayıs 1453'te İstanbul fethedildi. 1463 tarihli Bosna Ahidnamesi dini özgürlük güvencesiyle bilinir. 1481'de vefat etti.",
          "Constantinople fell on 29 May 1453. The 1463 Bosnia charter is known for guaranteeing religious freedom. He died in 1481.")),
    ]),
    dict(name=("İsmet İnönü Salonu", "İsmet İnönü Hall"), short="İnönü",
         color=(60, 90, 150), img="inonu.jpg", items=[
        ("1884", ("İzmir'de doğuş", "Born in İzmir"),
         ("İzmir'de doğdu, askeri okullarda yetişti. Soyadını 1934'te İnönü Savaşları'nın anısına aldı.",
          "Born in İzmir and trained in military schools. He took his surname in 1934 in memory of the battles of İnönü.")),
        ("1921", ("I. İnönü", "First İnönü"),
         ("Ocak 1921'de Batı Cephesi Komutanı olarak düzenli ordunun ilk büyük başarısını kazandı.",
          "In January 1921, as commander of the Western Front, he won the first major success of the regular army.")),
        ("Mart", ("II. İnönü", "Second İnönü"),
         ("Mart sonu ve Nisan başında düşman bir kez daha geri püskürtüldü. Zafer Ankara'nın konumunu güçlendirdi.",
          "In late March and early April the enemy was driven back again. The victory strengthened Ankara's position.")),
        ("1923", ("Lozan", "Lausanne"),
         ("Başdelege olarak görüştü. 24 Temmuz 1923 antlaşması yeni Türkiye'nin bağımsızlığını uluslararası alanda kabul ettirdi.",
          "He led the talks as chief delegate. The treaty of 24 July 1923 won international recognition of Türkiye's independence.")),
        ("1938", ("İkinci Cumhurbaşkanı", "Second President"),
         ("1938-1950 arası Cumhurbaşkanlığı yaptı. Çok partili hayata geçişte rol oynadı, 1950'de iktidarı devretti. 25 Aralık 1973'te vefat etti.",
          "President from 1938 to 1950. He took part in the move to multi-party politics and handed over power in 1950. He died on 25 December 1973.")),
    ]),
    dict(name=("Galeri", "Gallery"), short="Galeri", color=(110, 40, 48), img=None, gallery=True, items=[]),
]

UI = {
    0: dict(title="Şanlı Türkiye Müzesi", hint="E: incele", help="W A S D yürü · fare bak · E incele · L English · G galeri · Esc çık",
            close="Kapat: E veya Esc"),
    1: dict(title="Glorious Türkiye Museum", hint="E: inspect", help="W A S D walk · mouse look · E inspect · L Türkçe · G gallery · Esc quit",
            close="Close: E or Esc"),
}


def hall_of(y):
    return min(NH - 1, max(0, (MAPH - 2 - int(y)) // HL))


def build_map():
    g = [[0] * MAPW for _ in range(MAPH)]
    for y in range(MAPH):
        for x in range(MAPW):
            if y in (0, MAPH - 1):
                g[y][x] = 5
            elif x in (0, MAPW - 1):
                g[y][x] = hall_of(y) + 1
    for i in range(NH - 1):               # salonları ayıran kemerler
        y = MAPH - 2 - HL * i - (HL - 1)
        for x in range(1, MAPW - 1):
            if not 3 <= x <= 5:
                g[y][x] = 6
    return g


def cast(g, px, py, rdx, rdy):
    """DDA ışın atma. (dik mesafe, yüz, hücre tipi) döndürür."""
    mx, my = int(px), int(py)
    ddx = abs(1 / rdx) if rdx else 1e30
    ddy = abs(1 / rdy) if rdy else 1e30
    if rdx < 0:
        sx, sdx = -1, (px - mx) * ddx
    else:
        sx, sdx = 1, (mx + 1 - px) * ddx
    if rdy < 0:
        sy, sdy = -1, (py - my) * ddy
    else:
        sy, sdy = 1, (my + 1 - py) * ddy
    side = 0
    for _ in range(80):
        if sdx < sdy:
            sdx += ddx
            mx += sx
            side = 0
        else:
            sdy += ddy
            my += sy
            side = 1
        if not (0 <= mx < MAPW and 0 <= my < MAPH):
            return 40.0, side, 5
        c = g[my][mx]
        if c:
            return (sdx - ddx if side == 0 else sdy - ddy), side, c
    return 40.0, side, 5


def free(g, blockers, x, y, r=0.22):
    for cx, cy in ((x - r, y - r), (x + r, y - r), (x - r, y + r), (x + r, y + r)):
        if not (0 <= int(cx) < MAPW and 0 <= int(cy) < MAPH) or g[int(cy)][int(cx)]:
            return False
    return all(math.hypot(x - bx, y - by) > br for bx, by, br in blockers)


def wrap(font, text, width):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if font.size(trial)[0] <= width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def make_exhibit_surface(font, year):
    s = pygame.Surface((120, 180), pygame.SRCALPHA)
    pygame.draw.rect(s, (110, 78, 48), (25, 100, 70, 80))
    pygame.draw.rect(s, (160, 120, 70), (20, 94, 80, 10))
    pygame.draw.circle(s, (240, 200, 90), (60, 62), 34)
    pygame.draw.circle(s, (255, 235, 150), (50, 50), 10)
    t = font.render(year, True, (60, 40, 20))
    s.blit(t, (60 - t.get_width() // 2, 108))
    return s


def make_portrait_surface(hall, big_font):
    path = os.path.join(HERE, hall["img"])
    pw, ph = 220, 280
    s = pygame.Surface((pw + 24, ph + 24 + 90), pygame.SRCALPHA)
    pygame.draw.rect(s, (184, 146, 63), (0, 0, pw + 24, ph + 24))
    inner = pygame.Surface((pw, ph))
    img = None
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert()
        except pygame.error:
            img = None
    if img:
        iw, ih = img.get_size()
        k = max(pw / iw, ph / ih)                     # kırparak doldur
        img = pygame.transform.smoothscale(img, (int(iw * k), int(ih * k)))
        inner.blit(img, ((pw - img.get_width()) // 2, (ph - img.get_height()) // 2))
    else:
        inner.fill((30, 22, 16))
        pygame.draw.circle(inner, (70, 54, 40), (pw // 2, 100), 48)
        pygame.draw.rect(inner, (70, 54, 40), (pw // 2 - 70, 150, 140, 130))
        t = big_font.render(hall["short"], True, (244, 236, 220))
        inner.blit(t, (pw // 2 - t.get_width() // 2, ph - 50))
    s.blit(inner, (12, 12))
    pygame.draw.rect(s, (110, 78, 48), ((pw + 24) // 2 - 8, ph + 24, 16, 90))
    return s


PW_, PH_ = 320, 256


def make_painting(n):
    """foto/fotoN.jpg dosyasını altın çerçeveli tabloya çevirir."""
    s = pygame.Surface((PW_, PH_))
    s.fill((184, 146, 63))
    pygame.draw.rect(s, (24, 18, 12), (14, 14, PW_ - 28, PH_ - 28))
    path = os.path.join(HERE, "foto", "foto%d.jpg" % n)
    if os.path.exists(path):
        try:
            img = pygame.image.load(path).convert()
            iw, ih = img.get_size()
            k = min((PW_ - 44) / iw, (PH_ - 44) / ih)
            img = pygame.transform.smoothscale(img, (max(1, int(iw * k)), max(1, int(ih * k))))
            s.blit(img, ((PW_ - img.get_width()) // 2, (PH_ - img.get_height()) // 2))
        except pygame.error:
            pass
    return s


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Şanlı Türkiye Sanal Müzesi")
    clock = pygame.time.Clock()
    f_s = pygame.font.SysFont("arial", 16)
    f_m = pygame.font.SysFont("arial", 22)
    f_b = pygame.font.SysFont("arial", 30, bold=True)
    g = build_map()

    sprites, blockers = [], []
    for i, h in enumerate(HALLS):
        base = MAPH - 1 - HL * i
        if h.get("gallery"):
            continue
        for j, (year, title, desc) in enumerate(h["items"]):
            sprites.append(dict(x=1.7 if j % 2 == 0 else MAPW - 1.7, y=base - 1.5 - j * 2.0,
                                surf=make_exhibit_surface(f_s, year), scale=.55, info=(h, year, title, desc)))
        py_ = base - 6.5
        sprites.append(dict(x=MAPW / 2, y=py_, surf=make_portrait_surface(h, f_b), scale=.85, info=None))
        blockers.append((MAPW / 2, py_, .5))

    paintings = {}                                    # galeri tabloları
    slots = [(0, y) for y in (2, 4, 6, 8, 10)] + [(MAPW - 1, y) for y in (2, 4, 6, 8, 10)]
    for n, key in enumerate(slots[:9]):
        paintings[key] = make_painting(n + 1)

    found = sum(os.path.exists(os.path.join(HERE, "foto", "foto%d.jpg" % n)) for n in range(1, 10))
    print("Klasör:", HERE, "| bulunan foto:", found, "/ 9")

    sky = pygame.Surface((W, H))                      # tavan + zemin
    for y in range(H):
        if y < H // 2:
            k = 1 - y / (H / 2)
            col = (int(34 + 30 * k), int(26 + 24 * k), int(20 + 18 * k))
        else:
            k = (y - H / 2) / (H / 2)
            col = (int(70 + 80 * k), int(52 + 62 * k), int(36 + 44 * k))
        pygame.draw.line(sky, col, (0, y), (W, y))

    wallcol = {i + 1: h["color"] for i, h in enumerate(HALLS)}
    wallcol[6], wallcol[5] = (130, 92, 56), (30, 22, 16)

    px, py, ang = MAPW / 2, MAPH - 1.8, -math.pi / 2
    lang, modal = 0, None
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    pygame.mouse.get_rel()
    zbuf = [0.0] * RAYS
    frames = int(os.environ.get("MUZE_FRAMES", "0"))     # sadece test için

    while True:
        dt = min(clock.tick(60) / 1000, .05)
        near = None
        for sp in sprites:
            if sp["info"] and math.hypot(sp["x"] - px, sp["y"] - py) < 1.7:
                near = sp
                break
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    if modal:
                        modal = None
                    else:
                        return
                elif e.key == pygame.K_e:
                    modal = None if modal else (near["info"] if near else None)
                elif e.key == pygame.K_l:
                    lang = 1 - lang
                elif e.key == pygame.K_g:                        # galeriye ışınlan
                    px, py, ang = MAPW / 2, 7.5, math.pi
        rel = pygame.mouse.get_rel()[0]
        keys = pygame.key.get_pressed()
        if not modal:
            ang += rel * MOUSE + ((keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * TURN * dt)
            dx, dy = math.cos(ang), math.sin(ang)
            fwd = keys[pygame.K_w] - keys[pygame.K_s] + keys[pygame.K_UP] - keys[pygame.K_DOWN]
            strafe = keys[pygame.K_d] - keys[pygame.K_a]
            mvx = (dx * fwd - dy * strafe) * SPEED * dt
            mvy = (dy * fwd + dx * strafe) * SPEED * dt
            if free(g, blockers, px + mvx, py):
                px += mvx
            if free(g, blockers, px, py + mvy):
                py += mvy

        dx, dy = math.cos(ang), math.sin(ang)
        pl = math.tan(FOV / 2)
        plx, ply = -dy * pl, dx * pl
        screen.blit(sky, (0, 0))
        for r in range(RAYS):
            cam = 2 * r / RAYS - 1
            rdx, rdy = dx + plx * cam, dy + ply * cam
            dist, side, cell = cast(g, px, py, rdx, rdy)
            dist = max(dist, .05)
            zbuf[r] = dist
            hh = min(H * 4, int(H / dist))
            k = max(.25, 1 / (1 + dist * .1)) * (.78 if side else 1)
            c = tuple(int(v * k) for v in wallcol.get(cell, (90, 90, 90)))
            pygame.draw.rect(screen, c, (r * COLW, H // 2 - hh // 2, COLW, hh))
            if cell == 4 and side == 0 and hh < H * 3:          # galeri duvarındaki tablo
                hy = py + dist * rdy
                key = (0 if rdx < 0 else MAPW - 1, int(hy))
                if key in paintings:
                    fr = hy - int(hy)
                    u = fr if rdx > 0 else 1 - fr
                    strip = paintings[key].subsurface((min(PW_ - 1, int(u * PW_)), 0, 1, PH_))
                    screen.blit(pygame.transform.scale(strip, (COLW, max(1, int(hh * .8)))),
                                (r * COLW, H // 2 - hh // 2 + int(hh * .1)))

        inv = 1 / (plx * dy - dx * ply)
        order = sorted(sprites, key=lambda s: -((s["x"] - px) ** 2 + (s["y"] - py) ** 2))
        for sp in order:
            rx, ry = sp["x"] - px, sp["y"] - py
            tx = inv * (dy * rx - dx * ry)
            ty = inv * (-ply * rx + plx * ry)
            if ty < .35:
                continue
            wall_h = H / ty
            sh = int(wall_h * sp["scale"])
            sw = int(sh * sp["surf"].get_width() / sp["surf"].get_height())
            if sh < 4 or sh > H * 3:
                continue
            img = pygame.transform.scale(sp["surf"], (sw, sh))
            cx = int(W / 2 * (1 + tx / ty))
            left, top = cx - sw // 2, int(H / 2 + wall_h / 2 - sh)
            for x in range(max(0, left), min(W, left + sw), COLW):
                if ty < zbuf[min(RAYS - 1, x // COLW)]:
                    screen.blit(img, (x, top), (x - left, 0, COLW, sh))

        u = UI[lang]
        hn = HALLS[hall_of(py)]["name"][lang]
        screen.blit(f_b.render(u["title"], True, (244, 236, 220)), (16, 10))
        screen.blit(f_m.render(hn, True, (216, 180, 90)), (16, 48))
        screen.blit(f_s.render(u["help"], True, (230, 230, 230)), (16, H - 26))
        screen.blit(f_s.render("foto: %d/9" % found, True, (255, 220, 120)), (16, H - 48))
        for y in range(MAPH):                                   # mini harita
            for x in range(MAPW):
                if g[y][x]:
                    pygame.draw.rect(screen, (200, 190, 170), (W - 100 + x * 8, 12 + y * 3, 8, 3))
        pygame.draw.circle(screen, (230, 60, 60), (int(W - 100 + px * 8), int(12 + py * 3)), 3)
        if near and not modal:
            t = f_m.render(f"{u['hint']}  -  {near['info'][2][lang]}", True, (255, 255, 255))
            pygame.draw.rect(screen, (0, 0, 0), (W // 2 - t.get_width() // 2 - 10, H - 80, t.get_width() + 20, 36))
            screen.blit(t, (W // 2 - t.get_width() // 2, H - 74))
        if modal:
            h, year, title, desc = modal
            ov = pygame.Surface((W, H), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 170))
            screen.blit(ov, (0, 0))
            box = pygame.Rect(W // 2 - 300, H // 2 - 170, 600, 340)
            pygame.draw.rect(screen, (244, 236, 220), box)
            pygame.draw.rect(screen, (184, 146, 63), box, 6)
            screen.blit(f_b.render(title[lang], True, (124, 18, 25)), (box.x + 28, box.y + 24))
            screen.blit(f_s.render(f"{h['name'][lang]} · {year}", True, (110, 90, 70)), (box.x + 28, box.y + 66))
            for n, line in enumerate(wrap(f_m, desc[lang], box.w - 56)):
                screen.blit(f_m.render(line, True, (43, 26, 18)), (box.x + 28, box.y + 100 + n * 30))
            screen.blit(f_s.render(u["close"], True, (110, 90, 70)), (box.x + 28, box.bottom - 34))
        pygame.display.flip()

        if frames:
            frames -= 1
            if frames == 0:
                pygame.image.save(screen, os.path.join(HERE, "test.png"))
                return


if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()
