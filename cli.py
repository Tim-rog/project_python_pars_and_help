import argparse
from pathlib import Path
import subprocess
import sys


def build_parser():
    parser = argparse.ArgumentParser(
        description='Запуск бота и управление контейнерами проекта.',
    )
    parser.add_argument(
        '--project-dir', type=Path, default=Path(__file__).resolve().parent,
        help='Папка проекта; по умолчанию папка, где лежит cli.py.',
    )
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('up', help='Собрать и запустить контейнеры в фоне.')
    commands.add_parser('down', help='Остановить контейнеры проекта.')
    commands.add_parser('status', help='Показать состояние контейнеров.')
    commands.add_parser('check', help='Проверить конфигурацию Docker Compose.')
    logs = commands.add_parser('logs', help='Показать последние 100 строк логов.')
    logs.add_argument('-f', '--follow', action='store_true', help='Следить за новыми логами; выход — Ctrl+C.')
    return parser


def find_compose_file(project_dir):
    file_names = ['compose.yaml', 'compose.yml',
                  'docker-compose.yaml', 'docker-compose.yml']
    for name in file_names:
        file_path = project_dir / name
        if file_path.is_file():
            return file_path
    return None


def get_command_args(args):
    if args.command == 'up':
        return ['up', '-d', '--build', '--force-recreate',
                '--wait', '--wait-timeout', '180']
    elif args.command == 'down':
        return ['down']
    elif args.command == 'status':
        return ['ps', '--all']
    elif args.command == 'check':
        return ['config', '--quiet']
    elif args.command == 'logs':
        command_args = ['logs', '--tail', '100']
        if args.follow:
            command_args.append('--follow')
        return command_args


def main(argv=None):
    args = build_parser().parse_args(argv)
    project_dir = args.project_dir.resolve()
    compose_file = find_compose_file(project_dir)
    if compose_file is None:
        print('Не найден файл Docker Compose. Положите cli.py рядом с compose.yaml '
              'или укажите папку через --project-dir.', file=sys.stderr)
        return 1

    command_args = get_command_args(args)
    command = ['docker', 'compose', '--project-directory', str(project_dir),
               '-f', str(compose_file), *command_args]
    try:
        result = subprocess.run(command, cwd=project_dir, check=False)
    except FileNotFoundError:
        print('Docker не найден. Установите Docker с Compose и добавьте его в PATH.', file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130
    except OSError:
        print('Не удалось запустить Docker. Проверьте установку и права доступа.', file=sys.stderr)
        return 1
    if result.returncode == 0 and args.command == 'check':
        print('Конфигурация Docker Compose корректна.')
    return result.returncode if result.returncode >= 0 else 1


if __name__ == '__main__':
    sys.exit(main())
