"""
Module that contains the EndpointsHelper class.
"""
import logging
import traceback
from ...utils import CaseConverter, Logger, SERVER_ERROR_ALERT

# def sever_error_json(e):
#     model = ClinguinModel()
#     model.add_message("Error","Server error")
#     json_structure =  StandardJsonEncoder.encode(model)
#     return json_structure


class EndpointsHelper:
    """
    The EndpointsHelper class is responsible for getting the correct method in the ''backend'' (here backend refers to ClingoBackend, TemporalBackend, etc.). This is done via reflections, i.e. it checks if the method is in the backend, if yes the method it returned.
    """

    @classmethod
    def call_function(cls, backend, name, args, kwargs):
        logger = logging.getLogger(Logger.server_logger_name)

        found = False
        function = None

        snake_case_name = name
        camel_case_name = CaseConverter.snake_case_to_camel_case(snake_case_name)


        if hasattr(backend, snake_case_name):
            function = getattr(backend, snake_case_name)
            found = True
        elif hasattr(backend, camel_case_name):
            function = getattr(backend, camel_case_name)
            found = True

        if found:
            try:
                result = function(*args, **kwargs)
                return result
            except Exception as e:
                logger.error(e)
                logger.error(traceback.format_exc())
                return SERVER_ERROR_ALERT
                
                # return sever_error_json(e)
        else:
            error_string = "Could not find function: " + name + " :in backend"
            logger.error(error_string)
            raise Exception(error_string)

