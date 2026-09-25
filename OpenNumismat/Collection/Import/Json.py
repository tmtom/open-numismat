# -*- coding: utf-8 -*-

import json
import os

from PySide6.QtCore import QStandardPaths

from OpenNumismat.Collection.Import import _Import
from OpenNumismat.Collection.CollectionFields import ImageFields


class ImportJson(_Import):
    def __init__(self, parent=None):
        super().__init__(parent)

    @staticmethod
    def isAvailable():
        return True

    @staticmethod
    def defaultDir():
        dirs = QStandardPaths.standardLocations(QStandardPaths.DownloadLocation)
        if dirs:
            return dirs[0]
        else:
            return ''

    def _connect(self, src):
        return src

    def _getRows(self, srcFile):
        with open(srcFile, 'r', encoding='utf-8') as file:
            data = json.load(file)

        self.imageDir = os.path.splitext(srcFile)[0] + '_images'
        return data['coins'][:data['description']['count']]

    def _setRecord(self, record, coin):
        for field, value in coin.items():
            if field in ImageFields and value:
                image_file_name = os.path.join(self.imageDir, value)
                with open(image_file_name, 'rb') as file:
                    value = file.read()
            record.setValue(field, value)
