"""
Módulo para cálculo de estatísticas básicas de uma lista de números.

Este módulo fornece funções para calcular soma, média, máximo e mínimo
de forma eficiente e legível.
"""


def calculate_statistics(numbers: list[int | float]) -> dict[str, int | float]:
    """
    Calcula estatísticas básicas de uma lista de números.

    Retorna a soma, média aritmética, valor máximo e mínimo de uma lista.

    Args:
        numbers: Lista contendo números inteiros ou decimais.

    Returns:
        Dicionário com as seguintes chaves:
            - 'total': Soma de todos os números
            - 'media': Média aritmética dos números
            - 'maximo': Maior número da lista
            - 'minimo': Menor número da lista

    Raises:
        ValueError: Se a lista estiver vazia.
        TypeError: Se a lista contiver elementos que não são números.

    Examples:
        >>> calculate_statistics([23, 7, 45, 2, 67, 12, 89, 34, 56, 11])
        {'total': 346, 'media': 34.6, 'maximo': 89, 'minimo': 2}
    """
    if not numbers:
        raise ValueError("A lista não pode estar vazia")

    if not all(isinstance(num, (int, float)) for num in numbers):
        raise TypeError("Todos os elementos devem ser números")

    total = sum(numbers)
    average = total / len(numbers)
    maximum = max(numbers)
    minimum = min(numbers)

    return {
        "total": total,
        "media": average,
        "maximo": maximum,
        "minimo": minimum
    }


def display_statistics(statistics: dict[str, int | float]) -> None:
    """
    Exibe as estatísticas de forma formatada.

    Args:
        statistics: Dicionário contendo as estatísticas calculadas.
    """
    print("=" * 40)
    print("ESTATÍSTICAS DOS NÚMEROS")
    print("=" * 40)
    print(f"Total:   {statistics['total']}")
    print(f"Média:   {statistics['media']:.1f}")
    print(f"Máximo:  {statistics['maximo']}")
    print(f"Mínimo:  {statistics['minimo']}")
    print("=" * 40)


def main() -> None:
    """Função principal que executa o programa."""
    numbers = [23, 7, 45, 2, 67, 12, 89, 34, 56, 11]
    
    try:
        stats = calculate_statistics(numbers)
        display_statistics(stats)
    except (ValueError, TypeError) as error:
        print(f"Erro: {error}")


if __name__ == "__main__":
    main()