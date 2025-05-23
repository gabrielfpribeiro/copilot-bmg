


from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

activities = {
   "Clube de Xadrez": {
      "description": "Aprenda estratégias e participe de torneios de xadrez",
      "schedule": "Sextas, 15h30 - 17h",
      "max_participants": 12,
      "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
   },
   "Aula de Programação": {
      "description": "Aprenda fundamentos de programação e desenvolva projetos de software",
      "schedule": "Terças e quintas, 15h30 - 16h30",
      "max_participants": 20,
      "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
   },
   "Educação Física": {
      "description": "Educação física e atividades esportivas",
      "schedule": "Segundas, quartas e sextas, 14h - 15h",
      "max_participants": 30,
      "participants": ["john@mergington.edu", "olivia@mergington.edu"]
   },
   # Esportivas
   "Futebol": {
      "description": "Participe do time de futebol da escola e jogue campeonatos",
      "schedule": "Terças e quintas, 16h - 17h30",
      "max_participants": 22,
      "participants": ["lucas@mergington.edu"]
   },
   "Vôlei": {
      "description": "Treinos e jogos de vôlei para todos os níveis",
      "schedule": "Quartas, 15h - 16h30",
      "max_participants": 18,
      "participants": []
   },
   # Artísticas
   "Teatro": {
      "description": "Aulas de interpretação e produção de peças teatrais",
      "schedule": "Segundas e quartas, 16h - 17h",
      "max_participants": 15,
      "participants": ["ana@mergington.edu"]
   },
   "Clube de Artes": {
      "description": "Desenvolva suas habilidades em pintura, desenho e escultura",
      "schedule": "Sextas, 14h - 15h30",
      "max_participants": 20,
      "participants": []
   },
   # Intelectuais
   "Olimpíada de Matemática": {
      "description": "Prepare-se para olimpíadas de matemática com aulas e desafios",
      "schedule": "Terças, 17h - 18h",
      "max_participants": 25,
      "participants": ["bruno@mergington.edu"]
   },
   "Clube de Leitura": {
      "description": "Leitura e discussão de livros clássicos e contemporâneos",
      "schedule": "Quintas, 14h - 15h",
      "max_participants": 18,
      "participants": []
   }
}

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

@app.get("/activities")
def get_activities():
    return activities

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    activity = activities[activity_name]
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Estudante já inscrito nesta atividade")
    activity["participants"].append(email)
    return {"message": f"{email} inscrito(a) em {activity_name} com sucesso"}

@app.post("/activities/{activity_name}/remove")
def remove_participant(activity_name: str, email: str):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    activity = activities[activity_name]
    email_normalized = email.strip().lower()
    found = None
    for p in activity["participants"]:
        if p.strip().lower() == email_normalized:
            found = p
            break
    if not found:
        raise HTTPException(status_code=404, detail="Participante não encontrado nesta atividade")
    activity["participants"].remove(found)
    return {"message": f"{email} removido(a) de {activity_name} com sucesso"}
