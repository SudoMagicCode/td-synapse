from enum import Enum
import json


class MsgType(Enum):
    INIT = 'init'
    PROJECT_INFO = 'project_info'
    PERFORMANCE_INFO = 'performance_info'
    CUSTOM = 'custom'


class Synapse:

    def __init__(self, ownerOp: OP):
        self.Owner_op = ownerOp
        self.cook_info_chop: CHOP = ownerOp.op('base_cook_info/null_info')
        self.timer_chop: timerCHOP = ownerOp.op('timer_update')
        self.websocket_dat: websocketDAT = ownerOp.op('webserver_synapse')
        self.clients: set = set()
        print('Synapse initialized')

    def add_client(self, client: str) -> None:
        """
        """
        self.clients.add(client)
        self.timer_chop.par.start.pulse()

    def remove_client(self, client: str) -> None:
        """
        """
        self.clients.discard(client)

    def Server_start(self) -> None:
        """
        """
        pass

    def Server_stop(self) -> None:
        """
        """
        self.timer_chop.par.gotodone.pulse()
        self.clients.clear()

    def Websocket_open(self, client: str) -> None:
        """
        """
        self.add_client(client)
        self.Send_msg(
            msgType=MsgType.PROJECT_INFO,
            data=self.get_project_info())

    def Websocket_close(self, client: str) -> None:
        """
        """
        self.remove_client(client)

    def Send_performance_update(self) -> None:
        """
        """
        self.Send_msg(MsgType.PERFORMANCE_INFO, self.get_performance_info())

    def Send_msg(self, msgType: MsgType, data: dict) -> None:
        """
        """

        match msgType:
            case MsgType.INIT:
                pass

            case MsgType.PROJECT_INFO:
                data = self.get_project_info()
                msg_dict = {
                    'type': 'project_info',
                    'data': data
                }
                self.msg_clients(msg_dict)

            case MsgType.PERFORMANCE_INFO:
                data = self.get_performance_info()
                msg_dict = {
                    'type': 'performance_info',
                    'data': data
                }
                self.msg_clients(msg_dict)

            case MsgType.CUSTOM:
                pass

    def msg_clients(self, msg: dict) -> None:
        """
        """
        for eachClient in self.clients:
            self.websocket_dat.webSocketSendText(eachClient, json.dumps(msg))

    def get_project_info(self) -> dict:
        """
        """
        info = {
            'project': project.name,
            'version': app.version,
            'build': app.build,
            'experimental': app.experimental,
            'license': licenses.type,
            'colorBits': app.windowColorBits,
            'projectStartTime': round(app.launchTime, 2)
        }

        return info

    def get_performance_info(self) -> dict:
        """
        """
        info = {
            'frameTime': round(self.cook_info_chop['msec'][0], 4),
            'frameRate': int(self.cook_info_chop['fps'][0]),
            'targetFrameRate': int(self.cook_info_chop['cookrate'][0]),
            'dropoutRate': int(self.cook_info_chop['cook'][0]),
            'totalGpuMem': int(self.cook_info_chop['total_gpu_mem'][0]),
            'utilizedGpuMem': int(self.cook_info_chop['gpu_mem_used'][0]),
            'totalCpuMem': int(self.cook_info_chop['cpu_mem_used'][0]),
            'activeOps': int(self.cook_info_chop['active_ops'][0]),
            'realTime': bool(self.cook_info_chop['cookrealtime'][0]),
            'performMode': bool(self.cook_info_chop['perform_mode'][0]),
        }

        return info
