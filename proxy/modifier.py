import re

# this program replaces all of the newer css, js, html tags with older ones.
# If you encounter any issues, please open a issue at the issue tab. This is
# very likely to happen as I got all of the info about these tags from Chat-GPT
# and although I haven't encountered any issues I still wouldn't trust this info
# a 100%

def httpsoverwrite(url):
	if url[:7] == "http://":
		url = "https://" + url[7:]
	return url

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