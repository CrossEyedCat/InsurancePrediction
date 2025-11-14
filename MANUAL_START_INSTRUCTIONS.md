# Инструкция по ручному запуску федеративного обучения

Если автоматический запуск не работает, используйте этот метод:

## Способ 1: Запуск в отдельных окнах PowerShell

### Окно 1: Запуск сервера

```powershell
cd "c:\Users\Admin\Ai projects\InsurancePrediction"

$env:SERVER_ADDRESS = "localhost"
$env:SERVER_PORT = "8080"
$env:NUM_ROUNDS = "5"
$env:MIN_CLIENTS = "3"
$env:FRACTION_FIT = "1.0"
$env:FRACTION_EVALUATE = "1.0"
$env:MIN_AVAILABLE_CLIENTS = "3"
$env:LOCAL_EPOCHS = "3"
$env:BATCH_SIZE = "32"
$env:LEARNING_RATE = "0.001"

python flower_server\server.py
```

### Окно 2: Клиент 1

```powershell
cd "c:\Users\Admin\Ai projects\InsurancePrediction"

$env:FLOWER_SERVER_URL = "localhost:8080"
$env:LOCAL_EPOCHS = "3"
$env:BATCH_SIZE = "32"
$env:LEARNING_RATE = "0.001"

python flower_client\client.py --client-id 1 --server-address localhost:8080 --data-dir output
```

### Окно 3: Клиент 2

```powershell
cd "c:\Users\Admin\Ai projects\InsurancePrediction"

$env:FLOWER_SERVER_URL = "localhost:8080"
$env:LOCAL_EPOCHS = "3"
$env:BATCH_SIZE = "32"
$env:LEARNING_RATE = "0.001"

python flower_client\client.py --client-id 2 --server-address localhost:8080 --data-dir output
```

### Окно 4: Клиент 3

```powershell
cd "c:\Users\Admin\Ai projects\InsurancePrediction"

$env:FLOWER_SERVER_URL = "localhost:8080"
$env:LOCAL_EPOCHS = "3"
$env:BATCH_SIZE = "32"
$env:LEARNING_RATE = "0.001"

python flower_client\client.py --client-id 3 --server-address localhost:8080 --data-dir output
```

## Порядок запуска:

1. **Сначала** запустите сервер (Окно 1)
2. **Подождите 5-10 секунд** пока сервер инициализируется
3. **Затем** запустите все 3 клиента (Окна 2, 3, 4) - можно запускать одновременно

## Что должно произойти:

1. Сервер покажет: "Starting Flower server..." и будет ждать клиентов
2. Каждый клиент покажет: "Client X: Loaded data successfully" и подключится к серверу
3. Начнется обучение - вы увидите сообщения о раундах и метриках
4. После завершения сервер сохранит модели в `flower_server\models\`

## Проверка результатов:

После завершения обучения проверьте модели:

```powershell
Get-ChildItem flower_server\models\*.pt
```

Должны быть созданы файлы:
- `active_model.pt` - финальная модель
- `model_round_1.pt`, `model_round_2.pt`, и т.д. - модели после каждого раунда

## Устранение проблем:

### Клиенты не подключаются
- Убедитесь, что сервер запущен первым
- Проверьте, что порт 8080 не занят другим процессом
- Убедитесь, что все используют `localhost:8080`

### Ошибки загрузки данных
- Проверьте, что файлы CSV находятся в папке `output\`
- Убедитесь, что у вас есть права на чтение файлов

### Обучение слишком быстро завершается
- Увеличьте `NUM_ROUNDS` до 10 или больше
- Увеличьте `LOCAL_EPOCHS` до 5

