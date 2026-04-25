"""
Sistema de Cálculo de Compra com Imposto e Desconto.

Calcula o total de uma compra com até 3 itens, aplicando imposto
e desconto baseado em cupom.
"""


def get_positive_number(prompt: str) -> float:
    """
    Solicita um número positivo ao usuário com validação.

    Args:
        prompt: Mensagem a exibir ao usuário.

    Returns:
        Número positivo inserido pelo usuário.
    """
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Por favor, insira um número positivo.")
                continue
            return value
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")


def calculate_invoice(client_name: str, items: list[tuple[int, float]],
                      tax_rate: float = 0.10, discount_percent: float = 0) -> dict:
    """
    Calcula a fatura total com imposto e desconto.

    Args:
        client_name: Nome do cliente.
        items: Lista com tuplas (quantidade, preço) de cada item.
        tax_rate: Taxa de imposto (padrão 10%).
        discount_percent: Percentual de desconto (padrão 0%).

    Returns:
        Dicionário com detalhes da fatura.
    """
    item_totals = [qty * price for qty, price in items]
    subtotal = sum(item_totals)
    tax = subtotal * tax_rate
    discount_amount = subtotal * (discount_percent / 100)
    total = subtotal + tax - discount_amount

    return {
        "client": client_name,
        "item_totals": item_totals,
        "subtotal": subtotal,
        "tax": tax,
        "tax_rate": tax_rate,
        "discount_percent": discount_percent,
        "discount_amount": discount_amount,
        "total": total
    }


def display_invoice(invoice: dict) -> None:
    """
    Exibe a fatura de forma formatada.

    Args:
        invoice: Dicionário contendo os dados da fatura.
    """
    linha = "=" * 40
    separador = "-" * 40

    print(linha)
    print(f" Cliente: {invoice['client']}")
    print(linha)

    # Exibe cada item
    for idx, total in enumerate(invoice["item_totals"], 1):
        print(f" Item {idx}:        R$ {total:>8.2f}")

    print(separador)
    print(f" Subtotal:      R$ {invoice['subtotal']:>8.2f}")
    print(f" Imposto ({invoice['tax_rate']*100:.0f}%): R$ {invoice['tax']:>8.2f}")

    if invoice["discount_percent"] > 0:
        print(f" Desconto ({invoice['discount_percent']:.0f}%): -R$ {invoice['discount_amount']:>7.2f}")

    print(linha)
    print(f" TOTAL:         R$ {invoice['total']:>8.2f}")
    print(linha)


def main() -> None:
    """Função principal que executa o programa."""
    print("\n" + "=" * 40)
    print(" SISTEMA DE CÁLCULO DE COMPRA")
    print("=" * 40 + "\n")

    # Entrada de dados
    client_name = input("Qual é seu nome? ").strip()

    items = []
    for i in range(1, 4):
        qty = int(get_positive_number(f"Quantidade do item {i}: "))
        price = get_positive_number(f"Preço do item {i}: R$ ")
        items.append((qty, price))

    # Desconto
    discount_input = get_positive_number(
        "Você tem um cupom de desconto? (Digite o percentual ou 0): "
    )
    discount_percent = float(discount_input)

    # Validar percentual de desconto
    if discount_percent > 100:
        print("⚠️  Desconto máximo é 100%. Ajustando para 100%.")
        discount_percent = 100

    # Calcular fatura
    invoice = calculate_invoice(client_name, items, discount_percent=discount_percent)

    # Exibir resultado
    display_invoice(invoice)
    print("\n✅ Compra processada com sucesso!\n")


if __name__ == "__main__":
    main()