# PIL1_2526_59 — IFRI MentorLink

<p align="center">
  <img src="static/img/IFRI MentorLink.png" alt="Logo IFRI MentorLink" width="120px"/>
</p>

<h3 align="center"><strong>Plateforme d'entraide académique</strong></h3>

<p align="center">
  Challenger et connecter les mentors et mentorés de l'Institut de Formation et de Recherche en Informatique (IFRI / UAC).
</p>

---

## 👤 Membre 1 — Intégrateur Principal

Ce projet a été entièrement refactorisé par le **Membre 1** pour garantir :
- ✅ Réactivité maximale (SocketIO temps réel)
- ✅ Cohérence base de données (Supabase avec retry automatique)
- ✅ Menu dashboard rétractable (toggle sidebar)
- ✅ Profil dynamique (masquage/affichage matières + ajout personnalisé)
- ✅ Matching enrichi (40+ matières informatiques)

---

## 📦 Stack Technique Finale

| Composant | Technologie |
|-----------|-------------|
| Backend | Flask 3 + Flask-SocketIO |
| Base de données | PostgreSQL (Supabase) |
| Temps réel | WebSocket (SocketIO) |
| Frontend | Bootstrap 5 + Jinja2 + JS natif |

---

## 🚀 Installation

```bash
git clone <url-du-repo>
cd Riri
pip install -r requirements.txt
python app.py