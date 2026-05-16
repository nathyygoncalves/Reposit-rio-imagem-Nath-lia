# settings.py – Configurações globais do jogo

# ── Janela ──────────────────────────────────────────────────────────────────
LARGURA  = 800
ALTURA   = 600
FPS      = 60
TITULO   = "Space Shooter – Estilo Atari"

# ── Cores (R, G, B) ─────────────────────────────────────────────────────────
PRETO       = (0,   0,   0)
BRANCO      = (255, 255, 255)
VERDE_NEON  = (57,  255, 20)
VERMELHO    = (255, 50,  50)
AMARELO     = (255, 220, 0)
CINZA       = (160, 160, 160)
AZUL_ESCURO = (5,   10,  30)

# ── Nave (Player) ────────────────────────────────────────────────────────────
NAVE_VELOCIDADE    = 5       # pixels por frame
NAVE_LARGURA       = 40
NAVE_ALTURA        = 30

# ── Projétil ─────────────────────────────────────────────────────────────────
PROJETIL_VELOCIDADE = 10
PROJETIL_LARGURA    = 4
PROJETIL_ALTURA     = 14
COOLDOWN_TIRO       = 300    # milissegundos entre tiros

# ── Asteroide ────────────────────────────────────────────────────────────────
ASTEROIDE_VELOCIDADE_MIN = 2
ASTEROIDE_VELOCIDADE_MAX = 5
ASTEROIDE_RAIO_MIN       = 18
ASTEROIDE_RAIO_MAX       = 38
INTERVALO_SPAWN          = 1200  # ms entre spawns (diminui com o tempo)
SPAWN_MINIMO             = 400   # intervalo mínimo de spawn

# ── Pontuação ────────────────────────────────────────────────────────────────
PONTOS_POR_ASTEROIDE = 10
