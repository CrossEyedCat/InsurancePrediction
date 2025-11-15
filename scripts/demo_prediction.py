"""
Демонстрация работы системы предсказания стоимости страхования
"""
import torch
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent / "flower_server"))
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from model import InsuranceCostModel
from predict_utils import preprocess_patient_features


def demo_prediction():
    """Демонстрация предсказания на примере запроса"""
    
    print("=" * 80)
    print("ДЕМОНСТРАЦИЯ СИСТЕМЫ ПРЕДСКАЗАНИЯ СТОИМОСТИ СТРАХОВАНИЯ")
    print("=" * 80)
    print()
    
    # Загрузка модели
    print("Шаг 1: Загрузка обученной модели...")
    possible_paths = [
        Path(__file__).parent.parent / "flower_server" / "models" / "active_model.pt",
        Path(__file__).parent.parent / "models" / "active_model.pt",
    ]
    
    model_path = None
    for path in possible_paths:
        if path.exists():
            model_path = path
            break
    
    if model_path is None:
        print("ОШИБКА: Модель не найдена!")
        print("Пожалуйста, сначала обучите модель с помощью start_training_v2.bat")
        return
    
    print(f"   Модель найдена: {model_path}")
    model = InsuranceCostModel(input_size=17)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    print("   Модель загружена успешно!")
    print()
    
    # Пример запроса
    print("Шаг 2: Получение данных пациента...")
    print("-" * 80)
    
    # Пример реального запроса
    patient_request = {
        'date_of_birth': '1988-03-15',  # ~36 лет
        'sex': 'male',
        'number_of_dependents': 1,
        'region': 'southeast',
        'height_cm': 178.0,
        'weight_kg': 85.0,
        'bmi': 26.8,
        'systolic_bp': 128,
        'diastolic_bp': 85,
        'resting_heart_rate': 75,
        'smoking_status': 'former',  # Бывший курильщик
        'physical_activity_level': 'moderate',
        'total_cholesterol': 205.0,
        'glucose': 95.0,
    }
    
    print("Входные данные:")
    for key, value in patient_request.items():
        print(f"   {key}: {value}")
    print()
    
    # Предобработка
    print("Шаг 3: Предобработка данных...")
    try:
        features = preprocess_patient_features(patient_request)
        print(f"   Извлечено признаков: {len(features)}")
        print(f"   Форма признаков: {features.shape}")
        print("   Предобработка завершена успешно!")
    except Exception as e:
        print(f"   ОШИБКА при предобработке: {e}")
        import traceback
        traceback.print_exc()
        return
    print()
    
    # Предсказание
    print("Шаг 4: Выполнение предсказания...")
    try:
        model.eval()
        with torch.no_grad():
            features_tensor = torch.FloatTensor(features).unsqueeze(0)
            prediction = model(features_tensor)
            predicted_cost = prediction.item()
        
        print(f"   Предсказание выполнено успешно!")
        print()
        
        # Результат
        print("=" * 80)
        print("РЕЗУЛЬТАТ ПРЕДСКАЗАНИЯ")
        print("=" * 80)
        print()
        print(f"   Предсказанная стоимость страхования: ${predicted_cost:,.2f}")
        print()
        
        # Сравнение со статистикой датасета
        try:
            import pandas as pd
            patients_df = pd.read_csv("output/patients.csv")
            avg_cost = patients_df['insurance_cost'].mean()
            median_cost = patients_df['insurance_cost'].median()
            min_cost = patients_df['insurance_cost'].min()
            max_cost = patients_df['insurance_cost'].max()
            
            print("Сравнение с датасетом:")
            print(f"   Средняя стоимость в датасете: ${avg_cost:,.2f}")
            print(f"   Медианная стоимость: ${median_cost:,.2f}")
            print(f"   Минимальная стоимость: ${min_cost:,.2f}")
            print(f"   Максимальная стоимость: ${max_cost:,.2f}")
            print()
            
            diff = predicted_cost - avg_cost
            pct_diff = (diff / avg_cost) * 100
            
            if predicted_cost < median_cost:
                status = "НИЖЕ МЕДИАНЫ"
                color_indicator = "(ниже)"
            elif predicted_cost > avg_cost * 1.2:
                status = "ВЫШЕ СРЕДНЕГО"
                color_indicator = "(выше)"
            else:
                status = "ОКОЛО СРЕДНЕГО"
                color_indicator = "(норма)"
            
            print(f"   Отклонение от среднего: ${diff:+,.2f} ({pct_diff:+.1f}%)")
            print(f"   Статус: {status} {color_indicator}")
            
        except Exception as e:
            print(f"   (Не удалось загрузить статистику датасета: {e})")
        
        print()
        print("=" * 80)
        print("Демонстрация завершена успешно!")
        print("=" * 80)
        
    except Exception as e:
        print(f"   ОШИБКА при предсказании: {e}")
        import traceback
        traceback.print_exc()
        return


if __name__ == "__main__":
    demo_prediction()

