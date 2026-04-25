# Explicação do Código Python: Verificação de Números Primos

Este documento explica o código Python presente no arquivo `num_primos.py`, que implementa uma função para verificar se um número é primo.

## Código Python

```python
def is_prime(n: int) -> bool:
    """Retorna True se n for primo, caso contrário False."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


if __name__ == "__main__":
    numeros = [0, 1, 2, 3, 4, 5, 17, 18, 19, 20, 97]
    for numero in numeros:
        print(f"{numero} é primo? {is_prime(numero)}")
```

## Explicação Detalhada

### Função `is_prime(n: int) -> bool`

Esta função verifica se um número inteiro `n` é primo. Um número primo é um número maior que 1 que não tem divisores positivos além de 1 e ele mesmo.

- **Parâmetros**:
  - `n`: O número a ser verificado (tipo `int`).

- **Retorno**:
  - `bool`: `True` se o número for primo, `False` caso contrário.

### Lógica da Função

1. **Verificação inicial para números pequenos**:
   - Se `n <= 1`, retorna `False` (1 e números negativos não são primos).
   - Se `n <= 3`, retorna `True` (2 e 3 são primos).

2. **Verificação de divisibilidade por 2 e 3**:
   - Se `n` for divisível por 2 ou 3, retorna `False`.

3. **Loop de verificação para outros fatores**:
   - Inicia com `i = 5`.
   - Enquanto `i * i <= n` (ou seja, enquanto `i` for menor ou igual à raiz quadrada de `n`):
     - Verifica se `n` é divisível por `i` ou por `i + 2` (que são os próximos números ímpares).
     - Se for divisível, retorna `False`.
     - Incrementa `i` em 6 (pulando para o próximo número que não é múltiplo de 2 ou 3).
   - Se nenhum divisor for encontrado, retorna `True`.

Essa abordagem é eficiente porque:
- Elimina rapidamente números pares e múltiplos de 3.
- Verifica apenas até a raiz quadrada de `n`, reduzindo o número de operações.
- Usa incrementos de 6 para pular números desnecessários.

### Bloco de Teste (`if __name__ == "__main__"`)

Este bloco é executado apenas quando o script é rodado diretamente (não quando importado como módulo).

- Define uma lista de números de teste: `[0, 1, 2, 3, 4, 5, 17, 18, 19, 20, 97]`.
- Para cada número na lista, chama a função `is_prime` e imprime o resultado no formato: "{numero} é primo? {resultado}".

Isso permite testar a função com vários casos, incluindo números primos e não primos.

## Como Executar

Para executar o código, use o comando:
```
python num_primos.py
```

Isso irá imprimir os resultados dos testes na tela.
