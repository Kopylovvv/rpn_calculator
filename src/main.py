import sys
# import os
#
# # Добавляем родительскую директорию в путь
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.constants as constants

# Строки, содержащие все операторы, унарные и бинарные операторы
operators = constants.operators
unary_operators = constants.unary_operators
binary_operators = constants.binary_operators


def is_int(token: float) -> bool:
    """
    Проверяет, является ли число целым.

    Args:
        token (float): Число для проверки

    Returns:
        bool: True если число целое, False в противном случае
    """
    if token == int(token):
        return True
    return False


def is_operator(token: str) -> bool:
    """
    Проверяет, является ли токен оператором.

    Args:
        token (str): Токен для проверки

    Returns:
        bool: True если токен является оператором, False в противном случае
    """
    if operators.find(token) != -1:
        return True
    return False


def get_token(expr: list) -> str | None:
    """
    Извлекает первый токен из выражения.

    Args:
        expr (list): Список токенов выражения

    Returns:
        str | None: Первый токен из списка или None если список пуст
    """
    return expr[0] if expr else None


def compute(stack: list[float], operator: str) -> list[float]:
    """
    Выполняет математическую операцию над числами из стека.

    Args:
        stack (list[float]): Стек с числами для операций
        operator (str): Оператор для выполнения

    Returns:
        list[float]: Обновленный стек после выполнения операции

    Raises:
        IndexError: Если для бинарного оператора недостаточно операндов
        ZeroDivisionError: При делении на ноль
        ValueError: Для операций, требующих целые числа
        SyntaxError: При неизвестном операторе
    """
    # Извлекаем первый операнд из стека
    num1 = stack.pop()

    # Обрабатываем унарные операторы
    if unary_operators.find(operator) != -1:
        match operator:
            case '~':
                # Унарный минус - меняем знак числа
                stack.append(num1 * -1)
            case '$':
                # Унарный плюс - оставляем число как есть
                stack.append(num1)

    # Обрабатываем бинарные операторы
    elif binary_operators.find(operator) != -1:
        # Извлекаем второй операнд из стека
        if stack:
            num2 = stack.pop()
        else:
            raise IndexError('Wrong expression: there are more operators than operands')

        # Выполняем соответствующую бинарную операцию
        match operator:
            case '+':
                stack.append(num1 + num2)
            case '-':
                stack.append(num2 - num1)
            case '*':
                stack.append(num1 * num2)
            case '**':
                stack.append(num2 ** num1)
            case '/':
                if num1 != 0:
                    stack.append(num2 / num1)
                else:
                    raise ZeroDivisionError('Cannot divide by zero')
            case '//':
                if num1 != 0:
                    if is_int(num1) and is_int(num2):
                        stack.append(num2 // num1)
                    else:
                        raise ValueError('Can be performed only for integers')
                else:
                    raise ZeroDivisionError('Cannot divide by zero')
            case '%':
                if num1 != 0:
                    if is_int(num1) and is_int(num2):
                        stack.append(num2 % num1)
                    else:
                        raise ValueError('Can be performed only for integers')
                else:
                    raise ZeroDivisionError('Cannot divide by zero')
    else:
        raise SyntaxError('Unknown operator')
    return stack


def is_num(token: str) -> bool:
    """
    Проверяет, является ли токен числом.

    Args:
        token (str): Токен для проверки

    Returns:
        bool: True если токен можно преобразовать в число, False в противном случае
    """
    try:
        float(token)
        return True
    except ValueError:
        return False


def check_brackets(expression: str) -> bool:
    """
    Проверяет правильность расстановки скобок в выражении.

    Args:
        expression (str): Математическое выражение для проверки

    Returns:
        bool: True если скобки расставлены правильно, False в противном случае
    """
    stack = []

    for char in expression:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if not stack:  # Если стек пуст, но встретилась закрывающая скобка
                return False
            stack.pop()  # Удаляем соответствующую открывающую скобку

    return len(stack) == 0  # Все скобки должны быть закрыты


def remove_brackets(expr: str) -> str:
    """
    Удаляет скобки из выражения, заменяя их пробелами.

    Args:
        expr (str): Выражение со скобками

    Returns:
        str: Выражение с удаленными скобками
    """
    expr = expr.replace('(', ' ').replace(')', ' ')
    return expr


def calc(expr: str) -> None:
    """
    Вычисляет математическое выражение в обратной польской записи.

    Args:
        expr (str): Выражение для вычисления


    Raises:
        SyntaxError: При ошибках в выражении (неправильные скобки, синтаксис)
        ValueError: При неизвестных токенах
        ZeroDivisionError: При делении на ноль
        IndexError: При неправильном количестве операндов
    """
    # Проверяем корректность скобок перед вычислением
    if check_brackets(expr):
        # Удаляем скобки и разбиваем выражение на токены
        expr_without_brackets = remove_brackets(expr)
        expr_list = expr_without_brackets.split()
        stack: list[float] = []

        # Обрабатываем каждый токен в выражении
        while expr_list:
            token = get_token(expr_list)

            if token is None:
                break

            if is_operator(token):
                # Обрабатываем оператор
                if len(stack) >= 1:
                    stack = compute(stack, token)
                else:
                    raise SyntaxError('Wrong expression')

            elif is_num(token):
                # Добавляем число в стек
                stack.append(float(token))

            else:
                raise ValueError('Unknown token')
            expr_list = expr_list[1:]

        # Извлекаем результат из стека
        if stack:
            res = stack.pop()
        else:
            raise SyntaxError('Wrong expression')

        # Проверяем, что в стеке не осталось лишних чисел
        if not stack:
            print(res)
        else:
            raise SyntaxError('Wrong expression: there are more operands than operators')
    else:
        raise SyntaxError('Wrong expression: incorrect brackets')


def run() -> None:
    """
    Основная функция для запуска калькулятора.
    Читает выражения из стандартного ввода и вычисляет их.
    Обрабатывает возможные исключения при вычислениях.
    """
    for line in sys.stdin:
        try:
            calc(line)
        except ZeroDivisionError as err:
            print(f"{err}")
        except SyntaxError as err:
            print(f"{err}")
        except ValueError as err:
            print(f"{err}")
        except IndexError as err:
            print(f"{err}")


if __name__ == "__main__":
    run()
