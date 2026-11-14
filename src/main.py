"""
Модуль для разбора аргументов командной строки
и валидации параметров конфигурации.
Вариант 11, Этапы 1-2.
"""
import argparse
import os
import sys
from urllib.parse import urlparse


VALID_IMAGE_EXTENSIONS = (
    '.png', '.jpg', '.jpeg', '.svg'
)


def create_parser():
    """Создает и настраивает парсер аргументов."""
    parser = argparse.ArgumentParser(
        description='Инструмент анализа '
                    'зависимостей Python.'
    )
    parser.add_argument(
        '-p', '--package',
        required=True,
        help='Имя анализируемого пакета'
    )
    parser.add_argument(
        '-s', '--source',
        required=True,
        help='URL PyPI или путь к JSON-файлу'
    )
    parser.add_argument(
        '-t', '--test-mode',
        action='store_true',
        help='Режим работы с тестовым '
             'репозиторием'
    )
    parser.add_argument(
        '-o', '--output',
        default='graph.png',
        help='Имя файла с изображением графа'
    )
    parser.add_argument(
        '-d', '--depth',
        type=int,
        default=3,
        help='Максимальная глубина анализа'
    )
    return parser


def validate_args(parser, args):
    """Проверяет корректность аргументов."""
    if args.depth <= 0:
        parser.error(
            'Глубина анализа должна быть > 0'
        )
    if args.test_mode:
        if not os.path.isfile(args.source):
            parser.error(
                f'Файл "{args.source}" '
                f'не найден'
            )
    else:
        parsed = urlparse(args.source)
        if parsed.scheme not in ('http', 'https'):
            parser.error(
                f'Некорректный URL: '
                f'"{args.source}"'
            )
    if not args.output.lower().endswith(
        VALID_IMAGE_EXTENSIONS
    ):
        parser.error(
            f'Файл должен иметь расширение '
            f'{VALID_IMAGE_EXTENSIONS}'
        )


def print_config(args):
    """Выводит параметры конфигурации."""
    print('=== Конфигурация приложения ===')
    print(f'package   : {args.package}')
    print(f'source    : {args.source}')
    print(f'test_mode : {args.test_mode}')
    print(f'output    : {args.output}')
    print(f'depth     : {args.depth}')
    print('================================')


def print_dependencies(deps, version):
    """
    Выводит список зависимостей на экран.
    :param deps: Список зависимостей.
    :param version: Версия пакета.
    """
    print(
        f'\nПрямые зависимости пакета '
        f'(версия {version}):'
    )
    if not deps:
        print('  (зависимости не найдены)')
        return
    for dep in deps:
        name = dep.get('name', '?')
        spec = dep.get('version_spec', '')
        if spec:
            print(f'  - {name} {spec}')
        else:
            print(f'  - {name}')


def main():
    """Точка входа в приложение."""
    parser = create_parser()
    args = parser.parse_args()
    validate_args(parser, args)
    print_config(args)

    try:
        from pypi import get_dependencies
        deps, version = get_dependencies(
            args.source,
            args.package,
            args.test_mode
        )
        print_dependencies(deps, version)
    except ValueError as e:
        print(f'Ошибка: {e}', file=sys.stderr)
        sys.exit(1)

    print('\nЭтап 2 успешно завершён.')


if __name__ == '__main__':
    main()
