# About
This project builds upon the work presented by **_Merlin Alex_** & **_Maheen Hasib_** in:  
["<ins>Prediction Of Heart Failure Patient Survival Using Machine Learning</ins>"](https://ojs.aaai.org/index.php/AAAI-SS/article/view/36050), using their methodology as a primary basis for our analysis and article.

<br/>


# Heart-Failure-Survival-Prediction-with-Machine-Learning
ML in Cardiology: turning data into a lifeline by predicting a heart failure survivability odds with precision and care.

<br/>

[Project's Chosen Dataset](https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records)  
[Project's Google Colabolatory](https://colab.research.google.com/drive/1uTj5PE84BZ8ZuCoFtqn3ZQ4cWv6C8s3q?authuser=2)  


<br/>

## **Colaborators & Github**  
  Roberto Almeida Burlamaque Catunda  -  @grutex  
  Gabriel Reis de Melo Pires  -  @13grmp  
  Joao Pedro Araújo  -  @joaopedrofds  
  Marina da Fonseca Frias de Siqueira Campos  -  @MarinaFFSC  
  David Ian Pereira Paula  -  @davidian19  

<br/>

## **Discipline & Institution**  
  Machine Learning - 2nd Semester of 2025 @ C.E.S.A.R School, Recife, Brazil

<br/>
 
## **How to Replicate and Execute (Step-by-Step)**

This guide provides step-by-step instructions to set up the environment, configure dependencies, and execute the code.


### 1. Prerequisites

- **Docker Desktop** installed (with Docker Compose)
- **Git** (optional)

### 2. Clone/Access the Project

```bash
cd c:\Users\gabbr\Desktop\ml-cesar
```

### 3. Start Everything

```bash
docker compose up -d
```

Wait 30-60 seconds for all services to start.

### 4. Check Status

```bash
docker ps
```

You should see 10 containers running: fastapi, postgres, minio, mlflow, jupyterlab, thingsboard, trendz, etc.

---

## Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **FastAPI** | http://localhost:8000 | - |
| **API Docs** | http://localhost:8000/docs | - |
| **MinIO Console** | http://localhost:9001 | admin / admin123 |
| **Jupyter Lab** | http://localhost:8890 | Token: admin123 |
| **MLflow** | http://localhost:5000 | - |
| **ThingsBoard** | http://localhost:8080 | sysadmin@thingsboard.org / sysadmin - tenant@thingsboard.org | tenant |

---

## ⚙️ Operações Básicas

### Parar Containers (Preservando Dados)

```bash
docker compose stop
```

### Reiniciar Containers

```bash
docker compose start
```

### Logs

```bash
# FastAPI
docker logs fastapi -n 20

# ThingsBoard
docker logs thingsboard -n 20

# Todos os containers
docker logs --all
```

## 📚 Documentação

### Estrutura do Projeto

```
ml-cesar/
├── fastapi/                    # API de Predição
│   ├── main.py                # FastAPI app
│   ├── predict.py             # Lógica de ML
│   └── requirements.txt
├── notebooks/                  # Jupyter Notebooks
│   └── heartFailureSurvivalPrediction.ipynb
├── docker-compose.yml         # Orquestração
├── README.md                  # Este arquivo
├── backup_databases.ps1       # Backup
├── restore_database.ps1       # Restore
└── configure_thingsboard.py   # Setup ThingsBoard
```

### Modelo de ML

- **Tipo**: Ensemble Voting Classifier
- **Modelos**: KNeighborsClassifier + DecisionTreeClassifier + RandomForestClassifier
- **Features**: 12 parâmetros clínicos
- **Target**: DEATH_EVENT (0 ou 1)

### Fluxo de Dados

```
[Dados do Paciente]
        ↓
   [FastAPI]
        ↓
   [Predição]
        ↓
  [MinIO + PostgreSQL]
        ↓
[ThingsBoard + Trendz]
```

---

## 🐛 Problemas Comuns

| Problema | Solução |
|----------|---------|
| API não responde | `docker logs fastapi` e `docker compose restart fastapi` |
| ThingsBoard não abre | Esperar 1-2 minutos, acessar http://localhost:8080 |
| Dados perdidos | Usar `docker compose stop` em vez de `down` |
| Espaço em disco | `docker system prune -a --volumes` |

---

## 📊 Containers Disponíveis

```bash
docker ps
```

Deve mostrar:
- ✅ fastapi (porta 8000)
- ✅ postgres (porta 5432)
- ✅ minio (porta 9000, 9001)
- ✅ mlflow (porta 5000)
- ✅ jupyterlab (porta 8890)
- ✅ thingsboard (porta 8080)
- ✅ trendz (porta 8888)
- ✅ trendz-postgres
- ✅ mlflow-serving

---

**Pronto para usar! 🚀**

