\# Dependency Graph Visualizer



\## Общее описание

Инструмент для анализа зависимостей пакетов NuGet.



\## Описание функций и настроек

\*\*Параметры командной строки:\*\*

\- `-p, --package` - имя анализируемого пакета (обязательно)

\- `-s, --source` - URL репозитория или путь к файлу (обязательно)

\- `-t, --test-mode` - режим работы с тестовым репозиторием

\- `-o, --output` - имя файла с изображением графа (по умолчанию: graph.png)

\- `-d, --depth` - максимальная глубина анализа (по умолчанию: 3)



\## Команды для сборки и запуска тестов

Запуск приложения:

```bash

.\\\\\\\\\\\\\\\\run.bat -p Newtonsoft.Json -s https://api.nuget.org/v3/index.json

"# Configur.p2" 
"# Configur.p2" 
"# Configur.p2" 

## Структура проекта



```text

my-shell/

├── src/

│   ├── \_\_init\_\_.py                # Делает папку src модулем Python

│   ├── pypi.py.py                 # работа с PyPI API

│   └── main.py                    # Главный файл

├── tests/

│   ├── \_\_init\_\_.py                # Делает папку tests модулем Python

│   ├── test\_pypi.bat  		    # тесты парсера PyPI

│   └── sample\_pypi.json          # тестовый JSON от PyPI

├── run.bat                        # Скрипт запуска для Windows

├── README.md                      # Документация проекта

└── .gitignore                     # Список файлов, игнорируемых Git

```

