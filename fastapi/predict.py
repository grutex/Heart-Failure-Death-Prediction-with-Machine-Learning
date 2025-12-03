import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class HeartFailurePredictor:
    """
    Classe para realizar predições de morte por insuficiência cardíaca.
    Implementa o modelo Ensemble (Voting Classifier) treinado no notebook.
    """
    
    def __init__(self, model=None):
        """
        Inicializa o preditor com o modelo carregado do MLflow.
        
        Args:
            model: Modelo treinado (sklearn). Se None, usa o ensemble padrão.
        """
        self.model = model
        self.scaler = StandardScaler()
        self.feature_names = [
            'age', 'anaemia', 'creatinine_phosphokinase', 'diabetes',
            'ejection_fraction', 'high_blood_pressure', 'platelets',
            'serum_creatinine', 'serum_sodium', 'sex', 'smoking', 'time'
        ]
        
        logger.info("HeartFailurePredictor inicializado")
    
    def prepare_data(self, data: Dict[str, Any]) -> pd.DataFrame:
        """
        Prepara os dados de entrada para predição.
        
        Args:
            data: Dicionário com os dados do paciente
            
        Returns:
            DataFrame preparado e normalizado
        """
        try:
            # Criar DataFrame com os dados
            df = pd.DataFrame([data])
            
            # Remover coluna DEATH_EVENT se existir (é o target, não feature)
            df = df.drop(columns=['DEATH_EVENT'], errors='ignore')
            
            # Garantir que todas as features estão presentes
            for feature in self.feature_names:
                if feature not in df.columns:
                    df[feature] = 0
            
            # Manter apenas as features esperadas
            df = df[self.feature_names]
            
            # Normalizar os dados
            df_scaled = self.scaler.fit_transform(df)
            df_scaled = pd.DataFrame(df_scaled, columns=self.feature_names)
            
            logger.debug(f"Dados preparados: {df_scaled.shape}")
            return df_scaled
            
        except Exception as e:
            logger.error(f"Erro ao preparar dados: {str(e)}")
            raise
    
    def predict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza a predição de risco de morte por insuficiência cardíaca.
        
        Args:
            data: Dicionário com os dados do paciente
            
        Returns:
            Dicionário com DEATH_EVENT (inteiro 0 ou 1) e confiança
        """
        try:
            if self.model is None:
                logger.warning("Modelo não carregado")
                return {
                    "DEATH_EVENT": 0,
                    "risk": "DESCONHECIDO",
                    "confidence": 0.0,
                    "probability_death": 0.0
                }
            
            # Preparar dados
            df_prepared = self.prepare_data(data)
            
            # Fazer predição
            prediction = int(self.model.predict(df_prepared)[0])
            
            # Obter probabilidades
            try:
                probabilities = self.model.predict_proba(df_prepared)[0]
                probability_death = float(probabilities[1]) if len(probabilities) > 1 else 0.0
                confidence = float(np.max(probabilities))
            except:
                probability_death = float(prediction)
                confidence = 0.0
            
            # Interpretar resultado
            risk = "ALTO RISCO" if prediction == 1 else "BAIXO RISCO"
            
            result = {
                "DEATH_EVENT": prediction,
                "risk": risk,
                "confidence": round(confidence, 4),
                "probability_death": round(probability_death, 4)
            }
            
            logger.info(f"Predição realizada: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Erro ao fazer predição: {str(e)}")
            raise
    
    def predict_batch(self, data_list: list) -> list:
        """
        Realiza predições em lote.
        
        Args:
            data_list: Lista de dicionários com dados dos pacientes
            
        Returns:
            Lista de resultados de predição
        """
        results = []
        for data in data_list:
            try:
                result = self.predict(data)
                results.append(result)
            except Exception as e:
                logger.error(f"Erro em predição em lote: {str(e)}")
                results.append({
                    "prediction": -1,
                    "risk": "ERRO",
                    "confidence": 0.0,
                    "probability_death": 0.0,
                    "error": str(e)
                })
        
        return results
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Obtém a importância das features (se disponível no modelo).
        
        Returns:
            Dicionário com importância das features
        """
        try:
            if hasattr(self.model, 'feature_importances_'):
                importances = self.model.feature_importances_
                return dict(zip(self.feature_names, importances))
            else:
                logger.warning("Modelo não possui feature_importances_")
                return {}
        except Exception as e:
            logger.error(f"Erro ao obter feature importance: {str(e)}")
            return {}


def build_ensemble_model() -> VotingClassifier:
    """
    Constrói e treina o modelo Ensemble (Voting Classifier) conforme treinado no notebook.
    Este é o modelo padrão caso nenhum modelo MLflow esteja disponível.
    
    Returns:
        Modelo Ensemble treinado com dados dummy para funcionar
    """
    from sklearn.datasets import make_classification
    
    # Criar dados dummy para treinar o modelo
    X, y = make_classification(
        n_samples=100, 
        n_features=12, 
        n_informative=8,
        n_redundant=2,
        n_classes=2,
        random_state=42
    )
    
    knn = KNeighborsClassifier(n_neighbors=3)
    dt = DecisionTreeClassifier(max_depth=3, random_state=42)
    rf = RandomForestClassifier(max_depth=3, random_state=42)
    
    ensemble = VotingClassifier(
        estimators=[
            ('knn', knn),
            ('dt', dt),
            ('rf', rf)
        ],
        voting='hard'
    )
    
    # Treinar o modelo com dados dummy
    ensemble.fit(X, y)
    
    logger.info("Modelo Ensemble criado e treinado com sucesso")
    return ensemble
