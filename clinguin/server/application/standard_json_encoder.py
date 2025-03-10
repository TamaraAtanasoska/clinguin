"""
Module which contains the StandardJsonEncoder
"""
import logging

import networkx as nx

from clinguin.utils import Logger

from .element import ElementDto
from .attribute import AttributeDto
from .callback import CallbackDto

class StandardJsonEncoder:
    """
    The standrd json encoder is responsible for converting a ClinguinModel into a json hierarchy.
    """

    def __init__(self):
        pass

    @classmethod
    def encode(cls, model):
        """
        Public easy to access wrapper for the _generate_hierarchy method.

        Arguments:
            model : ClinguinModel
        """
        elements_dict = {}

        root = ElementDto('root', 'root', 'root')
        elements_dict[str(root.id)] = root

        cls._generate_hierarchy(model, root, elements_dict)

        return root

    @classmethod
    def _generate_hierarchy(cls, model, hierarchy_root, elements_dict):
        """
        Converts the ClinguinModel into an Json Hierarchy (which is represented by an ElementDto). Therefore it first gets all dependencies, then orders the elements according to the dependencies and then adds for each element its attributes, callbacks and children.

        Arguments:
            model : ClinguinModel
            hierarchy_root : ElementDto
            elements_dict : Dict
        """
        logger = logging.getLogger(Logger.server_logger_name)

        dependency = []
        elements_info = {}

        for w in model.get_elements():
            elements_info[w.id] = {'parent': w.parent, 'type': w.type}
            dependency.append((w.id, w.parent))

        DG = nx.DiGraph(dependency)
        order = list(reversed(list(nx.topological_sort(DG))))

        attrs = model.get_attributesGrouped()
        attrs = {a[0]:list(a[1]) for a in attrs}
        cbs = model.get_callbacksGrouped()
        cbs = {a[0]:list(a[1]) for a in cbs}

        for element_id in order:
            if str(element_id) == str(hierarchy_root.id):
                continue

            if not element_id in elements_info:
                logger.critical("The provided element id (ID : %s) could not be found!", str(element_id))
                raise Exception("The provided element id (ID : " + str(element_id) + ") could not be found!")

            type = elements_info[element_id]['type']
            parent = elements_info[element_id]['parent']
            element = ElementDto(element_id, type, parent)

            if element_id in attrs:
                elem_attributes = [AttributeDto(a.id, a.key, a.value) for a in attrs[element_id]]
                element.set_attributes(elem_attributes)
            if element_id in cbs:
                elem_callbacks = [CallbackDto(a.id, a.action, a.policy) for a in cbs[element_id]]
                element.set_callbacks(elem_callbacks)

            elements_dict[str(element_id)] = element
            elements_dict[str(element.parent)].add_child(element)
