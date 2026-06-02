from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import Response
from fastapi.responses import JSONResponse
import random
import string

router = APIRouter()

# Génère un code anonyme unique ex: Y4-482C
def generer_code():
    chiffres = str(random.randint(100, 999))
    lettre = random.choice(string.ascii_uppercase)
    return f"Y4-{chiffres}{lettre}"

# Les réponses du chatbot par langue
reponses = {
    "fr": {
        "accueil": "Bienvenue sur Y4thLink 🌿 Tes questions restent privées. Tape : info, rdv, clinique ou conseiller",
        "info": "📚 Sujets disponibles : contraception, grossesse, IST, violence. Tape le sujet qui t'intéresse.",
        "contraception": "La pilule se prend chaque jour à la même heure. Efficace à 99%. Tape 'rdv' pour prendre rendez-vous.",
        "grossesse": "Signes : absence de règles, nausées, fatigue. Consultation recommandée dès 8 semaines. Tape 'rdv'.",
        "rdv": f"🔐 Ton code privé : {generer_code()}. Montre ce code à la clinique. Aucun nom enregistré.",
        "clinique": "📍 CS Akpakpa — Cotonou\n📍 CSCOM Gbégamey — Cotonou\n📍 CS Godomey — Abomey-Calavi",
        "conseiller": "🟢 Adjoavi K. est disponible. Temps d'attente : 3 min. Ta conversation est confidentielle.",
    },
    "en": {
        "accueil": "Welcome to Y4thLink 🌿 Your questions stay private. Type: info, appointment, clinic or counselor",
        "info": "📚 Available topics: contraception, pregnancy, STI, violence. Type the topic you want.",
        "contraception": "The pill must be taken every day at the same time. 99% effective. Type 'appointment' to book.",
        "pregnancy": "Signs: missed period, nausea, fatigue. Consultation recommended from week 8. Type 'appointment'.",
        "appointment": f"🔐 Your private code: {generer_code()}. Show this code at the clinic. No name stored.",
        "clinic": "📍 CS Akpakpa — Cotonou\n📍 CSCOM Gbégamey — Cotonou\n📍 CS Godomey — Abomey-Calavi",
        "counselor": "🟢 Adjoavi K. is available. Wait time: 3 min. Your conversation is confidential.",
    }
}

@router.get("/chat")
def chat(message: str, langue: str = "fr"):
    msg = message.lower().strip()
    lang = reponses.get(langue, reponses["fr"])

    if msg in ["bonjour", "salut", "hello", "hi", "start"]:
        reponse = lang["accueil"]
    elif msg == "info":
        reponse = lang["info"]
    elif msg in ["contraception", "pilule"]:
        reponse = lang.get("contraception", lang["info"])
    elif msg in ["grossesse", "pregnancy"]:
        reponse = lang.get("grossesse", lang.get("pregnancy", lang["info"]))
    elif msg in ["rdv", "appointment"]:
        code = generer_code()
        reponse = f"🔐 Ton code privé : {code}. Montre ce code à la clinique. Aucun nom enregistré."
    elif msg in ["clinique", "clinic"]:
        reponse = lang["clinique"]
    elif msg in ["conseiller", "counselor"]:
        reponse = lang.get("conseiller", lang.get("counselor"))
    else:
        reponse = lang["accueil"]

    return JSONResponse(
        content={"reponse": reponse},
        media_type="application/json; charset=utf-8"
    )


@router.post("/whatsapp")
async def whatsapp(request: Request):
    try:
        form = await request.form()
        msg = form.get("Body", "bonjour").lower().strip()
        langue = "fr"
        if any(w in msg for w in ["hello", "hi", "appointment", "clinic", "counselor"]):
            langue = "en"
        lang = reponses.get(langue, reponses["fr"])
        if msg in ["bonjour", "salut", "hello", "hi", "start"]:
            reponse_texte = lang["accueil"]
        elif msg == "info":
            reponse_texte = lang["info"]
        elif msg in ["contraception", "pilule"]:
            reponse_texte = lang.get("contraception", lang["info"])
        elif msg in ["grossesse", "pregnancy"]:
            reponse_texte = lang.get("grossesse", lang.get("pregnancy", lang["info"]))
        elif msg in ["rdv", "appointment"]:
            code = generer_code()
            reponse_texte = f"Ton code prive : {code}. Montre ce code a la clinique. Aucun nom enregistre."
        elif msg in ["clinique", "clinic"]:
            reponse_texte = lang["clinique"]
        elif msg in ["conseiller", "counselor"]:
            reponse_texte = lang.get("conseiller", lang.get("counselor"))
        else:
            reponse_texte = lang["accueil"]

        xml = f"""

    
        {reponse_texte}
    
"""
        return Response(content=xml, media_type="text/xml")
    except Exception as e:
        xml = f"""

    
        Y4thLink disponible. Tape bonjour pour commencer.
    
"""
        return Response(content=xml, media_type="text/xml")
