from enum import Enum


class RunState(Enum):
    """
    服务器运行状态，继承枚举类型
    使用方法 获取值：RunState.down.value 结果 0
             获取名：RunState.down.name  结果 'down'
             根据id获取name  RunState(1).name  结果 'up'
             根据name获取id  RunState['checkSucc'].value  结果 2
    """
    down = 0  # 关机
    up = 1  # 开机
    checkSucc = 2  # IPMI效验成功
    checkFail = 3  # IPMI效验失败
    RaidSuccess = 4  # Raid配置成功
    RaidFail = 5  # Raid配置失败
    InstallOsSuccess = 6  # 安装系统成功
    InstallOsFail = 7  # 安装系统失败
    ConfigBiosSuccess = 8
    ConfigBiosFail = 9


print(RunState['ConfigBiosFail'].value)