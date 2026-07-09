import re

with open("src/lib/googleAuth.ts", "r") as f:
    content = f.read()

content = content.replace("let cachedAccessToken: string | null = null;", "let cachedAccessToken: string | null = sessionStorage.getItem('google_access_token');")
content = content.replace("cachedAccessToken = credential.accessToken;", "cachedAccessToken = credential.accessToken;\n    sessionStorage.setItem('google_access_token', cachedAccessToken);")
content = content.replace("cachedAccessToken = null;", "cachedAccessToken = null;\n      sessionStorage.removeItem('google_access_token');")

with open("src/lib/googleAuth.ts", "w") as f:
    f.write(content)
