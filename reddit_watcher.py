import praw
import time
import requests
import traceback

# 🔐 Configura tus claves
REDDIT_CLIENT_ID = "ZQBaRpbyz5fBRyc95oEf1A"
REDDIT_CLIENT_SECRET = "FPzAxa7DLy8NCPktoB6TiNxShcJH4Q"
REDDIT_USER_AGENT = "vex-watcher by u/TU_USUARIO"

PUSHOVER_USER_KEY = "uo72zr61ujiyn41oe974o67srkvy1v"
PUSHOVER_API_TOKEN = "ancgu2ep9hwgn3qjqasrb7d5uedwcr"

# 🔧 Configuración: 1 = solo flair "identify", 0 = cualquier post
SOLO_IDENTIFY = 0

# 🧠 IDs de posts ya procesados
vistos = set()

# 📡 Conexión a Reddit
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

# 🔔 Función de notificación por Pushover
def notificar_pushover(titulo, mensaje):
    try:
        requests.post("https://api.pushover.net/1/messages.json", data={
            "token": PUSHOVER_API_TOKEN,
            "user": PUSHOVER_USER_KEY,
            "title": titulo,
            "message": mensaje
        })
    except Exception as e:
        print("⚠️ Error al enviar a Pushover:", e)

# ▶️ Bucle principal
modo = "solo flair 'identify'" if SOLO_IDENTIFY else "todos los posts nuevos"
print(f"🔍 Vigilando r/vexillology por {modo}...")

while True:
    try:
        subreddit = reddit.subreddit("vexillology")
        for post in subreddit.new(limit=10):
            flair = post.link_flair_text
            print(f"{post.title} → flair: {flair}")

            if post.id in vistos:
                continue

            if SOLO_IDENTIFY:
                if flair and "identify" in flair.lower():
                    vistos.add(post.id)
                    titulo = "📢 Nuevo post con flair 'identify'"
                    mensaje = f"{post.title}\n{post.url}"
                    print(f"\n{mensaje}")
                    notificar_pushover(titulo, mensaje)
            else:
                # Notificar cualquier post, con o sin flair
                vistos.add(post.id)
                flair_info = f" (flair: {flair})" if flair else ""
                titulo = "📢 Nuevo post en r/vexillology"
                mensaje = f"{post.title}{flair_info}\n{post.url}"
                print(f"\n{mensaje}")
                notificar_pushover(titulo, mensaje)

        print("⏱️ Esperando 30 segundos...")
        time.sleep(30)

    except Exception:
        print("⚠️ Error en el bucle principal:")
        traceback.print_exc()
        time.sleep(60)
