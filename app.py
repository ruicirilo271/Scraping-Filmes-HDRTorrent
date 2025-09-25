from flask import Flask, render_template, request, redirect
from bs4 import BeautifulSoup
import requests
from urllib.parse import quote

app = Flask(__name__)

HDR_URL = "https://hdrtorrent.com/filmes/"

# Função para buscar filmes
def buscar_filmes(query=None):
    url = HDR_URL
    if query:
        url += f"?s={quote(query)}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    filmes = []
    for div in soup.select(".capa-img"):
        try:
            link = div.find("a")["href"]
            img = div.find("img")["src"]
            titulo = div.find("h2").text.strip()
            tipo = div.find("span", class_="box_midia").text.strip()
            qualidade = div.find("span", class_="box_qual").text.strip()
            filmes.append({
                "link": link,
                "img": img,
                "titulo": titulo,
                "tipo": tipo,
                "qualidade": qualidade
            })
        except Exception:
            continue
    return filmes

# Rota principal
@app.route("/", methods=["GET", "POST"])
def index():
    query = request.args.get("query", "")
    filmes = buscar_filmes(query)
    return render_template("index.html", filmes=filmes, query=query)

# Rota detalhes
@app.route("/detalhes")
def detalhes():
    filme_url = request.args.get("url")
    if not filme_url:
        return redirect("/")

    response = requests.get(filme_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Título do filme
    titulo_tag = soup.find("h1")
    titulo = titulo_tag.text.strip() if titulo_tag else "Detalhes do Filme"

    # Imagem
    img_tag = soup.find("img")
    img = img_tag["src"] if img_tag else ""

    # Selecionar link magnet
    magnet_tag = soup.select_one("p.text-center a.btn-success.botao")
    torrent_link = magnet_tag["href"] if magnet_tag else filme_url

    return render_template("detalhes.html", titulo=titulo, img=img, torrent_link=torrent_link)

if __name__ == "__main__":
    app.run(debug=True)
