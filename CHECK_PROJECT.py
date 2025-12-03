#!/usr/bin/env python3
"""
CHECKLIST DE VERIFICAÇÃO - Módulo predict.py
Validar que tudo foi criado e integrado corretamente
"""

import os
import sys
from pathlib import Path

def check_files():
    """Verificar se todos os arquivos foram criados"""
    base_path = Path("c:/Users/gabbr/Desktop/ml-cesar")
    fastapi_path = base_path / "fastapi"
    
    print("\n" + "="*70)
    print("CHECKLIST DE VERIFICAÇÃO - ARQUIVOS CRIADOS")
    print("="*70 + "\n")
    
    files_to_check = {
        "predict.py": fastapi_path / "predict.py",
        "example_predict.py": fastapi_path / "example_predict.py",
        "test_predict.py": fastapi_path / "test_predict.py",
        "PREDICT_DOCUMENTATION.md": fastapi_path / "PREDICT_DOCUMENTATION.md",
        "QUICK_START.py": fastapi_path / "QUICK_START.py",
        "main.py": fastapi_path / "main.py",
        "CHANGES_SUMMARY.md": base_path / "CHANGES_SUMMARY.md",
        "ANALISE_COMPLETA.md": base_path / "ANALISE_COMPLETA.md",
    }
    
    all_exist = True
    for name, path in files_to_check.items():
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {name:<35} ({size:,} bytes)")
        else:
            print(f"❌ {name:<35} NÃO ENCONTRADO")
            all_exist = False
    
    return all_exist

def check_main_py_integration():
    """Verificar se main.py foi atualizado corretamente"""
    print("\n" + "="*70)
    print("CHECKLIST - INTEGRAÇÃO NO main.py")
    print("="*70 + "\n")
    
    main_path = Path("c:/Users/gabbr/Desktop/ml-cesar/fastapi/main.py")
    
    if not main_path.exists():
        print("❌ main.py não encontrado!")
        return False
    
    with open(main_path, 'r') as f:
        content = f.read()
    
    checks = {
        "Import predict module": "from predict import HeartFailurePredictor, build_ensemble_model",
        "Import logging": "import logging",
        "Global predictor": "predictor = None",
        "Load predictor startup": "predictor = HeartFailurePredictor",
        "Use predictor.predict()": "predictor.predict(data.dict())",
    }
    
    all_ok = True
    for check_name, search_string in checks.items():
        if search_string in content:
            print(f"✅ {check_name:<30}")
        else:
            print(f"❌ {check_name:<30} NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok

def check_predict_py_structure():
    """Verificar estrutura de predict.py"""
    print("\n" + "="*70)
    print("CHECKLIST - ESTRUTURA DE predict.py")
    print("="*70 + "\n")
    
    predict_path = Path("c:/Users/gabbr/Desktop/ml-cesar/fastapi/predict.py")
    
    if not predict_path.exists():
        print("❌ predict.py não encontrado!")
        return False
    
    with open(predict_path, 'r') as f:
        content = f.read()
    
    classes_functions = {
        "Classe HeartFailurePredictor": "class HeartFailurePredictor",
        "Método __init__": "def __init__(self, model=None)",
        "Método prepare_data": "def prepare_data(self, data",
        "Método predict": "def predict(self, data",
        "Método predict_batch": "def predict_batch(self, data_list",
        "Método get_feature_importance": "def get_feature_importance",
        "Função build_ensemble_model": "def build_ensemble_model()",
        "Logging setup": "import logging",
        "Feature names": "feature_names = [",
    }
    
    all_ok = True
    for check_name, search_string in classes_functions.items():
        if search_string in content:
            print(f"✅ {check_name:<35}")
        else:
            print(f"❌ {check_name:<35} NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok

def check_documentation():
    """Verificar documentação"""
    print("\n" + "="*70)
    print("CHECKLIST - DOCUMENTAÇÃO")
    print("="*70 + "\n")
    
    docs = {
        "PREDICT_DOCUMENTATION.md": "c:/Users/gabbr/Desktop/ml-cesar/fastapi/PREDICT_DOCUMENTATION.md",
        "QUICK_START.py": "c:/Users/gabbr/Desktop/ml-cesar/fastapi/QUICK_START.py",
        "CHANGES_SUMMARY.md": "c:/Users/gabbr/Desktop/ml-cesar/CHANGES_SUMMARY.md",
        "ANALISE_COMPLETA.md": "c:/Users/gabbr/Desktop/ml-cesar/ANALISE_COMPLETA.md",
    }
    
    all_ok = True
    for doc_name, doc_path in docs.items():
        path = Path(doc_path)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {doc_name:<30} ({size:,} bytes)")
        else:
            print(f"❌ {doc_name:<30} NÃO ENCONTRADO")
            all_ok = False
    
    return all_ok

def check_python_syntax():
    """Verificar sintaxe Python dos arquivos criados"""
    print("\n" + "="*70)
    print("CHECKLIST - VALIDAÇÃO DE SINTAXE PYTHON")
    print("="*70 + "\n")
    
    files = [
        "c:/Users/gabbr/Desktop/ml-cesar/fastapi/predict.py",
        "c:/Users/gabbr/Desktop/ml-cesar/fastapi/main.py",
        "c:/Users/gabbr/Desktop/ml-cesar/fastapi/example_predict.py",
        "c:/Users/gabbr/Desktop/ml-cesar/fastapi/test_predict.py",
    ]
    
    all_ok = True
    for file_path in files:
        path = Path(file_path)
        if not path.exists():
            print(f"❌ {path.name:<35} NÃO ENCONTRADO")
            all_ok = False
            continue
        
        try:
            with open(path, 'r') as f:
                compile(f.read(), path.name, 'exec')
            print(f"✅ {path.name:<35} Sintaxe OK")
        except SyntaxError as e:
            print(f"❌ {path.name:<35} ERRO: {e}")
            all_ok = False
    
    return all_ok

def main():
    """Executar todos os checks"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "CHECKLIST DE VERIFICAÇÃO - PROJETO" + " "*19 + "║")
    print("╚" + "="*68 + "╝")
    
    results = {}
    
    results['files'] = check_files()
    results['integration'] = check_main_py_integration()
    results['structure'] = check_predict_py_structure()
    results['documentation'] = check_documentation()
    results['syntax'] = check_python_syntax()
    
    # Resumo Final
    print("\n" + "="*70)
    print("RESUMO FINAL")
    print("="*70 + "\n")
    
    checks_summary = {
        "Arquivos Criados": results['files'],
        "Integração main.py": results['integration'],
        "Estrutura predict.py": results['structure'],
        "Documentação": results['documentation'],
        "Sintaxe Python": results['syntax'],
    }
    
    for check_name, passed in checks_summary.items():
        status = "✅ PASSOU" if passed else "❌ FALHOU"
        print(f"{check_name:<30} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 TODOS OS CHECKS PASSARAM! Projeto pronto para usar!")
    else:
        print("⚠️  Alguns checks falharam. Verifique acima.")
    print("="*70 + "\n")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
