# Explicação do Código Python: Verificação de Números Primos

Este documento explica o código Python refatorado no arquivo `num_primos.py`, que implementa um módulo completo para verificar números primos seguindo padrões de **Clean Code**.

## Visão Geral

O módulo contém:
- **Função principal**: `is_prime()` - verifica se um número é primo
- **Funções auxiliares**: `get_prime_status()` e `print_prime_results()` - funções de suporte
- **Função principal**: `main()` - coordena a execução

---

## Código Python Refatorado

```python
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
```

---

## Melhorias Implementadas (Clean Code)

### 1. **Docstring de Módulo**
   - Adicionado docstring descritivo no início do arquivo.
   - Explica o propósito e conteúdo do módulo.

### 2. **Nomes Descritivos**
   - `n` → `number`: Nome mais claro e expressivo
   - `i` → `divisor`: Identifica o propósito da variável
   - `numeros` → `test_numbers`: Mais específico e em inglês (padrão)

### 3. **Docstrings Completas**
   - Adicionadas seções: Args, Returns, Raises, Examples
   - Seguem o padrão Google/NumPy para documentação
   - Facilitam compreensão e uso da função

### 4. **Type Hints Aprimorados**
   - `list[int]` em vez de `list` (tipo parametrizado)
   - `dict[int, bool]` para retornos de dicionário
   - `None` para funções sem retorno

### 5. **Validação de Entrada**
   - Adicionada verificação de tipo com `isinstance()`
   - Lança `TypeError` com mensagem descritiva se necessário

### 6. **Comentários Estratégicos**
   - Adicionados apenas onde a lógica não é óbvia
   - Explicam o "por quê" e não o "o quê"

### 7. **Separação de Responsabilidades**
   - `is_prime()`: Apenas valida se é primo
   - `get_prime_status()`: Retorna dicionário de resultados
   - `print_prime_results()`: Exibe resultados formatados
   - `main()`: Coordena a execução

### 8. **Função Main()**
   - Padrão Python para ponto de entrada
   - Deixa claro qual é a execução principal

---

## Explicação da Lógica

### Algoritmo `is_prime()`

O algoritmo utiliza otimizações para eficiência:

1. **Tratamento de casos especiais**:
   - Números ≤ 1: não são primos
   - 2 e 3: são primos
   
2. **Eliminação rápida**:
   - Se divisível por 2 ou 3: não é primo
   
3. **Loop otimizado**:
   - Verifica apenas divisores da forma `6k ± 1`
   - Itera apenas até √n
   - Reduz significativamente o número de operações

**Complexidade**: O(√n) - muito eficiente para números grandes

---

## Como Usar

### Executar o script:
```bash
python num_primos.py
```

### Importar como módulo:
```python
from num_primos import is_prime, get_prime_status

# Verificar um número
print(is_prime(17))  # True

# Verificar múltiplos números
status = get_prime_status([2, 3, 4, 5])
print(status)  # {2: True, 3: True, 4: False, 5: True}
```

---

## Benefícios da Refatoração

✅ **Mais legível**: Nomes claros e estrutura organizada  
✅ **Mais mantível**: Funções com responsabilidades únicas  
✅ **Mais robusto**: Validação de entrada e tratamento de erros  
✅ **Mais documentado**: Docstrings detalhadas e exemplos  
✅ **Mais reutilizável**: Pode ser importado como módulo  
✅ **Mais testável**: Funções puras e isoladas
