import sys
import traceback


class ApplicationException(Exception):
    """
    This class encapsulates the implementation of application exceptions.
    """

    def __init__(self):
        """
        The application exception constructor
        """
        # Get current system exception
        ex_type, ex_value, ex_traceback = sys.exc_info()

        # Extract unformatter stack traces as tuples
        trace_back = traceback.extract_tb(ex_traceback)

        # Format stacktrace
        stack_trace = list()

        # For all trace
        for trace in trace_back:
            stack_trace.append(
                "File : %s , Line : %d, Func.Name : %s, Message : %s" % (trace[0], trace[1], trace[2], trace[3]))

        # Save info in class attributes
        self.__type = ex_type.__name__
        self.__message = ex_value
        self.__stack_trace = stack_trace

    def get_type(self):
        """
        This function return the exception type
        :return: Type application exception
        """
        return self.__type

    def get_message(self):
        """
        This function return the exception messa
        :return: Message application exception
        """
        return self.__message

    def get_stack_trace(self):
        """
        This function return the exception stack trace
        :return: Stack trace application exception
        """
        return self.__stack_trace

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        r = 'TYPE:\n' + str(self.__type) + '\n\n'
        r += 'MESSAGE:\n' + str(self.__message) + '\n\n'
        r += 'STACK TRACE:\n' + str(self.__stack_trace)
        r += '\n-------------------------------------------------------------------------------\n'
        return r
