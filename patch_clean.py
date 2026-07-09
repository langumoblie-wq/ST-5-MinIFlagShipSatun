import re

with open("src/App.tsx", "r") as f:
    content = f.read()

content = content.replace("import { initializeApp } from 'firebase/app';", "")
content = content.replace("import firebaseConfig from '../firebase-applet-config.json';", "")
content = content.replace("const app = initializeApp(firebaseConfig);", "")

with open("src/App.tsx", "w") as f:
    f.write(content)
