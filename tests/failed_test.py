from tests.test import Test


class FailedTest(Test):
    def __init__(self, status):
        self.status = status

    def run_test(self, status_result):
        status_result['status'] = self.status
