1) Перед запуском тестов нужно выполнить установку необходимых библиотек

    Команда: **pip install -r requirements.txt**

2) Коллекцию тестов можно запустить командой: **pytest -v** 

3) Для запуска конкретного теста:
**pytest -v test_suite.py::TestSuite::test_case_#**

где, 
******test_case_# = имя функции теста****


