import re
from validator import constants


class Validator:

    @staticmethod
    def validate(cron_expression: str) -> bool:
        """
            Validates a given cron expression and returns a boolean evaluated value.

            Fields -------- Required -------- Allowed values -------- Allowed Special Characters
            Seconds            Y              0-59                    ,-*/
            Minutes            Y              0-59                    ,-*/
            Hours              Y              0-23                    ,-*/
            Day of Month       Y              1-31                    ,-*/? L W
            Month              Y              1-12 or JAN-DEC         ,-*/
            Day of Week        Y              0-6 or SUN-SAT          ,-*/? L
            Year               N              empty or 1970-2099      ,-*/
        """
        cron_arguments = cron_expression.rsplit(" ")
        if len(cron_arguments) < constants.CRON_EXPRESSION_MIN_ARGUMENTS or \
                len(cron_arguments) > constants.CRON_EXPRESSION_MAX_ARGUMENTS:
            return False
        is_cron_valid = Validator.validate_seconds_and_minutes(
            cron_arguments[constants.SECONDS_SUBEXPRESSION_INDEX]) and Validator.validate_seconds_and_minutes(
            cron_arguments[constants.MINUTES_SUBEXPRESSION_INDEX]) and Validator.validate_hours(
            cron_arguments[constants.HOURS_SUBEXPRESSION_INDEX]) and Validator.validate_day_of_month(
            cron_arguments[constants.DAY_OF_MONTH_SUBEXPRESSION_INDEX]) and Validator.validate_month(
            cron_arguments[constants.MONTH_SUBEXPRESSION_INDEX]) and Validator.validate_day_of_week(
            cron_arguments[constants.DAY_OF_WEEK_SUBEXPRESSION_INDEX])
        if len(cron_arguments) == constants.CRON_EXPRESSION_MAX_ARGUMENTS:
            return is_cron_valid and Validator.validate_year(cron_arguments[constants.YEAR_SUBEXPRESSION_INDEX])
        return is_cron_valid

    @staticmethod
    def validate_seconds_and_minutes(seconds_and_minutes_expression: str) -> bool:
        """
            Validates a cron subexpression of seconds or minutes and returns a boolean evaluated value.
        """
        return len(re.findall(constants.SECONDS_AND_MINUTES_REGEX_EXPRESSION, seconds_and_minutes_expression)) > 0 and \
               Validator.__validate_list_with_ranges(seconds_and_minutes_expression)

    @staticmethod
    def validate_hours(hours_expression: str) -> bool:
        """
            Validates a cron subexpression of hours and returns a boolean evaluated value.
        """
        return len(re.findall(constants.HOURS_REGEX_EXPRESSION, hours_expression)) > 0 and \
               Validator.__validate_list_with_ranges(hours_expression)

    @staticmethod
    def validate_day_of_month(day_of_month_expression: str) -> bool:
        """
            Validates a cron subexpression of the day of the month and returns a boolean evaluated value.
        """
        return len(re.findall(constants.DAY_OF_MONTH_REGEX_EXPRESSION, day_of_month_expression)) > 0 and \
               Validator.__validate_list_with_ranges(day_of_month_expression)

    @staticmethod
    def validate_month(month_expression: str) -> bool:
        """
            Validates a cron subexpression of the month and returns a boolean evaluated value.
        """
        if any(alternative_value in month_expression for alternative_value in constants.MONTHS_LIST):
            return len(re.findall(constants.MONTH_ALTERNATIVE_VALUES_REGEX_EXPRESSION, month_expression)) > 0 and \
                   Validator.__validate_list_with_ranges(month_expression, constants.MONTHS_LIST)
        return len(re.findall(constants.MONTH_NUMBERS_REGEX_EXPRESSION, month_expression)) > 0 and \
               Validator.__validate_list_with_ranges(month_expression)

    @staticmethod
    def validate_day_of_week(day_of_week_expression: str) -> bool:
        """
            Validates a cron subexpression of the day of the week and returns a boolean evaluated value.
        """
        if any(alternative_value in day_of_week_expression for alternative_value in constants.DAY_OF_WEEK_LIST):
            return len(re.findall(constants.DAY_OF_WEEK_ALTERNATIVE_VALUES_REGEX_EXPRESSION,
                                  day_of_week_expression)) > 0 and \
                   Validator.__validate_list_with_ranges(day_of_week_expression, constants.DAY_OF_WEEK_LIST)
        return len(re.findall(constants.DAY_OF_WEEK_NUMBERS_REGEX_EXPRESSION, day_of_week_expression)) > 0 and \
               Validator.__validate_list_with_ranges(day_of_week_expression)

    @staticmethod
    def validate_year(year_expression: str) -> bool:
        """
            Validates a cron subexpression of the year and returns a boolean evaluated value.
        """
        return len(re.findall(constants.YEAR_REGEX_EXPRESSION, year_expression)) > 0 and \
               Validator.__validate_list_with_ranges(year_expression)

    @staticmethod
    def __validate_range(range_expression: str, range_list: list = None) -> bool:
        range_values = range_expression.rsplit(constants.RANGE_ELEMENT_DELIMITER)
        if not len(range_values) > 0:
            return False
        if range_list:
            return range_list.index(range_values[constants.FIRST_RANGE_ELEMENT_INDEX]) < \
                   range_list.index(range_values[constants.SECOND_RANGE_ELEMENT_INDEX])
        return int(range_values[constants.FIRST_RANGE_ELEMENT_INDEX]) < \
               int(range_values[constants.SECOND_RANGE_ELEMENT_INDEX])

    @staticmethod
    def __validate_list_with_ranges(list_expression: str, range_list: list = None) -> bool:
        if Validator.__is_range_expression(list_expression):
            if Validator.__is_list_expression(list_expression):
                list_values = list_expression.rsplit(constants.LIST_ELEMENT_DELIMITER)
                range_values = [arg for arg in list_values if Validator.__is_range_expression(arg)]
                valid_ranges = [range_value for range_value in range_values
                                if Validator.__validate_range(range_value, range_list)]
                return len(valid_ranges) == len(range_values)
            return Validator.__validate_range(list_expression, range_list)
        return True

    @staticmethod
    def __is_list_expression(expression: str) -> bool:
        return constants.LIST_ELEMENT_DELIMITER in expression

    @staticmethod
    def __is_range_expression(expression: str) -> bool:
        return constants.RANGE_ELEMENT_DELIMITER in expression
