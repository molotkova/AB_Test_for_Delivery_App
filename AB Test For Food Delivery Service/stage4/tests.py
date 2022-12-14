from hstest import *
import re


def remove_empty_lines(string):
    # removes empty lines from the string
    # returns a list with \n separator
    string_splitted = string.split("\n")
    string_splitted_with_no_empty_lines = [line for line in string_splitted if line.strip() != ""]
    return string_splitted_with_no_empty_lines


class AATest(StageTest):
    TEST_NAME = "Mann-Whitney U test"

    def check_format_of_output(self, parameter_name, test_name, output_user):
        test_name_raw = test_name.replace(" ", "").lower()
        if test_name_raw not in output_user:
            raise WrongAnswer(f"Didn't find \"{test_name}\" substring in the output. Check the output format in the Examples section.")

        if output_user.count(test_name_raw) != 1:
            raise WrongAnswer(f"Substring \"{test_name}\" occurs more than once. Check the output format in the Examples section.")
        if parameter_name.lower() not in output_user:
            raise WrongAnswer(f"Didn't find \"{parameter_name}\", which is the test-statistic for the control group, in the output of your program.\n"
                              f"Check the output format in the Examples section.")

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

    def check_distributioins(self, output_user, test_name, answer_CORRECT, answer_WRONG):
        if output_user.count("distributionsaresame:") != 1:
            raise WrongAnswer(
                f"Substring \"Distributions are same:\" should occur once in the 3rd line of {test_name} results.\n"
                f"Found {output_user.count('distributionsaresame:')} occurrences.\n"
                f"Check the output format in the Examples section. Make sure there is no typos in the output of your program.")
        if answer_WRONG in output_user or answer_CORRECT not in output_user:
            raise WrongAnswer(f"Conclusion on distributions in {test_name} is wrong.")

    @dynamic_test
    def test(self):
        pr = TestedProgram()
        output = pr.start().replace(" ", "").lower()

        if len(output.strip()) == 0:
            raise WrongAnswer("Seems like your program does not show any output.")

        # check output format
        self.check_format_of_output(parameter_name="U1", test_name=self.TEST_NAME, output_user=output)

        mannwh_splitted = remove_empty_lines(output)

        if len(mannwh_splitted) != 4:
            raise WrongAnswer(f"The number of lines in {self.TEST_NAME} results is wrong.\n"
                              f"Expected 4, found {len(mannwh_splitted)}.\n"
                              f"Make sure that you provide test results in the correct format.")

        # check parameter value
        self.check_parameter_value(mannwh_splitted[1], self.TEST_NAME, "U1", 60612.0)

        # check p-value
        self.check_pvalue(mannwh_splitted[1], self.TEST_NAME, "p-value<=0.05", "p-value>0.05")

        # check conclusion on null hypothesis
        self.check_null_hypothesis(mannwh_splitted[2], self.TEST_NAME, "yes", "no")

        # check conclusion on distributions
        self.check_distributioins(mannwh_splitted[3], self.TEST_NAME, "no", "yes")

        return CheckResult.correct()


if __name__ == '__main__':
    AATest().run_tests()
