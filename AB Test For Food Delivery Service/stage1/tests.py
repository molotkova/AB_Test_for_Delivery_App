from hstest import *
import re


def remove_empty_lines(string):
    # removes empty lines from the string
    # returns a list with \n separator
    string_splitted = string.split("\n")
    string_splitted_with_no_empty_lines = [line for line in string_splitted if line.strip() != ""]
    return string_splitted_with_no_empty_lines


class AATest(StageTest):
    LEVENE_TEST_NAME = "Levene's test"
    TTEST_NAME = "T-test"

    def check_format_of_output(self, test_name, output_user):
        test_name_raw = test_name.replace(" ", "").lower()
        if test_name_raw not in output_user:
            raise WrongAnswer(f"Didn't find \"{test_name}\" substring in the output. Check the output format in the Examples section.")

        if output_user.count(test_name_raw) != 1:
            raise WrongAnswer(f"Substring \"{test_name}\" occurs more than once. Check the output format in the Examples section.")

    def check_parameter_value(self, output_user, test_name, parameter_name, parameter_CORRECT):
        parameter_user = re.search(f'{parameter_name.lower()}=([+-]?(?:[0-9]*[.])?[0-9]+)', output_user)
        if parameter_user is None:
            raise WrongAnswer(f"Didn't find the value of {parameter_name} in the 1st line of {test_name} results.\n"
                              f"Note that you should present its value in the following format: {parameter_name} = <calculated value>.")
        parameter_user = float(parameter_user.group(1))
        if abs(parameter_CORRECT - parameter_user) > 1e-3:
            raise WrongAnswer(f"The value of {parameter_name}-statistics is wrong")

    def check_pvalue(self, output_user, test_name, pvalue_CORRECT, pvalue_WRONG):
        if output_user.count("p-value") != 1:
            raise WrongAnswer(f"Substring \"p-value\" should occur once in the 1st line of {test_name} results.\n"
                              f"Found {output_user.count('p-value')} occurrences.")
        if pvalue_WRONG in output_user or pvalue_CORRECT not in output_user:
            raise WrongAnswer(f"{test_name} p-value is wrong.\n"
                              f"Note that there are only two options: p-value <= 0.05 or p-value > 0.5.")

    def check_null_hypothesis(self, output_user, test_name, answer_CORRECT, answer_WRONG):
        if output_user.count("rejectnullhypothesis:") != 1:
            raise WrongAnswer(
                f"Substring \"Reject null hypothesis:\" should occur once in the 2nd line of {test_name} results.\n"
                f"Found {output_user.count('rejectnullhypothesis:')} occurrences.\n"
                f"Check the output format in the Examples section. Make sure there is no typos in the output of your program.")
        if answer_WRONG in output_user or answer_CORRECT not in output_user:
            raise WrongAnswer(f"Conclusion on {test_name} null hypothesis is wrong.")

    def check_equality(self, output_user, equality_parameter, test_name, answer_CORRECT, answer_WRONG):
        if output_user.count(f"{equality_parameter.lower()}areequal:") != 1:
            raise WrongAnswer(
                f"Substring \"{equality_parameter} are equal:\" should occur once in the 3rd line of {test_name} results.\n"
                f"Found {output_user.count(f'{equality_parameter}areequal:')} occurrences.\n"
                f"Check the output format in the Examples section. Make sure there is no typos in the output of your program.")
        if answer_WRONG in output_user or answer_CORRECT not in output_user:
            raise WrongAnswer(f"Conclusion on equality in {test_name} is wrong.")

    @dynamic_test
    def test(self):
        pr = TestedProgram()
        output = pr.start().replace(" ", "").lower()

        if len(output.strip()) == 0:
            raise WrongAnswer("Seems like your program does not show any output.")

        # check output format
        for test_name in [self.LEVENE_TEST_NAME, self.TTEST_NAME]:
            self.check_format_of_output(test_name=test_name,
                                        output_user=output)

        if not output.index(self.LEVENE_TEST_NAME.replace(" ", "").lower()) < output.index(self.TTEST_NAME.replace(" ", "").lower()):
            raise WrongAnswer(f"{self.LEVENE_TEST_NAME} results should be located before {self.TTEST_NAME} results.\n"
                              "Check the output format in the Examples section.")

        levene = output.split("t-test")[0]
        ttest = "t-test" + output.split("t-test")[1]

        levene_splitted = remove_empty_lines(levene)
        ttest_splitted = remove_empty_lines(ttest)

        for lines, test_name in [(levene_splitted, self.LEVENE_TEST_NAME), (ttest_splitted, self.TTEST_NAME)]:
            if len(lines) != 4:
                raise WrongAnswer(f"The number of lines in {test_name} results is wrong.\n"
                                  f"Expected 4, found {len(lines)}.\n"
                                  f"Make sure that you provide test results in the correct format.")
        # check parameter value
        for info in [(levene_splitted[1], self.LEVENE_TEST_NAME, "W", 0.0),
                     (ttest_splitted[1], self.TTEST_NAME, "t", -3.432)]:
            self.check_parameter_value(*info)
        # check p-value
        for info in [(levene_splitted[1], self.LEVENE_TEST_NAME, "p-value>0.05", "p-value<=0.05"),
                     (ttest_splitted[1], self.TTEST_NAME, "p-value<=0.05", "p-value>0.05")]:
            self.check_pvalue(*info)
        # check conclusion on null hypothesis
        for info in [(levene_splitted[2], self.LEVENE_TEST_NAME, "no", "yes"),
                     (ttest_splitted[2], self.TTEST_NAME, "yes", "no")]:
            self.check_null_hypothesis(*info)
        # check conclusion on equality
        for info in [(levene_splitted[3], "Variances", self.LEVENE_TEST_NAME, "yes", "no"),
                     (ttest_splitted[3], "Means", self.TTEST_NAME, "no", "yes")]:
            self.check_equality(*info)

        return CheckResult.correct()


if __name__ == '__main__':
    AATest().run_tests()
