import pytest
from io import StringIO
from contextlib import redirect_stdout

# Импортируем калькулятор
import src.main as calculator

def test_calculator_expressions() -> None :
    """Простой тест вычислений калькулятора"""

    # Тестируем основные операции
    test_cases = [
        # (входное выражение, ожидаемый результат)
        ('2 3 +', '5.0'),
        ('5 2 -', '3.0'),
        ('3 4 *', '12.0'),
        ('10 2 /', '5.0'),
        ('2 3 **', '8.0'),
        ('10 3 //', '3.0'),
        ('10 3 %', '1.0'),
        ('5 ~', '-5.0'),
        ('5 $', '5.0'),
        ('2.5 1.5 +', '4.0'),
        ('-2 -3 *', '6.0'),
    ]

    for expr, expected in test_cases:
        output = StringIO()
        with redirect_stdout(output):
            calculator.calc(expr)
        assert output.getvalue().strip() == expected

def test_calculator_errors() -> None :
    """Тест обработки ошибок"""

    # Тестируем ошибки
    error_cases = [
        ('10 0 /', ZeroDivisionError),
        ('10 0 //', ZeroDivisionError),
        ('10 0 %', ZeroDivisionError),
        ('( 2 3 +', SyntaxError),
        ('2 abc +', ValueError),
        ('2 3 4 +', SyntaxError),
        ('2 +', SyntaxError),
        ('', SyntaxError),
    ]

    for expr, error_type in error_cases:
        with pytest.raises(error_type):
            calculator.calc(expr)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
