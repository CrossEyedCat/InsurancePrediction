# Flower Federated Learning Setup

Система федеративного обучения для предсказания стоимости медицинского страхования с использованием Flower.ai.

## Архитектура

- **1 сервер агрегации** - агрегирует веса моделей от клиентов
- **3 клиента** - каждый клиент обучается на своей части данных (приблизительно 1/3 от 50,000 записей)

## Структура данных

Каждый клиент получает:
- **Клиент 1**: пациенты с ID 1-16,666 (~16,666 записей)
- **Клиент 2**: пациенты с ID 16,667-33,333 (~16,667 записей)
- **Клиент 3**: пациенты с ID 33,334-50,000 (~16,666 записей)

## Модель

Нейронная сеть с архитектурой:
- **Входной слой**: 17 признаков
  - Базовые: возраст, пол, BMI, количество детей, статус курения
  - Физические: рост, вес, систолическое АД, диастолическое АД, пульс
  - Здоровье: холестерин, глюкоза, уровень активности
  - Регион: one-hot encoding (4 региона)
- **Скрытые слои**: 256 → 128 → 64 → 32 нейронов
- **Выходной слой**: 1 нейрон (предсказание стоимости)

## Установка зависимостей

```bash
# Установить зависимости для сервера
pip install -r flower_server/requirements.txt

# Установить зависимости для клиента
pip install -r flower_client/requirements.txt
```

## Запуск системы

### Вариант 1: Автоматический запуск (рекомендуется)

Запускает сервер и всех клиентов автоматически:

```bash
# Windows
python scripts/run_federated_learning.py

# Linux/Mac
python3 scripts/run_federated_learning.py
```

### Вариант 2: Ручной запуск

#### Шаг 1: Запустить сервер

В первом терминале:

```bash
# Windows
scripts\start_server.bat

# Linux/Mac
chmod +x scripts/start_server.sh
./scripts/start_server.sh
```

Или напрямую:

```bash
python flower_server/server.py
```

#### Шаг 2: Запустить клиентов

В отдельных терминалах (по одному на клиента):

```bash
# Windows
scripts\start_client.bat 1
scripts\start_client.bat 2
scripts\start_client.bat 3

# Linux/Mac
chmod +x scripts/start_client.sh
./scripts/start_client.sh 1
./scripts/start_client.sh 2
./scripts/start_client.sh 3
```

Или напрямую:

```bash
python flower_client/client.py --client-id 1 --server-address localhost:8080
python flower_client/client.py --client-id 2 --server-address localhost:8080
python flower_client/client.py --client-id 3 --server-address localhost:8080
```

## Конфигурация

Настройки можно изменить через переменные окружения:

```bash
# Сервер
export SERVER_ADDRESS="0.0.0.0"
export SERVER_PORT="8080"
export NUM_ROUNDS="10"
export MIN_CLIENTS="3"
export FRACTION_FIT="1.0"
export FRACTION_EVALUATE="1.0"

# Клиент
export LOCAL_EPOCHS="5"
export BATCH_SIZE="32"
export LEARNING_RATE="0.001"
export FLOWER_SERVER_URL="localhost:8080"
```

## Процесс обучения

1. **Инициализация**: Сервер создает начальную модель с случайными весами
2. **Распределение**: Сервер отправляет текущие веса всем клиентам
3. **Локальное обучение**: Каждый клиент обучает модель на своих данных
4. **Агрегация**: Клиенты отправляют обновленные веса обратно на сервер
5. **Федеративная агрегация**: Сервер усредняет веса от всех клиентов (FedAvg)
6. **Сохранение**: Сервер сохраняет агрегированную модель
7. **Повторение**: Процесс повторяется для заданного количества раундов

## Результаты

После обучения:
- Модели сохраняются в `flower_server/models/`
- `active_model.pt` - финальная обученная модель
- `model_round_N.pt` - модели после каждого раунда

## Использование обученной модели

```python
import torch
from flower_server.model import InsuranceCostModel

# Загрузить модель
model = InsuranceCostModel(input_size=17)
model.load_state_dict(torch.load('flower_server/models/active_model.pt'))
model.eval()

# Предсказание (пример)
# features должны быть предобработаны так же, как в data_loader
features = torch.FloatTensor([...])  # 17 признаков
prediction = model(features)
insurance_cost = prediction.item()  # Восстановить из нормализованного значения
```

## Требования

- Python 3.8+
- PyTorch
- Flower (flwr)
- pandas
- numpy

## Устранение неполадок

### Клиенты не подключаются к серверу
- Убедитесь, что сервер запущен первым
- Проверьте адрес и порт сервера
- Проверьте, что порт 8080 не занят другим процессом

### Ошибки загрузки данных
- Убедитесь, что CSV файлы находятся в директории `output/`
- Проверьте, что файлы содержат необходимые колонки

### Проблемы с памятью
- Уменьшите `BATCH_SIZE`
- Уменьшите количество `LOCAL_EPOCHS`

## Дополнительная информация

- [Документация Flower](https://flower.ai/docs/framework/)
- [Tutorial по Flower](https://flower.ai/docs/framework/tutorial-quickstart-pytorch.html)


