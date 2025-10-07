from flask import Flask, jsonify, render_template, request, redirect
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# This handles minecraft skin requests from minecraft alpha
@app.route('/mojang/skin')
def mojang_skin():
    username = request.args.get('username')
    if not username:
        return jsonify({'error': 'Missing username parameter'}), 400

    # Here we send a request to a modern (but unofficial) api to request a skin
    req = requests.get(f'https://api.ashcon.app/mojang/v2/user/{username}')
    skin_url = req.json().get('textures', {}).get('skin', {}).get('url')
    if not skin_url:
        return jsonify({'error': 'Skin not found'}), 404

    response = requests.get(skin_url)

    return response.content, 200, {'Content-Type': 'image/png'}

# This is the landing page for the google frontend
@app.route('/google/')
def google():
    return render_template('google/index.html')

# This is one of the (probably many) miscellaneous helper endpoints. it just redirects to where you tell it to.
@app.route('/misc/redirto')
def redirto():
    page = request.args.get('page')
    if not page:
        return jsonify({'error': 'Missing page parameter'}), 400

    # This needs to be done with JS because sending a normal redirect makes everything look wierd and maybe causes problems down the line
    redir_page = "<html><head></head><body onLoad=\"window.location.href='http://{page}'\"></body></html>"

    return redir_page.format(page=page), 200, {'Content-Type': 'text/html'}

@app.route('/misc/redirtohard')
def redirect_hard():
    # This is the redirect that makes everything look wierd and maybe causes problems down the line
    page = request.args.get('page')
    return redirect(page)

# this just handles sending the google logo
@app.route('/google/logo.gif')
def google_logo():
    req = requests.get('http://www.google.de/intl/de_de/images/logo.gif')
    return req.content, 200, {'Content-Type': 'image/gif'}

# this also handles sending the google logo, but this time a different one
@app.route('/google/web_logo_left.gif')
def google_web_logo_left():
    req = requests.get('http://www.google.com/images/web_logo_left.gif')
    return req.content, 200, {'Content-Type': 'image/gif'}

# this is for the search results (trigger warning, I wrote this code while being tired and with the help of gpt)
@app.route('/google/search')
def google_search():
    query = request.args.get('q')

    # this is the chat-gpt part, i have no idea what it does but it works
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Encoding": "gzip, deflate"
    }
    response = requests.get(f"https://search.brave.com/search?q={query}", headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for item in soup.select("div.snippet"):
        title_elem = item.select_one("a")
        snippet_elem = item.select_one(".snippet-description")

        if title_elem:
            title = title_elem.get_text(strip=True)
            link = title_elem.get("href")
            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
            results.append({"title": title, "link": link, "snippet": snippet})
    
    # this is my part. It is absolutely gross and disgusting
    result_html = ""
    for r in results:
        # we check if a link is a search result or just a link to another brave page
        if r['link'].startswith("https://"):
            # here we get the link and the preview
            result_link = r['link']
            result_snippet = r['snippet']
            # here we generate a title because braves titles are formatted wierd and won't work correctly
            if len(result_link.split("/")[2].split(".")) > 2:
                # This just takes the Domain Name and makes the first letter capital. Same for the one below, just that that one does it for pages without a subdomaine
                result_title = result_link.split("/")[2].split(".")[1]
                result_title = result_title[0].upper() + result_title[1:]
            else:
                result_title = result_link.split("/")[2].split(".")[0]
                result_title = result_title[0].upper() + result_title[1:]
            # now we generate the results
            result_html += f'<br><a href="{result_link}"><h3>{result_title}</h3></a><p class="link">{result_link}</p><p class="snippet">{result_snippet}</p><br>'

    with open('templates/google/search.html') as file:
        # and finally return it and replace the placeholders with the actual content along the way.
        page = file.read()
        page = page.replace("searchquerygoeshere", query if query else "")
        page = page.replace("<!-- Search results go here-->", result_html)
    return page

@app.route('/windows/services')
def mediaplayer_premium_services():
    # Here we send my page of what the premium services could have looked like, 
    # because the wayback machine only has a version of the page when it was in beta. 
    # The design is based on that but I have no idea what it looked like unless somebody finds it. 
    # The closest thing I have of the finished page is what appears to be a screenshot in japanese, 
    # but I can't read japanese so I have no idea what it says.
    return render_template('templates/windows/services.html')
    

@app.route('/orangewire/<path:subpath>')
def orangewire(subpath):
    # here we return the logo of my LimeWire parody site called OrangeWire.
    # The logo is made by me and not stolen from anywhere.
    if subpath == "logo.png":
        with open('templates/misc/orangewire/logo.png', 'rb') as file:
            return file.read(), 200, {'Content-Type': 'image/png'}

@app.route('/orangewire/')
def orangewire_index():
    # Here we return a placeholder page for the OrangeWire site, as I haven't done the actual site yet and it is not very high on my priority list. 
    return "OrangeWire coming soon!"

@app.route('/windows/FTPInfoXPSPZ01en.dat')
def ftp_info():
    # This is a file needed for Windows Movie Maker, if you want to publish your movies online.
    # The file was really hard to find, as not even the wayback machine has the exact one, but I found a similar one.
    with open('templates/misc/FTPInfoEMP0409.dat', 'rb') as file:
        return file.read(), 200, {'Content-Type': 'application/octet-stream'}
    
@app.route('/wuc/')
def wuc():
    # This is my own Windows Update Website, called Windows Updates Continued.
    # I will publish new updates for Windows 95 to XP here.
    return render_template('windows/wuc/index.html')

@app.route('/wuc/<path:subpath>')
def wuc_subpath(subpath):
    # Here we return the different assets and subpages
    if subpath.endswith(".html"):
        # This handles all the html files
        return render_template(f'windows/wuc/{subpath}')
    if subpath.endswith(".gif"):
        # this handles all the gif files
        with open(f'templates/windows/wuc/{subpath}', "rb") as file:
            return file.read(), 200, {'Content-Type': 'image/gif'}
    if subpath.endswith(".png"):
        # and this handles all the png files
        with open(f'templates/windows/wuc/{subpath}', "rb") as file:
            return file.read(), 200, {'Content-Type': 'image/png'}

@app.route('/windows/printxp')
def print_xp():
    # This is my local copy of the old printing under windows xp support page, as the original one is gone.
    return render_template('windows/printxp.html')

app.run(host='localhost', port=8081)