import pygame
import sys
import os

# Inicialización de Pygame
pygame.init()
pygame.font.init()

# Dimensiones de la pantalla
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mascota Virtual - IPET 249 Informática")
reloj = pygame.time.Clock()

# Paleta de Colores Institucionales IPET 249
BORDO = (128, 0, 32)
AMARILLO = (255, 215, 0)
ROJO = (220, 20, 60)
BLANCO = (255, 255, 255)
NEGRO = (20, 20, 20)
GRIS_OSCURO = (40, 40, 40)
VERDE_OK = (46, 204, 113)

# Fuentes
fuente_titulo = pygame.font.SysFont("arial", 22, bold=True)
fuente_texto = pygame.font.SysFont("arial", 16)
fuente_estado = pygame.font.SysFont("arial", 28, bold=True)

# Variables de Estado de la Mascota (0 a 100)
bateria = 100.0
codigo = 100.0
salud_bugs = 100.0

# Tasas de desgaste por segundo
DESGASTE_BATERIA = 1.5
DESGASTE_CODIGO = 2.0
DESGASTE_BUGS = 1.0

# Cargar imagen base si existe (firefox.jpeg)
imagen_mascota = None
if os.path.exists("firefox.jpeg"):
    try:
        imagen_original = pygame.image.load("firefox.jpeg")
        imagen_mascota = pygame.transform.scale(imagen_original, (200, 200))
    except Exception as e:
        print("No se pudo cargar la imagen:", e)

# Estructura de Botones
botones = [
    {"rect": pygame.Rect(80, 490, 180, 50), "texto": "1. Café (+Batería)", "tecla": pygame.K_1, "accion": "bateria"},
    {"rect": pygame.Rect(310, 490, 180, 50), "texto": "2. Programar (+Código)", "tecla": pygame.K_2, "accion": "codigo"},
    {"rect": pygame.Rect(540, 490, 180, 50), "texto": "3. Depurar (+Salud)", "tecla": pygame.K_3, "accion": "bugs"}
]

def dibujar_escudo(surface, x, y):
    """ Dibuja un emblema institucional representativo del IPET 249 """
    pygame.draw.rect(surface, AMARILLO, (x, y, 70, 70), border_radius=8)
    pygame.draw.rect(surface, BORDO, (x + 5, y + 5, 60, 60), border_radius=6)
    texto_escudo = fuente_texto.render("IPET", True, AMARILLO)
    texto_num = fuente_texto.render("249", True, BLANCO)
    surface.blit(texto_escudo, (x + 15, y + 12))
    surface.blit(texto_num, (x + 20, y + 35))

def dibujar_mascota_fallback(surface, x, y, estado):
    """ Dibuja un zorro tipo Firefox usando primitivas gráficas """
    # Cabeza/Cuerpo
    pygame.draw.circle(surface, (245, 124, 0), (x, y), 70) # Naranja Firefox
    pygame.draw.polygon(surface, (245, 124, 0), [(x - 60, y - 30), (x - 30, y - 90), (x - 10, y - 50)]) # Oreja Izq
    pygame.draw.polygon(surface, (245, 124, 0), [(x + 60, y - 30), (x + 30, y - 90), (x + 10, y - 50)]) # Oreja Der
    
    # Ojos según estado
    if estado == "TRISTE":
        pygame.draw.line(surface, NEGRO, (x - 30, y - 10), (x - 10, y), 4)
        pygame.draw.line(surface, NEGRO, (x + 10, y), (x + 30, y - 10), 4)
    else:
        pygame.draw.circle(surface, BLANCO, (x - 20, y - 10), 12)
        pygame.draw.circle(surface, BLANCO, (x + 20, y - 10), 12)
        pygame.draw.circle(surface, NEGRO, (x - 20, y - 10), 5)
        pygame.draw.circle(surface, NEGRO, (x + 20, y - 10), 5)

    # Hocico
    pygame.draw.polygon(surface, BLANCO, [(x - 25, y + 10), (x + 25, y + 10), (x, y + 35)])
    pygame.draw.circle(surface, NEGRO, (x, y + 20), 6)

    # Detalle informático: Auriculares Gamer
    pygame.draw.arc(surface, AMARILLO, (x - 75, y - 75, 150, 100), 0, 3.14, 8)
    pygame.draw.rect(surface, ROJO, (x - 80, y - 30, 15, 35), border_radius=4)
    pygame.draw.rect(surface, ROJO, (x + 65, y - 30, 15, 35), border_radius=4)

