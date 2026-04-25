"""
Módulo para verificação de números primos.

Este módulo fornece funções para identificar se um número é primo
usando algoritmos otimizados.
"""


def is_prime(number: int) -> bool:
    """
    Verifica se um número é primo.

    Um número primo é um número natural maior que 1 que possui
    exatamente dois divisores positivos: 1 e ele mesmo.

    Args:
        number: Um número inteiro a ser verificado.

    Returns:
        True se o número for primo, False caso contrário.

    Raises:
        TypeError: Se number não for um inteiro.

    Examples:
        >>> is_prime(17)
        True
        >>> is_prime(20)
        False
    """
    if not isinstance(number, int):
        raise TypeError(f"Esperado int, recebido {type(number).__name__}")

    if number <= 1:
        return False

    if number <= 3:
        return True

    # Elimina múltiplos de 2 e 3
    if number % 2 == 0 or number % 3 == 0:
        return False

    # Verifica divisores da forma 6k ± 1 até √n
    divisor = 5
    while divisor * divisor <= number:
        if number % divisor == 0 or number % (divisor + 2) == 0:
            return False
        divisor += 6

    return True


def get_prime_status(numbers: list[int]) -> dict[int, bool]:
    """
    Obtém o status primo para uma lista de números.

    Args:
        numbers: Lista de números inteiros.

    Returns:
        Dicionário com números como chaves e status primo como valores.
    """
    return {num: is_prime(num) for num in numbers}


def print_prime_results(numbers: list[int]) -> None:
    """
    Exibe se cada número em uma lista é primo.

    Args:
        numbers: Lista de números inteiros a verificar.
    """
    for number in numbers:
        status = "é primo" if is_prime(number) else "não é primo"
        print(f"{number} {status}")


def main() -> None:
    """Função principal com exemplos de teste."""
    test_numbers = [0, 1, 2, 3, 4, 5, 17, 18, 19, 20, 97]
    print_prime_results(test_numbers)


if __name__ == "__main__":
    main()
