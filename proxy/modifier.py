import re


def urlmodifier(url):
        # this ensures the url starts always with https
        url = httpsoverwrite(url)
        # this redirects the old mojang server requests to a local server that requests the data from the modern mojang servers
        if url.startswith("https://www.minecraft.net/skin/") and url.endswith(".png"):
                url = "http://localhost:8081/mojang/skin?username=" + url[31:][:-4]

        
        # this redirects google traffic to my custom frontend
        elif url.startswith("https://www.google.") or url.startswith("https://google."):
                if len(url.split("/")) > 3:
                        url = "http://localhost:8081/google/" + url.split("/")[3]
                else:
                        url = "http://localhost:8081/google/"
        


        # this emulates the old old redirect system from microsoft (later replaced by fwLink, will also be handeld somewhere here)
        elif url.startswith("https://www.microsoft.com/isapi/redir.dll"):
                if "msnhome" in url:
                        # this redirects to msn like it used to in the 2000s
                        url = "http://localhost:8081/misc/redirto?page=msn.com"
                elif "ie5update" in url:
                        # this redirects to... idk what. Wayback machine doesn't have it archived, 
                        # but it says the redirect redirects to another redirect. Microsoft - Code Optimization at its best.
                        url = "http://localhost:8081/misc/redirto?page=go.microsoft.com/fwlink/?Linkid=72970&clcid=0x0409"
                elif "Support" in url and "printing" in url:
                        url = "http://localhost:8081/misc/redirto?page=support.microsoft.com/gp/printxp"
        


        # This handles all of the windowsmedia.com pages,
        elif url.startswith("https://windowsmedia.com/redir/services.asp"):
                # this redirects to the services page
                url  = "http://localhost:8081/windows/services"
        

        # This handles all of the orangewire.org pages, which is a parody site of LimeWire I made.
        elif url.startswith("https://orangewire.org"):
                url = url.replace("https://orangewire.org", "http://localhost:8081/orangewire")

        
        # Here comes the fwlink emulation, which i mentioned a few lines above
        # I will later also add the fwlinks for some other stuff like the rss widget in windows vista
        elif url.startswith("https://go.microsoft.com/fwlink"):
                if "LinkID=26247" in url:
                        # This is the link for Windows Movie Maker
                        url = "http://localhost:8081/misc/redirtohard?page=http://www.microsoft.com/windowsmedia/moviemaker/hostinfo/FTPInfoXPSPZ01en.dat"
        
        
        # This returns the Webhosting infos for Windows Movie Maker
        elif url == "https://www.microsoft.com/windowsmedia/moviemaker/hostinfo/FTPInfoXPSPZ01en.dat":
                url = "http://localhost:8081/windows/FTPInfoXPSPZ01en.dat"

        
        # This makes my custom Windows Update Continued site work
        elif url.startswith("https://www.windowsupdatecontinued.net"):
                url = url.replace("https://www.windowsupdatecontinued.net", "http://localhost:8081/wuc")

        elif url.startswith("https://windowsupdatecontinued.net"):
                url = url.replace("https://windowsupdatecontinued.net", "http://localhost:8081/wuc")


        # This redirects from the official (now defunct) microsoft update servers to my custom windows update continued server
        elif url == "https://fe2.update.microsoft.com":
                url = "http://localhost:8081/misc/redirtosoft?page=www.windowsupdatecontinued.net"

        # Windows Media codecs for Winamp
        elif url == "https://download.nullsoft.com/redist/wm/wmfdist95.exe":
                url = "http://web.archive.org/web/20220913063716if_/http://download.nullsoft.com/redist/wm/wmfdist95.exe" 

        # This gets the CRL from the new locaton
        elif url.lower() == "https://csc3-2004-crl.verisign.com/csc3-2004.crl":
                url = "http://crl.verisign.com/CSC3-2004.crl"
        
        # This redirects some ask.com file to a archived version, 
        # as ask.com doesn't host it anymore. For now at least, up until I understand what this file does. 
        # Then I can modify it to work better with this project.
        elif url.startswith("https://websearch.ask.com/installed"):
                url = "https://web.archive.org/web/20150311173432/http://websearch.ask.com:80/installed"

        # This redirects the old support page of Printing under Windows XP to my local copy of it, as the original page is gone.
        elif url == "https://support.microsoft.com/gp/printxp":
                url = "http://localhost:8081/windows/printxp"

        # Yet another redirect system from microsoft, this time from redir.windowsmedia.com. 
        # Couldn't you just use fwlink like a normal person microsoft?
        # Seriously, you guys keep things less straight than me during pride month.
        elif url.startswith("https://redir.windowsmedia.com"):
                if "?page=" in url:
                        url = "http://localhost:8081/misc/redirto?page=" + url.split("?page=")[1].replace("http://", "")

        return url

# Yes I know I could migrate this function to the one above, but I like the name to much.
def httpsoverwrite(url):
	if url[:7] == "http://":
		url = "https://" + url[7:]
	return url

# this program replaces all of the newer css, js, html tags with older ones.
# If you encounter any issues, please open a issue at the issue tab. This is
# very likely to happen as I got all of the info about these tags from Chat-GPT
# and although I haven't encountered any issues I still wouldn't trust this info
# a 1000%

def codemodifier(code):
        code = code.replace("https://", "http://")
        code = re.sub(r'\.([a-zA-Z0-9_-]+):([a-zA-Z0-9_-]+)', r'\1 {\2}', code)
        code = re.sub(r'flex', 'display: inline-block', code)
        code = re.sub(r'grid', 'display: table', code)
        code = re.sub(r'const|let', 'var', code)
        code = re.sub(r'Array.prototype.forEach', 'for (var i = 0; i < this.length; i++)', code)
        code = re.sub(r'Object.keys', 'for (var key in this)', code)
        code = re.sub(r'async|await', '', code)
        code = code.replace("<video ", "<iframe ")
        code = code.replace("</video>", "</iframe>")
        code = code.replace("<embed ", "<iframe ")
        code = code.replace("</embed>", "</iframe>")
        code = re.sub(r'data-', '', code)
        code = code.replace("var ", "let ")
        code = code.replace("function ", "function* ")
        code = code.replace("for (var i = 0; i < ", "for (let i = 0; i < ")
        code = code.replace("if (", "if (" + "!!")
        code = code.replace("console.log(", "console.log(" + "JSON.stringify(")
        code = code.replace("margin: 0 auto;", "margin: 0 auto; display: block;")
        code = code.replace("float: left;", "float: left; display: inline-block;")
        code = code.replace("clear: both;", "clear: both; display: block;")
        code = code.replace("<table>", "<div class='table'>")
        code = code.replace("<tr>", "<div class='table-row'>")
        code = code.replace("button { width: 100px; }", "button { width: 5rem; }")
        return code
