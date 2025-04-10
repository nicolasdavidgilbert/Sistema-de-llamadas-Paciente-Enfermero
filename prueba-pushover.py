import requests
import time


USER = 'ui7zuhcejeynzdnw4cc7qfedj6cvnd'
TOKEN = 'aomxf28deq3iwza8qjkurzgjfgweb2'

pedido_id = 1
url_confirmacion = f"http://localhost:5000/confirmar?pedido={pedido_id}"

data = {
        "token": TOKEN,
        "user": USER,
        "title": "📦 Entrega pendiente",
        "message": f"🚪 Tocá el botón para confirmar la entrega del pedido #{pedido_id}",
        "url": url_confirmacion,
        "url_title": "✅ Confirmar entrega",
        "sound": "magic",
        "priority": 2,
        "retry": 60,
        "expire": 300
    }



requests.post("https://api.pushover.net/1/messages.json", data=data)

