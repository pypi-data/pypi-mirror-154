from collections import UserDict,deque
import timeit
import itertools
import abc
from functools import partial

__NOKEY__=('__iTree_NOKEY__',)
__NOVALUE__ = ('__iTree_NOVALUE__',)

class iTDataValueError(Exception):
    pass
class iTDataTypeError(Exception):
    pass

class iTDataModel(abc.ABC):

    __slots__ = ('_value', '_formatter_cache')

    def __init__(self, value=__NOVALUE__):
        if not value == __NOVALUE__:
            value = self.validator(value)
        self._value = value
        self._formatter_cache = None

    def is_empty(self):
        return self._value == __NOVALUE__

    def get(self):
        if self._value == __NOVALUE__:
            return None
        return self._value

    def set(self, value, _it_data_model_identifier=None):
        self._value = self.validator(value)
        self._formatter_cache = None

    value = property(get, set)

    def clear(self, _it_data_model_identifier=None):
        """
        clears (deletes) the current value content and sets the state to "empty"

        :param _it_data_model_identifier: internal parameter used for identification
                                         of the set method in special cases, no functional impact

        :return: returns the value object that was stored in the iTreeDataModel
        """
        v = self.value
        self._value = __NOVALUE__
        self._formatter_cache = None
        return v

    @abc.abstractmethod
    def validator(self, value):
        return value

    @abc.abstractmethod
    def formatter(self, value=None):
        # place specific formatting here:
        if value is None:
            if self.is_empty():
                return 'None'
            value = self._value
        return str(value)

    def __contains__(self, item):
        return self._value == item

    def __format__(self, format_spec=None):
        if self.is_empty:
            # we might create an exception here when we have numerical values!
            # must be overloaded!
            return 'None'
        if format_spec is None or format_spec == '':
            # as long as the value is not changed we cache the result for quicker reuse:
            if self._formatter_cache is None:
                # run the formatter
                self._formatter_cache = self.formatter()
            return self._formatter_cache
        else:
            return super(iTDataModel, self).__format__(format_spec)

    def __repr__(self):
        if self.is_empty():
            return '%s()'%self.__class__.__name__
        return '%s(value= %s)' % (self.__class__.__name__,self._value)


class iTData1(dict):

    def __init__(self,seq=None,**kwargs):
        if not kwargs:
            if seq is None:
                super().__init__()
            else:
                try:
                    super().__init__(seq)
                except:
                    super().__init__([(__NOKEY__, seq)])
        else:
            if seq is None:
                super().__init__(**kwargs)
            else:
                items=itertools.chain(seq,kwargs.items())
                super().__init__(items)


    def __setitem__(self,key,value):
        try:
            item = super().__getitem__(key)
            item._value = item.validator(value)
        except (KeyError, AttributeError):
            super().__setitem__(key, value)

    def update(self, E=None, **F):

        if hasattr(E, 'keys'):
            items = deque(itertools.chain(E.items(), F.items()))
        else:
            items = deque(itertools.chain(E, F.items()))
        # check if we have just valid items will raise an exception if not matching!
        # precheck:
        i=0
        super_class=super(iTData1,self)
        try:
            models=deque()
            for i, (k, v) in enumerate(items):
                append=False
                try:
                    super_class.__getitem__(k).validator(v)
                    append = True
                except (KeyError,AttributeError):
                    pass
                models.append(append)
        except Exception as e:
            raise e.__class__('Input item %s raises: %s'%(str(items[i]),str(e)))
        #finally fill the data
        for (k, v), m in zip(items, models):
            if m:
                super_class.__getitem__(k).set(v)
            else:
                super_class.__setitem__(k, v)


class iTData2(UserDict):

    def __init__(self,seq=None,**kwargs):
        if not kwargs:
            if seq is None:
                super().__init__()
            else:
                try:
                    super().__init__(seq)
                except:
                    super().__init__([(__NOKEY__, seq)])
        else:
            if seq is None:
                super().__init__(**kwargs)
            else:
                items=
                super().__init__(itertools.chain(seq,kwargs.items()))

    def __setitem__(self,key,value):
        try:
            item = super().__getitem__(key)
            item._value = item.validator(value)
        except (KeyError, AttributeError):
            super().__setitem__(key, value)

    def update(self, E=None, **F):
        if hasattr(E, 'keys'):
            items = deque(itertools.chain(E.items(), F.items()))
        else:
            items = deque(itertools.chain(E, F.items()))
        # check if we have just valid items will raise an exception if not matching!
        # precheck:
        i=0
        super_class=super(iTData2,self)
        try:
            models=deque()
            for i, (k, v) in enumerate(items):
                append=False
                try:
                    super_class.__getitem__(k).validator(v)
                    append = True
                except (KeyError,AttributeError):
                    pass
                models.append(append)
        except Exception as e:
            raise e.__class__('Input item %s raises: %s'%(str(items[i]),str(e)))
        #finally fill the data
        for (k, v), m in zip(items, models): #we reuse here the validation that was already done!
            if m:
                super_class.__getitem__(k).set(v,_it_data_model_identifier=0)
            else:
                super_class.__setitem__(k, v)

class Model(iTDataModel):
    def validator(self,value):
        if type(value) is not int:
            raise iTDataValueError('Wrong type given')
        return value

    def formatter(self,value):
        return str(value)

def test(data_class,show=False):
    test_dict={'normal_item':1,'model_item':Model()}
    a=data_class(test_dict)
    try:
        a['model_item']='abc'
    except iTDataValueError:
        pass
    a['model_item'] = 1
    try:
        a.update({'_a':1,2:2,'model_item':'abc'})
    except Exception as e:
        if show:
            print('Exception:',str(e))
        pass
    else:
        raise Exception('Error not found!')
    assert len(a)==2,'LEN changed: %i'%len(a)

    a.update({'_a':1,2:2,'model_item':3})
    assert len(a)==4,'LEN wrong!: %i'%len(a)
    if show:
        print('Result:',a)


test(iTData1,True)
test(iTData2,True)
print('SPEEDTEST:')

repeat=100000
f=partial(test,iTData1)
print('dict time:',timeit.timeit(f,number=repeat))
f=partial(test,iTData2)
print('UserDict time:',timeit.timeit(f,number=repeat))

a=iTData2()
a.__dict__()