🐍 Python 簡單語法筆記

1. 變數與資料型別

   Python 是一個動態型別語言，無需明確聲明變數型別。

```python
# 整數
x = 10

# 浮點數
y = 3.14

# 字串
name = "Alice"

# 布林值
is_active = True
```

2. 基本運算

   Python 支援常見的數學運算，並使用簡單的符號來表示。

```python
# 加法
result = 5 + 3 # 8

# 減法
result = 10 - 7 # 3

# 乘法
result = 4 \* 2 # 8

# 除法
result = 10 / 2 # 5.0 (浮點數結果)

# 次方
result = 2 \*\* 3 # 8
```

3. 條件判斷

   使用 if、elif 和 else 來進行條件判斷。

```python
age = 18

if age >= 18:
print("成人")
elif age > 12:
print("青少年")
else:
print("兒童")
```

4. 迴圈

   Python 有兩種主要的迴圈：for 和 while。

- for 迴圈

  ```python
  # 列印 1 到 5
  for i in range(1, 6):
  print(i)
  ```

- while 迴圈

  ```python
  # 列印直到條件為假
  count = 0
  while count < 5:
  print(count)
  count += 1
  ```

5. 函式

使用 def 關鍵字來定義函式

```python
def greet(name):
return f"Hello, {name}!"

# 呼叫函式
message = greet("Alice")
print(message) # Hello, Alice!
```

6. 清單與迭代

   清單是 Python 中的基本資料結構，可以存放多個元素。

```python
# 定義清單
fruits = ["蘋果", "香蕉", "橘子"]

# 迭代清單
for fruit in fruits:
print(fruit)
```

7. 字典

   字典是由鍵值對組成的資料結構。

```python
# 定義字典
person = {
    "name": "Alice",
    "age": 25,
    "city": "Taipei"
}

# 訪問字典元素
print(person["name"]) # Alice
```

8. 異常處理

   使用 try-except 來處理可能出現的錯誤。

```python
try:
result = 10 / 0
except ZeroDivisionError:
print("除以 0 的錯誤！")
```

這些是 Python 的一些基礎語法，適合初學者快速入門。如果要深入學習，可以進一步探討物件導向、模組與套件等進階概念。
