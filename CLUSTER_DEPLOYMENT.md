# Развертывание на Hackathon Cluster

## Учетные данные
- **Username:** team15
- **Password:** PGALSA36$xQaOg,nW8VB5z2WGpezWPP
- **Hosts:** 
  - 129.212.178.168:32605
  - 134.199.193.89:32605

## Шаг 1: Подготовка локально

### Создать архив для загрузки

```bash
# Windows (PowerShell)
Compress-Archive -Path flower_server,flower_client,output,scripts -DestinationPath federated_learning.zip

# Linux/Mac
tar -czf federated_learning.tar.gz flower_server/ flower_client/ output/ scripts/ --exclude="*.pyc" --exclude="__pycache__"
```

## Шаг 2: Подключение к кластеру

```bash
ssh team15@129.212.178.168 -p 32605
# или
ssh team15@134.199.193.89 -p 32605
```

При запросе пароля: `PGALSA36$xQaOg,nW8VB5z2WGpezWPP`

## Шаг 3: Загрузка файлов на кластер

### Вариант A: Используя SCP (из локального терминала)

```bash
# Загрузить архив
scp -P 32605 federated_learning.tar.gz team15@129.212.178.168:~/

# Или загрузить отдельные директории
scp -r -P 32605 flower_server team15@129.212.178.168:~/
scp -r -P 32605 flower_client team15@129.212.178.168:~/
scp -r -P 32605 output team15@129.212.178.168:~/
scp -r -P 32605 scripts team15@129.212.178.168:~/
```

### Вариант B: Используя Git (если код в репозитории)

```bash
# На кластере
cd ~
git clone <your-repo-url>
cd InsurancePrediction
```

## Шаг 4: Установка зависимостей

На кластере уже есть виртуальное окружение `hackathon-venv` или `hackathon-venv-cpu`.

Если нужно установить дополнительные пакеты:

```bash
# Активировать окружение (автоматически в submit-job.sh)
source ~/hackathon-venv/bin/activate  # для GPU
# или
source ~/hackathon-venv-cpu/bin/activate  # для CPU

# Установить зависимости
pip install -r flower_server/requirements.txt
pip install -r flower_client/requirements.txt
```

## Шаг 5: Запуск федеративного обучения

### Вариант 1: Используя submit-job.sh (рекомендуется)

Кластер использует Slurm для управления задачами. Скрипт `submit-job.sh` уже есть в домашней директории.

#### Запуск сервера:

```bash
cd ~
./submit-job.sh "python flower_server/server.py" --name flower-server --gpu
```

#### Запуск клиентов (в отдельных задачах):

```bash
# Клиент 1
./submit-job.sh "python flower_client/client.py --client-id 1 --server-address localhost:8080 --data-dir output" --name flower-client-1 --gpu

# Клиент 2
./submit-job.sh "python flower_client/client.py --client-id 2 --server-address localhost:8080 --data-dir output" --name flower-client-2 --gpu

# Клиент 3
./submit-job.sh "python flower_client/client.py --client-id 3 --server-address localhost:8080 --data-dir output" --name flower-client-3 --gpu
```

**Важно:** Если клиенты и сервер запускаются в разных задачах Slurm, они могут быть на разных узлах. В этом случае нужно использовать реальный IP адрес сервера вместо `localhost`.

### Вариант 2: Запуск в одной задаче (проще для тестирования)

Создайте скрипт `run_all.sh`:

```bash
#!/bin/bash
cd ~

# Экспорт переменных окружения
export SERVER_ADDRESS="0.0.0.0"
export SERVER_PORT="8080"
export NUM_ROUNDS="10"
export MIN_CLIENTS="3"
export LOCAL_EPOCHS="5"
export BATCH_SIZE="32"
export LEARNING_RATE="0.001"

# Запустить сервер в фоне
python flower_server/server.py &
SERVER_PID=$!

# Подождать запуска сервера
sleep 5

# Запустить клиентов в фоне
python flower_client/client.py --client-id 1 --server-address localhost:8080 --data-dir output &
python flower_client/client.py --client-id 2 --server-address localhost:8080 --data-dir output &
python flower_client/client.py --client-id 3 --server-address localhost:8080 --data-dir output &

# Ждать завершения
wait $SERVER_PID
```

Запустить через Slurm:

```bash
./submit-job.sh "bash run_all.sh" --name federated-learning --gpu
```

### Вариант 3: Использование Python скрипта run_federated_learning.py

```bash
./submit-job.sh "python scripts/run_federated_learning.py" --name federated-learning --gpu
```

## Шаг 6: Мониторинг выполнения

### Просмотр логов

```bash
# Список задач
squeue -u team15

# Просмотр логов задачи
cat ~/logs/job<ID>_<name>.out
tail -f ~/logs/job<ID>_<name>.out  # в реальном времени
```

### Проверка результатов

После завершения обучения модель будет сохранена в:

```bash
ls -lh ~/flower_server/models/
```

## Шаг 7: Тестирование модели

```bash
./submit-job.sh "python scripts/test_model.py" --name test-model --gpu
```

## Важные замечания

1. **Лимиты кластера:**
   - Максимум 4 параллельные задачи (2 GPU + 2 CPU)
   - Максимальное время выполнения: 15 минут
   - GPU: 1 GPU, 6 vCPUs, 120 GB RAM
   - CPU: 8 vCPUs, 46 GB RAM

2. **Сетевое взаимодействие:**
   - Если сервер и клиенты в разных задачах Slurm, используйте IP адрес узла сервера
   - Можно использовать `srun` для запуска на одном узле

3. **Оптимизация:**
   - Уменьшите `NUM_ROUNDS` если обучение занимает слишком много времени
   - Уменьшите `BATCH_SIZE` если не хватает памяти
   - Используйте CPU задачи если GPU недоступны

## Быстрая команда для запуска

```bash
# На кластере, в домашней директории
./submit-job.sh "python scripts/run_federated_learning.py" --name fl-training --gpu
```

## Устранение проблем

### Проблема: Клиенты не могут подключиться к серверу
**Решение:** Убедитесь, что сервер запущен первым и использует правильный адрес. Если задачи на разных узлах, используйте IP адрес узла сервера.

### Проблема: Задача завершается раньше времени
**Решение:** Уменьшите `NUM_ROUNDS` или `LOCAL_EPOCHS` чтобы уложиться в лимит 15 минут.

### Проблема: Недостаточно памяти
**Решение:** Уменьшите `BATCH_SIZE` или используйте CPU задачи.


