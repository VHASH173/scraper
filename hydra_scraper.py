import os
import requests
import json

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

def scrape_repo_to_dataset(owner, repo, output_file="dataset_cerebro_hydra.jsonl"):
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    headers = {
        "User-Agent": "Hydra-Cognitive-Engine",
        "Authorization": f"Bearer {GITHUB_TOKEN}" if GITHUB_TOKEN else ""
    }
    
    print(f"🚀 Iniciando extracción masiva segura desde {owner}/{repo}...")
    
    # Usamos una cola en lugar de recursividad para evitar que Python colapse la memoria
    queue = [""]
    
    while queue:
        path = queue.pop(0)
        url = f"{api_url}/{path}" if path else api_url
        res = requests.get(url, headers=headers)
        
        if res.status_code != 200:
            print(f"⚠️ Alerta en ruta {path}: código {res.status_code}")
            continue
            
        try:
            items = res.json()
        except Exception:
            continue
            
        if not isinstance(items, list):
            continue
            
        for item in items:
            if item["type"] == "file" and item["name"].endswith((".ts", ".tsx", ".js", ".jsx", ".py", ".json")):
                code_res = requests.get(item["download_url"], headers=headers)
                if code_res.status_code == 200:
                    code_text = code_res.text
                    
                    entry = {
                        "instruction": f"Analiza la arquitectura y escribe la implementación limpia para el módulo {item['name']} enfocado en desarrollo full-stack.",
                        "input": f"Repositorio fuente: {owner}/{repo} | Ruta: {item['path']}",
                        "output": f"### Análisis Lógico:\n1. Desglose de dependencias y tipos requeridos para {item['name']}.\n2. Estructuración del flujo de datos y manejo de estados.\n\n### Implementación:\n```typescript\n{code_text}\n```"
                    }
                    
                    with open(output_file, "a", encoding="utf-8") as f:
                        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
                    print(f"🧠 Neurona extraída: {item['name']}")
                    
            elif item["type"] == "dir":
                queue.append(item["path"])

    print(f"✨ Lote guardado de {owner}/{repo}.")

repos_a_devorar = [
    ("facebook", "react-native"),
    ("vercel", "next.js"),
    ("expo", "expo"),
    ("supabase", "supabase"),
    ("tailwindlabs", "tailwindcss")
]

for owner, repo in repos_a_devorar:
    print(f"\n================ ATACANDO REPOSITORIO: {owner}/{repo} ================")
    scrape_repo_to_dataset(owner, repo, output_file="dataset_cerebro_hydra.jsonl")

print("\n🎉 ¡Listo! Todos los repositorios devorados sin errores de pila.")