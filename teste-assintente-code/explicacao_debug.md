# Análise e Correção de Erros: Sistema de Cálculo de Compra

Este documento lista todos os erros encontrados no código original, explica suas causas e apresenta as correções.

---

## Erros Identificados

### 1. ❌ **Erro: Aspas Faltantes (Syntax Error)**

**Localização**: Linha 6

**Código Original (Incorreto)**:
```python
item1 = float(input(Preço do item 1? ))
```

**Causa do Erro**:
- A mensagem dentro de `input()` está sem aspas.
- Python interpreta `Preço` como um identificador (variável), não como uma string.
- Gera: `NameError: name 'Preço' is not defined`

**Correção**:
```python
price = get_positive_number(f"Preço do item {i}: R$ ")
```

**Explicação da Correção**:
- Adicionadas aspas duplas ao redor da mensagem.
- Convertida para função reutilizável com validação.

---

### 2. ❌ **Erro: Falta de f-string (Logic Error)**

**Localização**: Linha 24

**Código Original (Incorreto)**:
```python
print(" Item 2:        R$ {total_item2:.2f}")
```

**Causa do Erro**:
- String sem prefixo `f` não interpola variáveis.
- O texto literal `{total_item2:.2f}` é exibido como está.
- Saída: `Item 2:        R$ {total_item2:.2f}` (em vez de `Item 2:        R$ 45.50`)

**Correção**:
```python
print(f" Item {idx}:        R$ {total:>8.2f}")
```

**Explicação da Correção**:
- Adicionado prefixo `f` para ativar interpolação.
- Usado loop para evitar repetição de código.

---

### 3. ❌ **Erro: Conversão de Tipo Faltante (Type Error)**

**Localização**: Linha 22

**Código Original (Incorreto)**:
```python
desconto_cupom = (input("Você tem um cupom de desconto? (Digite o percentual ou 0): "))
desconto = subtotal * (desconto_cupom / 100)
```

**Causa do Erro**:
- `input()` retorna sempre uma **string**, mesmo que o usuário digite um número.
- Tentar dividir uma string (`"10" / 100`) gera: `TypeError: unsupported operand type(s) for /: 'str' and 'int'`

**Correção**:
```python
discount_input = get_positive_number(
    "Você tem um cupom de desconto? (Digite o percentual ou 0): "
)
discount_percent = float(discount_input)
```

**Explicação da Correção**:
- Função `get_positive_number()` converte entrada para `float`.
- Validação integrada para garantir números válidos.

---

### 4. ❌ **Erro: Indentação Incorreta (Syntax Error)**

**Localização**: Linhas 31-32

**Código Original (Incorreto)**:
```python
if desconto_cupom > 0: 
print(f" Desconto ({desconto_cupom:.0f}%): -R$ {desconto:.2f}")
```

**Causa do Erro**:
- Instrução `print` fora do bloco `if` (indentação faltando).
- Python gera: `IndentationError: expected an indented block`

**Correção**:
```python
if invoice["discount_percent"] > 0:
    print(f" Desconto ({invoice['discount_percent']:.0f}%): -R$ {invoice['discount_amount']:>7.2f}")
```

**Explicação da Correção**:
- Adicionada indentação correta (4 espaços).
- Refatorado para usar dicionário estruturado.

---

### 5. ❌ **Erro: Comparação com String (Logic Error)**

**Localização**: Linha 31

**Código Original (Incorreto)**:
```python
if desconto_cupom > 0:
```

**Causa do Erro**:
- `desconto_cupom` é uma string (retornada por `input()`).
- Comparação `"10" > 0` não funciona como esperado.
- Em Python, strings podem ser comparadas, mas não com números numéricos de forma significativa.
- Pode gerar: `TypeError: '>' not supported between instances of 'str' and 'int'`

**Correção**:
```python
if invoice["discount_percent"] > 0:
```

**Explicação da Correção**:
- Agora `discount_percent` é um float válido.
- Comparação numérica funciona corretamente.

---

## Resumo dos Erros

| # | Tipo | Linha | Erro | Impacto |
|---|------|-------|------|---------|
| 1 | Syntax | 6 | Aspas faltantes | ❌ Programa não executa |
| 2 | Logic | 24 | Falta de `f` | ⚠️ Saída incorreta |
| 3 | Type | 22 | String não convertida | ❌ Programa quebra |
| 4 | Syntax | 31-32 | Indentação incorreta | ❌ Programa não executa |
| 5 | Logic | 31 | Comparação de string vs número | ⚠️ Comportamento inesperado |

---

## Melhorias Adicionais Implementadas

Além de corrigir os erros, o código foi refatorado com:

### ✅ **Validação de Entrada**
```python
def get_positive_number(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Por favor, insira um número positivo.")
                continue
            return value
        except ValueError:
            print("Entrada inválida. Por favor, insira um número.")
```
- Garante que apenas números válidos e positivos são aceitos.
- Loop infinito até entrada correta.

### ✅ **Separação de Responsabilidades**
- `calculate_invoice()`: Calcula valores
- `display_invoice()`: Exibe resultado
- `main()`: Coordena execução

### ✅ **Type Hints**
```python
def calculate_invoice(client_name: str, items: list[tuple[int, float]],
                      tax_rate: float = 0.10, discount_percent: float = 0) -> dict:
```

### ✅ **Docstrings Completas**
```python
"""Calcula a fatura total com imposto e desconto."""
```

### ✅ **Melhor Formatação**
- Alinhamento de valores com `>8.2f`
- Separadores visuais
- Mensagens de confirmação

---

## Como Testar o Código Corrigido

Execute o script:
```bash
python debug.py
```

**Entrada de Exemplo**:
```
Qual é seu nome? João Silva
Quantidade do item 1: 2
Preço do item 1: R$ 50
Quantidade do item 2: 3
Preço do item 2: R$ 25
Quantidade do item 3: 1
Preço do item 3: R$ 100
Você tem um cupom de desconto? (Digite o percentual ou 0): 10
```

**Saída Esperada**:
```
========================================
 SISTEMA DE CÁLCULO DE COMPRA
========================================

========================================
 Cliente: João Silva
========================================
 Item 1:        R$   100.00
 Item 2:        R$    75.00
 Item 3:        R$   100.00
----------------------------------------
 Subtotal:      R$   275.00
 Imposto (10%): R$    27.50
 Desconto (10%): -R$    27.50
========================================
 TOTAL:         R$   275.00
========================================

✅ Compra processada com sucesso!
```

---

## Lições de Depuração

1. **Sempre use aspas** para strings em Python
2. **Converta input() para o tipo correto** (int, float, etc.)
3. **Use f-strings** para interpolação de variáveis
4. **Indente corretamente** blocos de código (if, for, def, etc.)
5. **Valide entrada do usuário** para evitar erros em tempo de execução
6. **Teste seu código** com diversos valores, inclusive casos extremos

---

## Checklist de Boas Práticas

✅ **Erros Corrigidos**: Todos os 5 erros foram identificados e resolvidos  
✅ **Documentação**: Docstrings e comentários adicionados  
✅ **Validação**: Entrada do usuário validada  
✅ **Tratamento de Erros**: Try/except implementado  
✅ **Type Hints**: Tipos de dados especificados  
✅ **Legibilidade**: Código bem estruturado e organizado  
✅ **Reutilização**: Funções isoladas e genéricas
