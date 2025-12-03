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
- **csv file** Download the .csv file presented on this Git's root.

### 2. Clone/Access the Project

```bash
cd *LOCAL ON DRIVE*\ml-cesar
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

### Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **FastAPI** | http://localhost:8000 | - |
| **API Docs** | http://localhost:8000/docs | - |
| **MinIO Console** | http://localhost:9001 | admin / admin123 |
| **Jupyter Lab** | http://localhost:8890 | Token: admin123 |
| **MLflow** | http://localhost:5000 | - |
| **ThingsBoard** | http://localhost:8080 | sysadmin@thingsboard.org / sysadmin - tenant@thingsboard.org / tenant |

---
### How to use FastApi
  To start using the system, you need to access FastAPI at /enviarDados and upload the dataset for training.  

### How to use ThingsBoard
  After executing the container, the ThingsBoard Dashboard will be your home.  
  Inside the Dashboard you can send data strings as JSON values to the model by filling the boxes with the corresponding data types  
  The JSON files will be sent to the predictor, which will predict the target column "DEATH_EVENT"  
  After predicted, this data will be appended to the Postgres Database, and thus being used for future predictions.  
  Metrics will be updated on the graphics plottage inside the Dashboard , as Well as the graphs visualization. 
    
### Basic Docker Operations

#### Parar Containers (Preservando Dados)

```bash
docker compose stop
```

#### Restart Container

```bash
docker compose start
```

#### Logs

```bash
# FastAPI
docker logs fastapi -n 20

# ThingsBoard
docker logs thingsboard -n 20

# Todos os containers
docker logs --all
```

#### ML Model used on ThingsBoard

- **Synthethic Data Sampler**: SMOTE
- **Model**: RandomForestClassifier
- **Features**: 12 params
- **Target**: DEATH_EVENT (0 or 1)

#### Dataflow

```
[Dados do Paciente]
        ↓
   [FastAPI]
        ↓
   [Prediction]
        ↓
  [MinIO + PostgreSQL]
        ↓
    [ThingsBoard]
```