def dibujar_barra(surface, x, y, ancho, alto, valor, etiqueta):
    """ Dibuja barras de estado estilizadas """
    pygame.draw.rect(surface, GRIS_OSCURO, (x, y, ancho, alto), border_radius=5)
    ancho_actual = int((valor / 100.0) * ancho)
    color_barra = VERDE_OK if valor > 50 else (AMARILLO if valor > 20 else ROJO)
    if ancho_actual > 0:
        pygame.draw.rect(surface, color_barra, (x, y, ancho_actual, alto), border_radius=5)
    pygame.draw.rect(surface, BLANCO, (x, y, ancho, alto), 2, border_radius=5)
    
    txt = fuente_texto.render(f"{etiqueta}: {int(valor)}%", True, BLANCO)
    surface.blit(txt, (x + 10, y - 22))

# Loop principal
ejecutando = True
while ejecutando:
    dt = reloj.tick(60) / 1000.0  # Tiempo transcurrido en segundos

    # 1. Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_1:
                bateria = min(100.0, bateria + 25)
            elif evento.key == pygame.K_2:
                codigo = min(100.0, codigo + 20)
            elif evento.key == pygame.K_3:
                salud_bugs = min(100.0, salud_bugs + 30)

        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            pos_mouse = evento.pos
            for btn in botones:
                if btn["rect"].collidepoint(pos_mouse):
                    if btn["accion"] == "bateria":
                        bateria = min(100.0, bateria + 25)
                    elif btn["accion"] == "codigo":
                        codigo = min(100.0, codigo + 20)
                    elif btn["accion"] == "bugs":
                        salud_bugs = min(100.0, salud_bugs + 30)

    # 2. Actualización de Estados
    bateria = max(0.0, bateria - DESGASTE_BATERIA * dt)
    codigo = max(0.0, codigo - DESGASTE_CODIGO * dt)
    salud_bugs = max(0.0, salud_bugs - DESGASTE_BUGS * dt)

    promedio_estado = (bateria + codigo + salud_bugs) / 3.0
    estado_anim = "FELIZ" if promedio_estado > 40 else "TRISTE"

    # 3. Renderizado (Dibujado)
    pantalla.fill(BORDO)

    # Encabezado Institucional
    dibujar_escudo(pantalla, 30, 20)
    titulo = fuente_titulo.render("IPET N° 249 'Nicolás Copérnico' - Especialidad Informática", True, AMARILLO)
    subtitulo = fuente_texto.render("Mascota Virtual: Firefox Tech (Laboratorio de Aplicaciones II)", True, BLANCO)
    pantalla.blit(titulo, (110, 25))
    pantalla.blit(subtitulo, (110, 55))

    # Área del Personaje (Centro)
    pygame.draw.rect(pantalla, GRIS_OSCURO, (200, 110, 400, 250), border_radius=15)
    pygame.draw.rect(pantalla, AMARILLO, (200, 110, 400, 250), 3, border_radius=15)

    if imagen_mascota:
        pantalla.blit(imagen_mascota, (300, 135))
    else:
        dibujar_mascota_fallback(pantalla, 400, 220, estado_anim)

    txt_estado = fuente_estado.render(f"Estado: {estado_anim}", True, VERDE_OK if estado_anim == "FELIZ" else ROJO)
    pantalla.blit(txt_estado, (320, 320))

    # Barras de Estado
    dibujar_barra(pantalla, 80, 410, 200, 20, bateria, "Batería / Energía")
    dibujar_barra(pantalla, 300, 410, 200, 20, codigo, "Nivel de Código")
    dibujar_barra(pantalla, 520, 410, 200, 20, salud_bugs, "Sistema Sin Bugs")

    # Botones de Interacción
    for btn in botones:
        pygame.draw.rect(pantalla, ROJO, btn["rect"], border_radius=10)
        pygame.draw.rect(pantalla, AMARILLO, btn["rect"], 2, border_radius=10)
        txt_btn = fuente_texto.render(btn["texto"], True, BLANCO)
        rect_txt = txt_btn.get_rect(center=btn["rect"].center)
        pantalla.blit(txt_btn, rect_txt)

    pygame.display.flip()

pygame.quit()
sys.exit()