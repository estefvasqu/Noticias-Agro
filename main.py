from flask import Flask
from datetime import datetime, timedelta
import feedparser
from urllib.parse import quote

app = Flask(__name__)

@app.route("/")
def noticias_agro():
    noticias_total = []

    ahora = datetime.now()
    hace_90_min = ahora - timedelta(minutes=90)

    # Términos de búsqueda por región
    keywords_ar = ['maíz', 'WASDE', 'FAO','trigo','fertilizantes','aceite de girasol','aceite de palma','USDA',
                   'soja', 'harina de soja', 'aceite de soja', 'granos', 'grano', 'campo','cereales','agroindustrial',
                   'cereal', 'agricultura', 'agro', 'agroindustria', 'agronomía', 'agrícola', 'agricultor/a',
                   'agricultor','agricultura', 'granja']

    keywords_us = ['corn', 'wheat', 'soybean', 'meal soybean', 'oil soybean', 'grains', 'grain', 'cereals', 'cereal',
                   'agriculture', 'agro', 'agribusiness', 'agronomy', 'agronomist', 'agricultural', 'agriculturist',
                   'farmer', 'farming', 'farm','sunflower','sunflowerseed', 'sunflower oil', 'palm oil']

    keywords_br = ['milho', 'trigo', 'soja' , 'farelo de soja', 'óleo de soja',  'grãos', 'grão', 'cereais',
                   'agricultura', 'agronomia']

    # Función auxiliar para buscar noticias
    def buscar_noticias(keywords, hl, gl, ceid):
        noticias = []
        for kw in keywords:
            url = f'https://news.google.com/rss/search?q={quote(kw)}&hl={hl}&gl={gl}&ceid={ceid}'
            feed = feedparser.parse(url)
            for entry in feed.entries:
                if hasattr(entry, 'published_parsed'):
                    fecha = datetime(*entry.published_parsed[:6])
                    if fecha >= hace_90_min:
                        noticias.append((fecha, entry.title))
        return noticias

    # Obtener noticias por país
    noticias_total += buscar_noticias(keywords_ar, 'es-419', 'AR', 'AR:es-419')
    noticias_total += buscar_noticias(keywords_us, 'en-US', 'US', 'US:en')
    noticias_total += buscar_noticias(keywords_br, 'pt-BR', 'BR', 'BR:pt-419')

    noticias_total = sorted(noticias_total, reverse=True)
    ultimas = noticias_total[:15]

    if ultimas:
        return "<br>".join([f"{n[0].strftime('%d/%m %H:%M')} - {n[1]}" for n in ultimas])
    else:
        return "No hay noticias nuevas en los últimos 90 minutos."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
