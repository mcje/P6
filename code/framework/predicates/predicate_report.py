__author__ = 'Mathias Claus Jensen'


 # The amount of errornous elements that will be printed
MAX_ELEMENTS = 100


class Report(object):
    """ A container object for all the info we would like regarding the result 
    of a predicate.
    """
    
    def __init__(self, result, predname, elements=[], msg=None):
        """
        :param result: Boolean denoting wether the predicate was succesful or 
        not.
        :param predname: String that contains the name of the predicate we are 
        reporting for. E.g 'CompareTablePredicate'
        :param elements: A list of elements in which errors were found. Each 
        element has to be printable
        :param msg: A message that is displayed if elements is empty and the
        result is False
        """
        self.result = result
        self.predname = predname
        
        if not result and not elements and not msg: # Maybe not do this
            raise ValueError('If result is False, then either elements or msg' \
                              + 'has to be set')
        else:
            self.elements = elements
            self.msg = msg

    def __str__(self):
        """ Prints the reports in a sorta nice way
        """
        s = self.predname + ': ' 
        if self.result:
            return s + 'SUCCESS\n'
        elif self.elements:
            s += 'FAILED\nThe predicate did not hold on the following entries\n'
            i = 0
            for e in self.elements:
                if i < MAX_ELEMENTS:
                    s += '\t' + str(e) + ',\n'
                    i += 1
                elif i == MAX_ELEMENTS:
                    s += ' \t...\n'
            return s
        else:
            return self.msg
