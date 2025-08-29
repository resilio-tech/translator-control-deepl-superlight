import deepl
import json
from PySide6 import QtCore
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QLabel, QTextEdit, QWidget, QLineEdit, QSizePolicy)
import argparse
import sys

parser = argparse.ArgumentParser("simple_example")
parser.add_argument("target_lang", help="Target lang in which you want to translate (ES, FR, DE, EN, IT, etc).", type=str)
parser.add_argument("base_file", help="Source file i18n-formatted containing the text to translate (relative path).", type=str)
parser.add_argument("auth_key", help="API key for Deepl", type=str)
args = parser.parse_args()

print(f'Starting translation, using Deepl to translate {args.base_file} in {args.target_lang}')

deepl_client = deepl.DeepLClient(args.auth_key)

with open(args.base_file, encoding='utf-8') as f:
	d = json.load(f)

def NestedDictValues(d):
	for v in d.values():
		if isinstance(v, dict):
			yield from NestedDictValues(v)
		else:
			yield v

res = {}
for source in set(NestedDictValues(d)):
	# print(source)
	# trad = deepl_client.translate_text(source, target_lang=args.target_lang)
	# print(trad.text)
	res.update({source: 'r'}) #trad.text})

res_updated = res.copy()

def NestedDictReplace(d):
	new = d.copy()
	for k, v in d.items():
		if isinstance(v, dict):
			new[k] = NestedDictReplace(v)
		else:
			new[k] = res_updated[v]
	return new

class MyWidget(QWidget):
	def __init__(self):
		super().__init__()

		# Preparing the widget
		self.text = QLabel("Please control translation", alignment=QtCore.Qt.AlignCenter)

		self.table = QTableWidget()
		self.table.setRowCount(len(res))
		self.table.setColumnCount(2)
		self.table.setHorizontalHeaderLabels(["Source", "Translation"])

		for i, (source, trad) in enumerate(res.items()):
			# Create a QLabel for the source text
			source_label = QLabel()
			source_label.setText(source)
			source_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

			# Create a QTextEdit for the translation text
			trad_edit = QTextEdit()
			trad_edit.setText(trad)
			trad_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

			# Set as cell widget
			self.table.setCellWidget(i, 0, source_label)
			self.table.setCellWidget(i, 1, trad_edit)

		# Resize the rows to fit the text
		for i in range(len(res)):
			self.table.resizeRowToContents(i)

		self.button = QPushButton("Validate and Save")

		self.layout = QVBoxLayout(self)
		self.layout.addWidget(self.text)
		self.layout.addWidget(self.table)
		self.layout.addWidget(self.button)

		self.button.clicked.connect(self.onValidation)

	@QtCore.Slot()
	def onValidation(self):
		values = []
		for row in range(self.table.rowCount()):
			translation = self.table.item(row, 1).text()
			values.append(translation)
		
		idx = 0
		for k, v in res.items():
			if v != values[idx]:
				res_updated.update({k: values[idx]})
				print(f"{k}: {v} -> {values[idx]}")
			idx += 1
		
		translated = NestedDictReplace(d)

		with open('translated.json', 'w') as f:
			json.dump(translated, f)

		print("Text translated !")
		print(translated)

		app.quit()

# All the stuff inside your window.
app = QApplication()
widget = MyWidget()
widget.resize(800, 600)
widget.show()

sys.exit(app.exec())
