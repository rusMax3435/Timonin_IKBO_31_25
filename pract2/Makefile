.PHONY: run test clean

# Запуск программы с демонстрационными параметрами
run:
	python3 src/main.py -p "my-fail" -r "https://github.com/rusMax3435/Timonin_IKBO_31_25" -o "graph.png" -v "1.0.0"

# Запуск тестов
test:
	python3 -m unittest discover tests

# Очистка кэша Python
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete