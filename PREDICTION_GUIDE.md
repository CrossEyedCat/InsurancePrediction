# Руководство по использованию системы предсказания

## Быстрый тест с примерами

Запустите скрипт с готовыми примерами:

```bash
python scripts/test_prediction_example.py
```

Или быстрый тест:

```bash
python scripts/quick_predict.py
```

## Интерактивное предсказание

Для предсказания стоимости страхования конкретного пациента:

```bash
python scripts/predict_insurance_cost.py --example
```

Или введите данные вручную:

```bash
python scripts/predict_insurance_cost.py
```

## Использование в коде

```python
from scripts.predict_utils import preprocess_patient_features
from flower_server.model import InsuranceCostModel
import torch

# Загрузить модель
model = InsuranceCostModel(input_size=17)
model.load_state_dict(torch.load('flower_server/models/active_model.pt'))
model.eval()

# Данные пациента
patient_data = {
    'age': 35,
    'sex': 'male',
    'number_of_dependents': 2,
    'region': 'southeast',
    'height_cm': 175.0,
    'weight_kg': 80.0,
    'bmi': 26.1,
    'systolic_bp': 125,
    'diastolic_bp': 82,
    'resting_heart_rate': 72,
    'smoking_status': 'never',
    'physical_activity_level': 'moderate',
    'total_cholesterol': 195.0,
    'glucose': 92.0,
}

# Предобработка
features = preprocess_patient_features(patient_data)

# Предсказание
with torch.no_grad():
    features_tensor = torch.FloatTensor(features).unsqueeze(0)
    prediction = model(features_tensor)
    insurance_cost = prediction.item()

print(f"Predicted insurance cost: ${insurance_cost:,.2f}")
```

## Требуемые поля

Обязательные поля:
- `age` или `date_of_birth` (для вычисления возраста)
- `sex` ('male' или 'female')
- `region` ('northeast', 'southeast', 'southwest', 'northwest')
- `smoking_status` ('never', 'current', 'former')
- `physical_activity_level` ('sedentary', 'light', 'moderate', 'active', 'very_active')

Рекомендуемые поля (будут использованы значения по умолчанию, если не указаны):
- `bmi`, `height_cm`, `weight_kg`
- `systolic_bp`, `diastolic_bp`, `resting_heart_rate`
- `total_cholesterol`, `glucose`
- `number_of_dependents`

## Примеры результатов

Система успешно делает предсказания:

1. **Молодой некурящий**: ~$12,500 (ниже среднего)
2. **Средний возраст, курящий**: ~$21,000 (выше среднего)
3. **Пожилой здоровый**: ~$17,300 (около среднего)

## Файлы

- `scripts/predict_insurance_cost.py` - полный интерактивный скрипт
- `scripts/test_prediction_example.py` - тест с примерами
- `scripts/quick_predict.py` - быстрый тест
- `scripts/predict_utils.py` - утилиты для предобработки

