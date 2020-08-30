from datetime import datetime, timedelta
import time


def getCurTimestamp(withMilliseconds=False):
    """
    get current time's timestamp
        (default)not milliseconds -&gt; 10 digits: 1351670162
        with milliseconds -&gt; 13 digits: 1531464292921
    """
    curDatetime = datetime.now()
    return datetimeToTimestamp(curDatetime, withMilliseconds)


def datetimeToTimestamp(datetimeVal, withMilliseconds=False):
    """
        convert datetime value to timestamp
        eg:
            "2006-06-01 00:00:00.123" -&gt; 1149091200
            if with milliseconds -&gt; 1149091200123
    :param datetimeVal:
    :return:
    """
    timetupleValue = datetimeVal.timetuple()
    timestampFloat = time.mktime(timetupleValue)  # 1531468736.0 -&gt; 10 digits
    timestamp10DigitInt = int(timestampFloat)  # 1531468736
    timestampInt = timestamp10DigitInt

    if withMilliseconds:
        microsecondInt = datetimeVal.microsecond  # 817762
        microsecondFloat = float(microsecondInt) / float(1000000)  # 0.817762
        timestampFloat = timestampFloat + microsecondFloat  # 1531468736.817762
        timestampFloat = timestampFloat * 1000  # 1531468736817.7621 -&gt; 13 digits
        timestamp13DigitInt = int(timestampFloat)  # 1531468736817
        timestampInt = timestamp13DigitInt

    return timestampInt
