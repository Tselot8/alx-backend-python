# ALX Backend Python: Unit and Integration Testing

## Project Overview

This project focuses on writing **unit tests** and **integration tests** for Python code using the `unittest` framework. Key skills include parameterization, mocking HTTP calls, patching methods and properties, memoization, and integration testing with fixtures.

All exercises are implemented in the `0x03-Unittests_and_integration_tests` directory of the repository.

**Repository:** [alx-backend-python](https://github.com/Tselot8/alx-backend-python)

---

## Table of Contents

1. [Parameterize a Unit Test](#1-parameterize-a-unit-test)  
2. [Mock HTTP Calls](#2-mock-http-calls)  
3. [Parameterize and Patch](#3-parameterize-and-patch)  
4. [Parameterize and Patch as Decorators](#4-parameterize-and-patch-as-decorators)  
5. [Mocking a Property](#5-mocking-a-property)  
6. [More Patching](#6-more-patching)  
7. [Parameterize License Check](#7-parameterize-license-check)  
8. [Integration Test: Fixtures](#8-integration-test-fixtures)  

---

## 1. Parameterize a Unit Test

**Objective:** Write unit tests for the `utils.access_nested_map` function.  

**Instructions:**

- Create a `TestAccessNestedMap` class inheriting from `unittest.TestCase`.
- Implement `test_access_nested_map` method.
- Use `@parameterized.expand` to test multiple inputs:

| `nested_map`              | `path`     | Expected Result |
|----------------------------|------------|----------------|
| `{"a": 1}`                | `("a",)`   | `1`            |
| `{"a": {"b": 2}}`         | `("a",)`   | `{"b": 2}`     |
| `{"a": {"b": 2}}`         | `("a","b")`| `2`            |

- The test body should **not exceed 2 lines**.
- Implement `test_access_nested_map_exception` to test KeyError with:

| `nested_map` | `path`      |
|--------------|------------|
| `{}`         | `("a",)`   |
| `{"a": 1}`   | `("a","b")`|

- Use `assertRaises` to ensure the exception and the message are correct.

**File:** `test_utils.py`  

---

## 2. Mock HTTP Calls

**Objective:** Test `utils.get_json` without making real HTTP calls.

**Instructions:**

- Create `TestGetJson(unittest.TestCase)` class.
- Implement `test_get_json` method.
- Use `unittest.mock.patch` to mock `requests.get`.
- Parametrize inputs with:

| `test_url`             | `test_payload`         |
|------------------------|----------------------|
| `"http://example.com"` | `{"payload": True}`  |
| `"http://holberton.io"`| `{"payload": False}` |

- Test that `requests.get` is called **once per input**.
- Ensure the return value of `get_json` equals `test_payload`.

**File:** `test_utils.py`  

---

## 3. Parameterize and Patch

**Objective:** Test the `utils.memoize` decorator.

**Instructions:**

- Create `TestMemoize(unittest.TestCase)` class with `test_memoize`.
- Inside, define:

```python
class TestClass:
    def a_method(self):
        return 42

    @memoize
    def a_property(self):
        return self.a_method()
