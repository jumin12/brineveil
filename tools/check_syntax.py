from pathlib import Path

root = next(Path(r"C:\Users\andyp\Desktop\Desktop\games\games\game making\projects").glob("other*"))
html = (root / "bryans stuff" / "bryan rpg" / "index.html").read_text(encoding="utf-8")
start = html.find("<script>\n")
end = html.rfind("</script>")
script = html[start + len("<script>\n") : end]
out = Path(r"C:\Users\andyp\AppData\Local\Temp\brineveil-check.js")
out.write_text(script, encoding="utf-8")
print(out, len(script))
