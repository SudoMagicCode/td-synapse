from enum import Enum
import json


class tdErrorLevel(Enum):
    info = 0
    warning = 1
    error = 2
    fatal = 3


class tdErrorOpType(Enum):
    comp = 'COMP'
    top = 'TOP'
    chop = 'CHOP'
    sop = 'SOP'
    pop = 'POP'
    mat = 'MAT'
    dat = 'DAT'
    custom = 'CUSTOM'
    misc = 'MISC'


class tdMsgType(Enum):
    message = 'message',
    error = 'error'


class tdAbstractMessage:
    def __init__(self,
                 message: str,
                 source: str,
                 absFrame: int,
                 severity: tdErrorLevel,
                 msgType: tdMsgType):
        self.message = message
        self.source = source
        self.severity = severity
        self.absFrame = absFrame
        self.messageType = msgType

    @property
    def _toDict(self) -> dict:
        dataAsDict: dict = {
            'message': self.message,
            'source': self.source,
            'severity': self.severity.value,
            'absFrame': self.absFrame,
            'msgType': self.messageType.value
        }
        return dataAsDict


class tdMessage(tdAbstractMessage):
    def __init__(self, message: str, source: str, absFrame: int):
        super().__init__(
            message=message,
            source=source,
            absFrame=absFrame,
            severity=tdErrorLevel.info,
            msgType=tdMsgType.message)

    @property
    def toDict(self) -> dict:
        return self._toDict

    @property
    def toJsonString(self) -> str:
        return json.dumps(self.toDict)


class tdError(tdAbstractMessage):
    def __init__(
            self,
            message: str,
            source: str,
            sourceOpType: str,
            absFrame: int,
            severity: int,
            opType: tdErrorOpType):

        super().__init__(
            message=message,
            source=source,
            absFrame=absFrame,
            severity=tdErrorLevel(severity),
            msgType=tdMsgType.error)

        self.sourceOpType = sourceOpType
        self.opType = tdErrorOpType(opType)

    def __repr__(self) -> str:
        return self.message

    @property
    def toDict(self) -> dict:
        dataAsDict: dict = self._toDict
        dataAsDict['opType'] = self.opType.name
        dataAsDict['sourceOpType'] = self.sourceOpType

        return dataAsDict

    @property
    def toJsonString(self) -> str:
        return json.dumps(self.toDict)
