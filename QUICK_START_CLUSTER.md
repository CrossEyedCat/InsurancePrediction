# Быстрый запуск на Hackathon Cluster

## Шаг 1: Подготовка архива (локально)

```bash
# Windows PowerShell
cd "c:\Users\Admin\Ai projects\InsurancePrediction"
Compress-Archive -Path flower_server,flower_client,output,scripts -DestinationPath federated_learning.zip -Force

# Linux/Mac
cd ~/InsurancePrediction
tar -czf federated_learning.tar.gz flower_server/ flower_client/ output/ scripts/ --exclude="*.pyc" --exclude="__pycache__" --exclude="models/"
```

## Шаг 2: Загрузка на кластер

```bash
# Windows PowerShell
scp -P 32605 federated_learning.zip team15@129.212.178.168:~/

# Linux/Mac
scp -P 32605 federated_learning.tar.gz team15@129.212.178.168:~/
```

Пароль: `PGALSA36$xQaOg,nW8VB5z2WGpezWPP`

## Шаг 3: Подключение к кластеру

```bash
ssh team15@129.212.178.168 -p 32605
```

Пароль: `PGALSA36$xQaOg,nW8VB5z2WGpezWPP`

## Шаг 4: На кластере - распаковка и запуск

```bash
# Распаковать
cd ~
unzip federated_learning.zip  # или tar -xzf federated_learning.tar.gz

# Сделать скрипты исполняемыми
chmod +x scripts/*.sh

# Запустить федеративное обучение
./submit-job.sh "bash scripts/run_all_cluster.sh" --name federated-learning --gpu
```

## Шаг 5: Мониторинг

```bash
# Просмотр задач
squeue -u team15

# Просмотр логов (замените <ID> на ID задачи)
cat ~/logs/job<ID>_federated-learning.out
tail -f ~/logs/job<ID>_federated-learning.out
```

## Альтернативный способ (если первый не работает)

```bash
# На кластере
cd ~
./submit-job.sh "python scripts/run_federated_learning.py" --name fl-training --gpu
```

## Проверка результатов

После завершения:

```bash
# Проверить модели
ls -lh flower_server/models/

# Протестировать модель
./submit-job.sh "python scripts/test_model.py" --name test-model --gpu
```


