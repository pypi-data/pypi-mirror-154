# coding: utf8
import pyTSL
import datetime
import configparser

connectConfig = {}
defaultConnection = None
connectConfigFile = None


def SetConnectConfig(fn):
    global connectConfigFile
    connectConfigFile = fn


def connectOptions(alias):
    global connectConfigFile
    if connectConfigFile:
        f = connectConfigFile
    else:
        f = 'tslclient.ini'
    config = configparser.ConfigParser(delimiters=('=',))
    config.read(f)
    if alias in config.sections():
        return config[alias]
    return {}


def DefaultConnectAndLogin(alias):
    global defaultConnection
    opts = connectOptions(alias)
    if opts:
        defaultConnection = pyTSL.Client(
            opts['LoginName']
            , opts['LoginPass']
            , opts['Address']
            , int(opts['Port'])
        )
        if defaultConnection.login():
            return 0, ''
        else:
            return defaultConnection.last_error()


def ConnectServer(host, port, proxy={}):
    global connectConfig
    connectConfig['host'] = host
    connectConfig['port'] = port
    connectConfig['proxy'] = proxy


def LoginServer(user, passwd):
    global defaultConnection
    host = connectConfig['host']
    port = connectConfig['port']
    defaultConnection = pyTSL.Client(user, passwd, host, port)
    if defaultConnection.login():
        return 0, ''
    else:
        return defaultConnection.last_error()


def Disconnect():
    global defaultConnection
    if defaultConnection:
        defaultConnection.logout()


def Logined():
    global defaultConnection
    if defaultConnection:
        return defaultConnection.login()
    return 0


def SetService(service):
    global defaultConnection
    if defaultConnection:
        defaultConnection.default_service(service)


def SetComputeBitsOption(opt):
    pass


def GetComputeBitsOption():
    pass


def GetService():
    global defaultConnection
    if defaultConnection:
        return defaultConnection.default_service()


def parse_params(params):
    pp = {}
    if 'StockID' in params:
        pp['stock'] = params['StockID']
    if 'Cycle' in params:
        pp['cycle'] = params['Cycle']
    if 'CurrentDate' in params:
        pp['time'] = pyTSL.DoubleToDatetime(params['CurrentDate'])
    if 'bRate' in params:
        pp['rate'] = params['bRate']
    if 'RateDay' in params:
        pp['rateday'] = params['RateDay']
    if 'nDay' in params:
        pp['nday'] = params['nDay']
    if 'Precision' in params:
        pp['precision'] = params['Precision']
    if 'ReportMode' in params:
        pp['reportmode'] = params['ReportMode']
    if 'EmptyMode' in params:
        pp['emptymode'] = params['EmptyMode']
    if 'viewpoint' in params:
        pp['viewpoint'] = params['viewpoint']
    return pp


def RemoteExecute(script, params):
    global defaultConnection
    if defaultConnection:
        pp = parse_params(params)
        r = defaultConnection.exec(script, **pp)
        return r.error(), r.value()
    return -1, '连接错误'


def RemoteCallFunc(func, args, params):
    global defaultConnection
    if defaultConnection:
        pp = parse_params(params)
        r = defaultConnection.call(func, *args, **pp)
        return r.error(), r.value()
    return -1, '连接错误'


def EncodeDate(y, m, d):
    return pyTSL.DatetimeToDouble(datetime.datetime(y, m, d))


def EncodeTime(h, m, s, ss):
    return h / 24.0 + m / 24.0 / 60.0 + s / 24.0 / 3600.0 + ss / 24.0 / 3600000.0


def EncodeDateTime(Y, M, D, h, m, s, ss):
    return pyTSL.DatetimeToDouble(datetime.datetime(Y, M, D, h, m, s, ss * 1000))


def DecodeDate(dt):
    d = pyTSL.DoubleToDatetime(dt)
    return d.year, d.month, d.day


def DecodeTime(dt):
    d = pyTSL.DoubleToDatetime(dt)
    return d.hour, d.minute, d.second, d.microsecond * 1000


def DecodeDateTime(dt):
    d = pyTSL.DoubleToDatetime(dt)
    return d.year, d.month, d.day, d.hour, d.minute, d.second, d.microsecond * 1000


if __name__ == '__main__':
    pass
