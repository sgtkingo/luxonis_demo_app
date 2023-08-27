from enum import Enum

#Define signals enums
SCRAPY_STATUS_ENUM = Enum('Status', ['UNKNOWN', 'READY', 'RUNNING', 'DONE', 'ERROR'])

#Define signals
SCRAPY_STATUS = SCRAPY_STATUS_ENUM.UNKNOWN
SCRAPY_PROCESS = 0
