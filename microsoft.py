#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 17:49:23 2019

@author: lsx
"""

import microsoft_utils
import microsoft_protocol


class Field(object):
    """
    """


class TimeField(Field):
    """
    """
    def __init__(self, vals):
        self.field = vals
        self.functions = microsoft_utils.time_func_mapping
        self.__parse_func = lambda field: field
    
    def _clean_func(self, field):
        try:
            field = int(field)
        except:
            field = None
        return field
                
    @property
    def parse_func(self):
        return self.__parse_func
        
    @parse_func.setter
    def parse_func(self, parse_func):
        self.__parse_func = parse_func        
        
    def _clean_field(self):
        func = self._clean_func
        para = self.field
        field = func(para)
        self.field = field
        
    def parse(self, parse_func=None):
        self._clean_field()
        '''
        '''
        if not parse_func:
            func = self.parse_func
        elif isinstance(parse_func, str):
            if not (parse_func in self.functions.keys()):
                raise ValueError('Invalid parse time function')
            func = microsoft_utils.time_func_mapping[parse_func]
        else:
            func = parse_func
        para = self.field
        self.parsed = func(para)

        
class KindField(Field):
    """
    """
    def __init__(self, vals):
        self.field = vals
        self.functions = microsoft_utils.kind_field_mapping

    def _clean_func(self, field):
        try:
            field = int(field)
        except:
            field = None
        return field        

    def _parse_func(self, field):
        if not (field in microsoft_utils.kind_field_mapping.keys()):
            field = 'uk'
        else:
            field = microsoft_utils.kind_field_mapping[field]
        return field
        
    def _clean_field(self):
        func = self._clean_func
        para = self.field
        field = func(para)
        self.field = field                 

    def parse(self):
        self._clean_field()
        func = self._parse_func 
        para = self.field
        self.parsed = func(para)                   
        
        
class DataField(Field):
    """
    """
    def __init__(self, vals):
        self.field = vals
        self.__clean_func = lambda field: field
        self.__parse_func = lambda field: field

    @property
    def clean_func(self):
        return self.__clean_func
        
    @clean_func.setter
    def clean_func(self, clean_func):
        self.__clean_func = clean_func       
        
    @property
    def parse_func(self):
        return self.__parse_func
        
    @parse_func.setter
    def parse_func(self, parse_func):
        self.__parse_func = parse_func         
        
    def _clean_field(self):
        func = self.clean_func
        para = self.field
        field = func(para)
        self.field = field
    
    def parse(self):
        self._clean_field()
        func = self.parse_func
        para = self.field
        self.parsed = func(para)


#class DeclarativeFieldsMetaclass(MediaDefiningClass):
#    """Collect Fields declared on the base classes."""
#    def __new__(mcs, name, bases, attrs):
#        # Collect fields from current class.
#        current_fields = []
#        for key, value in list(attrs.items()):
#            if isinstance(value, Field):
#                current_fields.append((key, value))
#                attrs.pop(key)
#        attrs['declared_fields'] = OrderedDict(current_fields)
#
#        new_class = super(DeclarativeFieldsMetaclass, mcs).__new__(mcs, name, bases, attrs)
#
#        # Walk through the MRO.
#        declared_fields = OrderedDict()
#        for base in reversed(new_class.__mro__):
#            # Collect fields from base class.
#            if hasattr(base, 'declared_fields'):
#                declared_fields.update(base.declared_fields)
#
#            # Field shadowing.
#            for attr, value in base.__dict__.items():
#                if value is None and attr in declared_fields:
#                    declared_fields.pop(attr)
#
#        new_class.base_fields = declared_fields
#        new_class.declared_fields = declared_fields
#
#        return new_class
        
   
class Frame(object):
    """
    """   
    def __init__(self, frame):
        self.frame = frame
    
    __struct = microsoft_protocol.frame_struct_mapping
    __time = None
    __kind = None
    __vals = None
    
    @property
    def struct(self):
        return self.__struct
        
    @struct.setter
    def struct(self, struct_dict):
        if not isinstance(struct_dict, dict):
            raise ValueError('Invalid struct dict')
        self.__struct = struct_dict
        
    @property
    def time(self):
        return self.__time
        
    @time.setter
    def time(self, time_vals):
        self.__time = time_vals
    
    @property
    def kind(self):
        return self.__kind
        
    @kind.setter
    def kind(self, kind_vals):
        self.__time = kind_vals

    @property
    def data(self):
        return self.__data
        
    @data.setter
    def data(self, data_vals):
        self.__data = data_vals       
    
    def _clean(self):
        """
        """
        
    def parse(self):
        """
        """
        pass


def FrameSelect(steam):
    mapping = {'1': HrFrame, '2': PmFrame, '5': AcFrame, '7': StFrame, '0': ErFrame}
    time_field_vals = steam[0]
    kind_field_vals = steam[1]
    data_field_vals = steam[2]
    Frame = mapping[kind_field_vals]
    frame = Frame(steam)
    return frame                
        
            
class HrFrame(Frame):
    """
    """    
    def __init__(self, frame):
        super(HrFrame, self).__init__(frame)
        self.frame = frame

#    def __init__(self, url_map, separator="+"):
#        super(ListConverter, self).__init__(url_map)
#        self.separator = urllib.parse.unquote(separator) 
        
    def _parse_data_field_func(self, vals):
        return [vals]
    
    def _clean_data_field_func(self, vals):
        try:
            vals = float(vals)
        except:
            vals = None
        return vals
    
    def _clean(self):
        time_vals = self.frame[0]
        kind_vals = self.frame[1]
        data_vals = self.frame[2]
        self.time_field = TimeField(time_vals)
        self.kind_field = KindField(kind_vals)
        self.data_field = DataField(data_vals)
        self.data_field.clean_func = self._clean_data_field_func       
        self.data_field.parse_func = self._parse_data_field_func        
               
    def parse(self, parse_time_field_func=None):
        self._clean()
        if parse_time_field_func:
            self.time_field.parse_func = parse_time_field_func
        self.time_field.parse()
        self.kind_field.parse()        
        self.data_field.parse()
        self.time = self.time_field.parsed
        self.kind = self.kind_field.parsed
        self.data = self.data_field.parsed
        self.parsed = {'time': self.time_field.parsed,
                       'kind': self.kind_field.parsed,
                       'data': self.data_field.parsed}

        
class AcFrame(Frame):
    """
    """
    def __init__(self, frame):
        super(AcFrame, self).__init__(frame)
        self.frame = frame
    
    def _parse_data_field_func(self, vals):
        return vals
    
    def _clean_data_field_func(self, vals):
        try:
            vals = list(map(lambda val: float(val), vals))
        except:
            vals = None
        return vals
    
    def _clean(self):
#        super(AcFrame, self)._clean()
        time_vals = self.frame[0]
        kind_vals = self.frame[1]
        data_vals = self.frame[2]
        self.time_field = TimeField(time_vals)
        self.kind_field = KindField(kind_vals)
        self.data_field = DataField(data_vals)
        self.data_field.clean_func = self._clean_data_field_func       
        self.data_field.parse_func = self._parse_data_field_func        
               
    def parse(self, parse_time_field_func=None):
#        super(AcFrame, self).parse(parse_time_field_func)
        self._clean()
        if parse_time_field_func:
            self.time_field.parse_func = parse_time_field_func
        self.time_field.parse()
        self.kind_field.parse()        
        self.data_field.parse()
        self.time = self.time_field.parsed
        self.kind = self.kind_field.parsed
        self.data = self.data_field.parsed
        self.parsed = {'time': self.time_field.parsed,
                       'kind': self.kind_field.parsed,
                       'data': self.data_field.parsed}


class PmFrame(Frame):
    """
    """
    def __init__(self, frame):
        super(PmFrame, self).__init__(frame)
        self.frame = frame
    
    def _parse_data_field_func(self, vals):
        return [vals]
    
    def _clean_data_field_func(self, vals):
        try:
            vals = float(vals)
        except:
            vals = None
        return vals
    
    def _clean(self):
#        super(PmFrame, self)._clean()
        time_vals = self.frame[0]
        kind_vals = self.frame[1]
        data_vals = self.frame[2]
        self.time_field = TimeField(time_vals)
        self.kind_field = KindField(kind_vals)
        self.data_field = DataField(data_vals)
        self.data_field.clean_func = self._clean_data_field_func       
        self.data_field.parse_func = self._parse_data_field_func        
               
    def parse(self, parse_time_field_func=None):
        self._clean()
        if parse_time_field_func:
            self.time_field.parse_func = parse_time_field_func
        self.time_field.parse()
        self.kind_field.parse()        
        self.data_field.parse()
        self.time = self.time_field.parsed
        self.kind = self.kind_field.parsed
        self.data = self.data_field.parsed
        self.parsed = {'time': self.time_field.parsed,
                       'kind': self.kind_field.parsed,
                       'data': self.data_field.parsed}


class StFrame(Frame):
    """
    """
    def __init__(self, frame):
        super(StFrame, self).__init__(frame)
        self.frame
    
    def _parse_data_field_func(self, vals):
        return [vals]
    
    def _clean_data_field_func(self, vals):
        try:
            vals = float(vals)
        except:
            vals = None
        return vals
    
    def _clean(self):
        time_vals = self.frame[0]
        kind_vals = self.frame[1]
        data_vals = self.frame[2]
        self.time_field = TimeField(time_vals)
        self.kind_field = KindField(kind_vals)
        self.data_field = DataField(data_vals)
        self.data_field.clean_func = self._clean_data_field_func       
        self.data_field.parse_func = self._parse_data_field_func        
               
    def parse(self, parse_time_field_func=None):
        self._clean()
        if parse_time_field_func:
            self.time_field.parse_func = parse_time_field_func
        self.time_field.parse()
        self.kind_field.parse()        
        self.data_field.parse()
        self.parsed = {'time': self.time_field.parsed,
                       'kind': self.kind_field.parsed,
                       'data': self.data_field.parsed}

                       
class ErFrame(Frame):
    
    def __init__(self, frame):
        super(ErFrame, self).__init__(frame)
        self.frame
        
#    def _parse_data_field_func(self, vals):
#        vals = None
#        return [vals]

    def _clean(self):
#        super(AcFrame, self)._clean()
        time_vals = self.frame[0]
        kind_vals = self.frame[1]
        data_vals = self.frame[2]
        self.time_field = TimeField(time_vals)
        self.kind_field = KindField(kind_vals)
        self.data_field = DataField(data_vals)
#        self.data_field.parse_func = self._parse_data_field_func       
        
    def parse(self, parse_time_field_func=None):
        self._clean()
        self.time_field.parse()
        self.kind_field.parse()        
        self.data_field.parse()
        self.time = self.time_field.parsed
        self.kind = self.kind_field.parsed
        self.data = self.data_field.parsed
        self.parsed = {'time': self.time_field.parsed,
                       'kind': self.kind_field.parsed,
                       'data': self.data_field.parsed}                       
                       
                       
def SteamTrans(steam):
    try:
        steam = steam.split(';')
    except:
        steam = [None, '0', None]
    if len(steam) < 3:
        steam = [None, '0', None]
    kind = steam[1]
    steam_ = list()
    try:
        if kind == '5':
            time = steam[0]
            kind = steam[1]
            data = steam[2:5]
            steam_ = [time, kind, data]
        elif kind in ['1', '2', '7']:
            time = steam[0]
            kind = steam[1]
            data = steam[2]
            steam_ = [time, kind, data]
        else:
            time = None
            kind = '0'
            data = None      
            steam_ = [time, kind, data]
    except:
        time = None
        kind = '0'
        data = None    
        steam_ = [time, kind, data]
    return steam_
                                     
                       
#    def parse(self, steam):
#        frame_struct = microsoft_protocol.frame_struct_mapping
#        steam = steam.split(';')
#        steam = steam[0:3]
#        time_field_vals = steam[frame_struct['time_field_offset']]
#        kind_field_vals = steam[frame_struct['kind_field_offset']]
#        data_field_vals = steam[frame_struct['data_field_offset']]
#        if kind_field_vals == self.mapping['hr']:
#            frame = HrFrame(time_field_vals, kind_field_vals, data_field_vals)
#        elif kind_field_vals == self.mapping['ac']:
#            frame = AcFrame(time_field_vals, kind_field_vals, data_field_vals)
#        elif kind_field_vals == self.mapping['pm']:
#            frame = PmFrame(time_field_vals, kind_field_vals, data_field_vals)
#        elif kind_field_vals == self.mapping['st']:
#            frame = StFrame(time_field_vals, kind_field_vals, data_field_vals)
#        else:
#            raise ValueError('Invalid frame') 
#        frame.parse()
#        return frame
        
        