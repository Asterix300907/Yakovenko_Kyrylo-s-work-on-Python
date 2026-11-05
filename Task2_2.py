import ast
import os
import sys


def analyze_settings(settings_path):
    with open(settings_path, 'r', encoding='utf-8-sig') as f:
        source = f.read()
    tree = ast.parse(source)
    config = {}
    target_keys = {'DEBUG', 'INSTALLED_APPS', 'DATABASES', 'LANGUAGE_CODE', 'TIME_ZONE'}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id in target_keys:
                    try:
                        value = ast.literal_eval(node.value)
                        config[target.id] = value
                    except (ValueError, TypeError):
                        config[target.id] = 'complex expression'
    return config


def check_security(settings_path):
    warnings = []
    with open(settings_path, 'r', encoding='utf-8-sig') as f:
        source = f.read()
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if not isinstance(target, ast.Name):
                    continue
                if target.id == 'DEBUG':
                    try:
                        if ast.literal_eval(node.value) is True:
                            warnings.append('DEBUG = True - nebezpechno dlia production')
                    except (ValueError, TypeError):
                        pass
                if target.id == 'SECRET_KEY':
                    if isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                        warnings.append('SECRET_KEY zakharkodzhenyi - vykorystovuite os.environ')
                if target.id == 'ALLOWED_HOSTS':
                    try:
                        value = ast.literal_eval(node.value)
                        if isinstance(value, list) and len(value) == 0:
                            warnings.append('ALLOWED_HOSTS porozhnii')
                    except (ValueError, TypeError):
                        pass
    return warnings


def main():
    settings_path = 'mysite/mysite/settings.py'
    if not os.path.exists(settings_path):
        print(f'Fail {settings_path} ne zaideno')
        sys.exit(1)
    config = analyze_settings(settings_path)
    print('=== Analiz konfiguratsii Django ===')
    for key, value in config.items():
        if key == 'INSTALLED_APPS':
            print(f'  {key}:')
            for app in value:
                print(f'    - {app}')
        elif key == 'DATABASES':
            print(f'  {key}:')
            if isinstance(value, dict):
                for alias, db_config in value.items():
                    engine = db_config.get('ENGINE', 'nevidomo')
                    db_name = engine.split('.')[-1] if '.' in engine else engine
                    print(f'    [{alias}] typ: {db_name}')
            else:
                print(f'    {value}')
    print()
    print('=== Perevirka bezpeky ===')
    warnings = check_security(settings_path)
    if warnings:
        for w in warnings:
            print(f'  [!] {w}')
    else:
        print('  Poperedzhen ne zaideno')


if __name__ == '__main__':
    main()