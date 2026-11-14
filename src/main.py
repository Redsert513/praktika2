"""
Модуль для разбора аргументов командной строки
и валидации параметров конфигурации.
"""
import argparse
import os
import sys
from urllib.parse import urlparse

VALID_IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.svg')


def create_parser():
    """
    Создает и настраивает парсер аргументов.
    """
    parser = argparse.ArgumentParser(
        description='Инструмент анализа зависимостей.'
    )
    parser.add_argument(
        '-p', '--package',
        required=True,
        help='Имя анализируемого пакета'
    )
    parser.add_argument(
        '-s', '--source',
        required=True,
        help='URL репозитория или путь к файлу'
    )
    parser.add_argument(
        '-t', '--test-mode',
        action='store_true',
        help='Режим работы с тестовым репозиторием'
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
    """
    Проверяет корректность переданных аргументов.
    """
    if args.depth <= 0:
        parser.error('Глубина анализа должна быть > 0')

    if args.test_mode:
        if not os.path.isfile(args.source):
            parser.error(
                f'Файл "{args.source}" не найден'
            )
    else:
        parsed = urlparse(args.source)
        if parsed.scheme not in ('http', 'https'):
            parser.error(
                f'Некорректный URL: "{args.source}"'
            )

    if not args.output.lower().endswith(VALID_IMAGE_EXTENSIONS):
        parser.error(
            f'Файл должен иметь расширение '
            f'{VALID_IMAGE_EXTENSIONS}'
        )


def print_config(args):
    """
    Выводит параметры в формате ключ-значение.
    """
    print('=== Конфигурация приложения ===')
    print(f'package   : {args.package}')
    print(f'source    : {args.source}')
    print(f'test_mode : {args.test_mode}')
    print(f'output    : {args.output}')
    print(f'depth     : {args.depth}')
    print('================================')


def main():
    """
    Точка входа в приложение.
    """
    parser = create_parser()
    args = parser.parse_args()
    validate_args(parser, args)
    print_config(args)


if __name__ == '__main__':
    main()
