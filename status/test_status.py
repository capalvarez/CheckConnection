import default_values


class TestStatus:
    def write_test(self, ip, file):
        pass

    def decide_status(self):
        return self

    def isOK(self):
        return False


class InvalidIPAddressStatus(TestStatus):
    def write_test(self, ip, file):
        file.write('\t' + ip['name'] + ' ' + ip['ip'] + ' Invalid destination IP\n')


class IncorrectPingFormatStatus(TestStatus):
    def write_test(self, ip, file):
        file.write('\t' + ip['name'] + ' ' + ip['ip'] + ' Incorrect Ping Format\n')


class InvalidIPSourceStatus(TestStatus):
    def write_test(self, ip, file):
        file.write('\t' + ip['name'] + ' ' + ip['ip'] + ' Invalid source IP\n')


class OKTestStatus(TestStatus):
    def __init__(self, result=0):
        self.result = result

    def write_test(self, ip, file):
        file.write('\t' + ip['name'] + ' ' + ip['ip'] + ' OK!\n')

    def decide_status(self):
        if self.result >= default_values.success_threshold:
            return OKTestStatus()
        else:
            return FailedTestStatus(self.result)

    def isOK(self):
        return True


class FailedTestStatus(TestStatus):
    def __init__(self, hits):
        self.hits = hits

    def write_test(self, ip, file):
        file.write('\t' + ip['name'] + ' ' + ip['ip'] + ' ' + str(self.hits) +
                   '% TESTS SUCCESSFUL \n')
