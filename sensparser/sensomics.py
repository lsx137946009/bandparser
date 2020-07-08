# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 17:58:36 2019

@author: sixing liu, yaru chen

__version = 2.0.0

Steam:
    - TimeSteam
    - DataSteam

Field:
    - ... Base Unit
    
Frame
    - ... 
    
Future:
    ADD-
    Metaclass
    Iter
    
"""

from __future__ import division, print_function, absolute_import
# from numpy import __version__ as __numpy_version__ 
import sensomics_utils



class SteamTrans(object):
    """
    summary of class here
    
    Attrbutes:
        steam: one piece of data.
    """
    
    def __init__(self):
        """ get attribute steam """
        pass
    
    def _clena_func(self, steam):
        steam = steam.replace('[','').replace(']','')
        steam = steam.split(',')
        steam = list(map(lambda vals: int(vals), steam))
        return steam
                        
    def _clean(self, steam):
        try: # split into [time_steam, data_steam:[*,*,*,*,...]]
            steam = str(steam)
            steam = steam.split(';')
            time_steam = int(steam[0])
            data_steam = self._clena_func(steam[1])
            type_steam = data_steam[4:6]
            steam = [time_steam, data_steam, type_steam]
        except:
            time_steam = None
            data_steam = None
            type_steam = [-1, -1]
            steam = [time_steam, data_steam, type_steam]
        return steam
        
    def parse(self, steam):
        steam = self._clean(steam)
        return steam

        

class Field(object):
    """
    """        


class TimeField(object):
    """
    """
    def __init__(self):
        self.functions = sensomics_utils.time_func_mapping
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
        
    def _clean(self, field):
        field = self._clean_func(field)
        return field
        
    def parse(self, field, parse_func=None):
        field = self._clean(field)
        '''
        '''
        if not parse_func:
            func = self.parse_func
        elif isinstance(parse_func, str):
            if not (parse_func in self.functions.keys()):
                raise ValueError('Invalid parse time function')
            func = sensomics_utils.time_func_mapping[parse_func]
        else:
            func = parse_func
        field = func(field)
        parsed = {'time': field}
        return parsed       
        
        
class StartFrameField(Field):
    """
    """
    def __init__(self):
        self.norm = [[int(0xab)], [int(0)]]
        self.size = 1
        self.__defined = None
        
    @property
    def defined(self):
        return self.__defined
        
    @defined.setter
    def defined(self, defined):
        self.__defined = defined      

    def _clean_func(self, field):
        if not isinstance(field, list):
            field = [field]
        if len(field) != self.size:
            field = None
        if not field in self.norm:
            field = None
        return field
        
    def _parse_func(self, field):
        if not field == self.defined:
            raise ValueError('Invaild StartFrameField Value')
        return field
        
    def _clean(self, field):
        field = self._clean_func(field)
        return field
    
    def _parse(self, field):
        field = self._parse_func(field)
        return field

    def parse(self, field):
        field = self._clean(field)
        parsed = self._parse(field)
        return parsed
        
                
class DataLengthField(Field):
    """
    """
    def __init__(self):
        self.size = 2
        self.__defined = None
        
    @property
    def defined(self):
        return self.__defined
        
    @defined.setter
    def defined(self, defined):
        self.__defined = defined
        
    def _clean_func(self, field):
        if not isinstance(field, list):
            field = [field]
        if len(field) != self.size:
            field = None
        return field
        
    def _parse_func(self, field):
        if not field == self.defined:
            raise ValueError('Invaild DataLengthField Value')
        return field 
        
    def _clean(self, field):
        field = self._clean_func(field)
        return field
    
    def _parse(self, field):
        field = self._parse_func(field)
        return field

    def parse(self, field):
        field = self._clean(field)
        parsed = self._parse(field)
        return parsed      
        
        
class KindField(Field):
    """
    """
    def __init__(self):
        self.norm = sensomics_utils.kind_field_mapping
        self.size = 2
        self.__defined = None
        self.__parse_func = lambda field: field
        
    @property
    def defined(self):
        return self.__defined
        
    @defined.setter
    def defined(self, defined):
        self.__defined = defined
        
    @property
    def parse_func(self):
        return self.__parse_func
        
    @parse_func.setter
    def parse_func(self, parse_func):
        self.__parse_func = parse_func 
        
    def _clean_func(self, field):
        if not isinstance(field, list):
            field = [field]
        if len(field) != self.size:
            raise ValueError('Invaild KindField Value')
        return field   
       
    def _clean(self, field):
        field = self._clean_func(field)
        return field
    
    def _parse(self, field):
        field = self.parse_func(field)
        return field

    def parse(self, field):
        field = self._clean(field)
        parsed = self._parse(field)
        return parsed        

        
class UserDefinedField(Field):
    """
    """
    def __init__(self):
        self.size = 1
        self.__defined = None
        self.__parse_func = lambda field: field
        
    @property
    def defined(self):
        return self.__defined
        
    @defined.setter
    def defined(self, defined):
        self.__defined = defined
        
    @property
    def parse_func(self):
        return self.__parse_func
        
    @parse_func.setter
    def parse_func(self, parse_func):
        self.__parse_func = parse_func 
        
    def _clean_func(self, field):
        if not isinstance(field, list):
            field = [field]
        if len(field) != self.size:
            raise ValueError('Invaild UserField Value')
        return field   
       
    def _clean(self, field):
        field = self._clean_func(field)
        return field
    
    def _parse(self, field):
        field = self.parse_func(field)
        return field

    def parse(self, field):
        field = self._clean(field)
        parsed = self._parse(field)
        return parsed       
        
        
class DataField(Field):
    """
    """
    def __init__(self):
        self.__size = None
        self.__clean_func = lambda field: field
        self.__parse_func = lambda field: field

    @property
    def size(self):
        return self.__size
        
    @size.setter
    def size(self, size):
        self.__size = size     
        
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
        
    def _clean(self, field):
        field = self.clean_func(field)
        return field
    
    def _parse(self, field):
        field = self.parse_func(field)
        return field

    def parse(self, field):
        field = self._clean(field)
        parsed = self._parse(field)
        return parsed                
        
        
class Frame(object):
    
    def __init__(self):
        pass
        
    @property
    def protocol_frame(self):
        protocol = {'Start_Frame_Offset':  0,           # 0
                    'Data_Length_Offset':  slice(1,3),  # 1, 2
                    'ID_Offset':           slice(3,5),  # 3, 4         
                    'User_Defined_Offset': 5,
                    'Data_Field_Offset':   6}
        return protocol


class HrCurrentFrame(Frame):

    def __init__(self):
        super(HrCurrentFrame, self).__init__()
        self.start_frame_field = StartFrameField()
        self.data_length_field = DataLengthField()
        self.kind_field = KindField()
        self.user_defined_field = UserDefinedField()
        self.data_field = DataField()
        
        self.start_frame_field.defined = [int(0xab)]
        self.data_length_field.defined = [int(0x00), int(0x04)]
        self.kind_field.defined        = [int(0xff), int(0x84)]
        
        self.kind_field.parse_func = self._parse_kind_func
        self.data_field.clean_func = self._clean_data_func
        self.data_field.parse_func = self._parse_data_func

    @property
    def protocol_data(self):
        protocol = {'HR_Value_Offset':     6}
        return protocol

    def _clean_data_func(self, field):
        if not isinstance(field, list):
            field = [field]        
        return field
    
    def _parse_kind_func(self, field):
        if field == self.kind_field.defined:
            field = 'hr'
        else:
            field = None
        return field    
        
    def _parse_data_func(self, field):
        data_offset = self.protocol_frame['Data_Field_Offset']
        hr = field[self.protocol_data['HR_Value_Offset']-data_offset]
        field = [hr]
        return field   
        
    def _clean(self, frame):
        if not (isinstance(frame, list) and len(frame) == 7):
            return ErFrame().parse(frame)
        
        start_frame_vals = frame[self.protocol_frame['Start_Frame_Offset']] # frame[0]
        start_frame_parsed = self.start_frame_field.parse(start_frame_vals)
        if not start_frame_parsed:
            return ErFrame().parse(frame)
        
        data_length_vals = frame[self.protocol_frame['Data_Length_Offset']] # frame[1-2]
        data_length_parsed = self.data_length_field.parse(data_length_vals)
        if not data_length_parsed:
            return ErFrame().parse(frame)       
        return frame
            
    def _parse(self, frame):
        data_offset = self.protocol_frame['Data_Field_Offset']
        kind_vals = frame[self.protocol_frame['ID_Offset']] # frame[3-4]
        kind_parsed = self.kind_field.parse(kind_vals)
        data_vals = frame[data_offset:]  # frame[6]
        data_parsed = self.data_field.parse(data_vals)
        frame = {'kind': kind_parsed, 'data': data_parsed}
        frame = [frame]
        return frame
        
    def parse(self, frame):
        frame = self._clean(frame)
        if isinstance(frame, ErFrame):
            return frame
        parsed = self._parse(frame)
        return parsed
        
        
class AcCurrentFrame(Frame):

    def __init__(self):
        super(AcCurrentFrame, self).__init__()
        self.start_frame_field = StartFrameField()
        self.data_length_field = DataLengthField()
        self.kind_field = KindField()
        self.user_defined_field = UserDefinedField()
        self.data_field = DataField()
        
        self.start_frame_field.defined = [int(0xab)]
        self.data_length_field.defined = [int(0x00), int(0x11)] # 0, 17
        self.kind_field.defined        = [int(0xff), int(0xa1)] # 255, 161
        
        self.kind_field.parse_func = self._parse_kind_func
        self.data_field.clean_func = self._clean_data_func
        self.data_field.parse_func = self._parse_data_func
        
    @property
    def protocol_frame(self):
        protocol = {'Start_Frame_Offset':  0,           # 0
                    'Data_Length_Offset':  slice(1,3),  # 1, 2
                    'ID_Offset':           slice(3,5),  # 3, 4         
                    'Data_Field_Offset':   5}
        return protocol
        
    @property
    def protocol_data(self):
        protocol = {'X_Sign_Offset':  9,
                    'X_High_Offset': 10,
                    'X_Low_Offset' : 11,
                    'Y_Sign_Offset': 12,
                    'Y_High_Offset': 13,
                    'Y_Low_Offset' : 14,        
                    'Z_Sign_Offset': 15,
                    'Z_High_Offset': 16,
                    'Z_Low_Offset' : 17,
                    'P_High_Offset': 18,
                    'P_Low_Offset' : 19}
        return protocol

    def _parse_kind_func(self, field):
        if field == self.kind_field.defined:
            field = ['ac', 'ppg']
        else:
            field = None
        return field
            
    def _clean_data_func(self, field):
        if not isinstance(field, list):
            field = [field]
        return field
        
    def _parse_data_func(self, field):        
        ## XYZ-Axis Field
        data_offset = self.protocol_frame['Data_Field_Offset']
        # X-Axis
        x1 = field[self.protocol_data['X_Sign_Offset']-data_offset]
        x2 = field[self.protocol_data['X_High_Offset']-data_offset]
        x3 = field[self.protocol_data['X_Low_Offset']-data_offset]
        x_axis = sensomics_utils.function_byte_shift_sign([x1, x2, x3])
        # Y-Axis
        y1 = field[self.protocol_data['Y_Sign_Offset']-data_offset]
        y2 = field[self.protocol_data['Y_High_Offset']-data_offset]
        y3 = field[self.protocol_data['Y_Low_Offset']-data_offset]
        y_axis = sensomics_utils.function_byte_shift_sign([y1, y2, y3])
        # Z-Axis
        z1 = field[self.protocol_data['Z_Sign_Offset']-data_offset]
        z2 = field[self.protocol_data['Z_High_Offset']-data_offset]
        z3 = field[self.protocol_data['Z_Low_Offset']-data_offset]
        z_axis = sensomics_utils.function_byte_shift_sign([z1, z2, z3])
        field1 = [x_axis, y_axis, z_axis]
        ## PPG Field
        p1 = field[self.protocol_data['P_High_Offset']-data_offset]
        p2 = field[self.protocol_data['P_Low_Offset']-data_offset]
        ppg = sensomics_utils.function_byte_shift([p1, p2])
        field2 = [ppg]
        field = [field1, field2]     
        return field 
        
    def _clean(self, frame):
        if not (isinstance(frame, list) and len(frame) == 20):
            return ErFrame().parse(frame)
       
        start_frame_vals = frame[self.protocol_frame['Start_Frame_Offset']] # frame[0]
        start_frame_parsed = self.start_frame_field.parse(start_frame_vals)
        if not start_frame_parsed:
            return ErFrame().parse(frame)
       
        data_length_vals = frame[self.protocol_frame['Data_Length_Offset']] # frame[1-2]
        data_length_parsed = self.data_length_field.parse(data_length_vals)
        if not data_length_parsed:
            return ErFrame().parse(frame)
        return frame
            
    def _parse(self, frame):
        data_offset = self.protocol_frame['Data_Field_Offset']
        kind_vals = frame[self.protocol_frame['ID_Offset']] # frame[3-4]
        data_vals = frame[data_offset:]  # frame[5:-1]
        kind_parsed = self.kind_field.parse(kind_vals)
        kind_parsed1 = kind_parsed[0]
        kind_parsed2 = kind_parsed[1]
        data_parsed = self.data_field.parse(data_vals)
        data_parsed1 = data_parsed[0] 
        data_parsed2 = data_parsed[1]
        frame1 = {'kind': kind_parsed1, 'data': data_parsed1}
        frame2 = {'kind': kind_parsed2, 'data': data_parsed2}
        frame = [frame1, frame2]
        return frame
        
    def parse(self, frame):
        frame = self._clean(frame)
        if isinstance(frame, ErFrame):
            return frame
        parsed = self._parse(frame)
        return parsed    

        
class HrStoreFrame(Frame):

    def __init__(self):
        super(HrStoreFrame, self).__init__()
        self.start_frame_field = StartFrameField()
        self.data_length_field = DataLengthField()
        self.kind_field = KindField()
        self.user_defined_field = UserDefinedField()
        self.data_field = DataField()
        
        self.start_frame_field.defined  = [int(0xab)]
        self.data_length_field.defined  = [int(0x00), int(0x0a)] # [0, 10]
        self.kind_field.defined         = [int(0xff), int(0x51)] # [255, 81]
        self.user_defined_field.defined = [int(0x11)]            # 17

        self.kind_field.parse_func = self._parse_kind_func
        self.user_defined_field.parse_func = self._parse_user_defined_func
        self.data_field.clean_func = self._clean_data_func
        self.data_field.parse_func = self._parse_data_func

    @property
    def protocol_data(self):
        protocol = {'HR_Value_Offset':     11}
        return protocol

    def _parse_kind_func(self, field):
        if field == self.kind_field.defined:
            field = 'store'
        else:
            field = None
        return field
        
    def _parse_user_defined_func(self, field):
        if field == self.user_defined_field.defined:
            field = 'hr'
        else:
            field = None
        return field      
        
    def _clean_data_func(self, field):
        if not isinstance(field, list):
            field = [field]
        return field
        
    def _parse_data_func(self, field):
        data_offset = self.protocol_frame['Data_Field_Offset']
        hr = field[self.protocol_data['HR_Value_Offset']-data_offset]
        field = [hr]
        return field
        
    def _clean(self, frame):
        if not (isinstance(frame, list) and len(frame) == 13):
            return ErFrame().parse(frame)
            
        start_frame_vals = frame[self.protocol_frame['Start_Frame_Offset']] # frame[0]
        start_frame_parsed = self.start_frame_field.parse(start_frame_vals)
        if not start_frame_parsed:
            return ErFrame().parse(frame)
            
        data_length_vals = frame[self.protocol_frame['Data_Length_Offset']] # frame[1-2]
        data_length_parsed = self.data_length_field.parse(data_length_vals)
        if not data_length_parsed:
            return ErFrame().parse(frame)
            
        kind_vals = frame[self.protocol_frame['ID_Offset']] # frame[3-4]
        kind_parsed = self.kind_field.parse(kind_vals)
        if not kind_parsed:
            return ErFrame().parse(frame)
        return frame
        
    def _parse(self, frame):
        # parse kind
        user_vals = frame[self.protocol_frame['User_Defined_Offset']] # frame [5]
        user_parsed = self.user_defined_field.parse(user_vals)     
        # parse data
        data_offset = self.protocol_frame['Data_Field_Offset']        
        data_vals = frame[data_offset:]  # frame[6]
        data_parsed = self.data_field.parse(data_vals)
        frame = {'kind': user_parsed, 'data': data_parsed}
        frame = [frame]
        return frame
        
    def parse(self, frame):
        frame = self._clean(frame)
        if isinstance(frame, ErFrame):
            return frame
        parsed = self._parse(frame)
        return parsed
        

class StStoreFrame(Frame):

    def __init__(self):
        super(StStoreFrame, self).__init__()
        self.start_frame_field = StartFrameField()
        self.data_length_field = DataLengthField()
        self.kind_field = KindField()
        self.user_defined_field = UserDefinedField()
        self.data_field = DataField()
        
        self.start_frame_field.defined  = [int(0xab)]
        self.data_length_field.defined  = [int(0x00), int(0x11)] # [0, 17]
        self.kind_field.defined         = [int(0xff), int(0x51)] # [255, 81]
        self.user_defined_field.defined = [int(0x20)]            # 32

        self.kind_field.parse_func = self._parse_kind_func
        self.user_defined_field.parse_func = self._parse_user_defined_func
        self.data_field.clean_func = self._clean_data_func
        self.data_field.parse_func = self._parse_data_func

    @property
    def protocol_data(self):
        protocol = {'Step_Byte1_Offset':      6,
                    'Step_Byte2_Offset':      7,
                    'Step_Byte3_Offset':      8,
                    'Calorie_Byte1_Offset':   9,
                    'Calorie_Byte2_Offset':  10,
                    'Calorie_Byte3_Offset':  11}
        return protocol

    def _parse_kind_func(self, field):
        if not field == self.kind_field.defined:
            field = 'store'
        else:
            field = None
        return field
        
    def _parse_user_defined_func(self, field):
        if not field == self.kind_field.defined:
            field = ['step', 'calorie']
        else:
            field = None
        return field        
        
    def _clean_data_func(self, field):
        if not isinstance(field, list):
            field = [field]        
        if len(field) != self.data_length_field.defined:
            field = None
        return field
        
    def _parse_data_func(self, field):
        data_offset = self.protocol_frame['Data_Field_Offset']
        # Step
        s1 = field[self.protocol_data['Step_Byte1_Offset']-data_offset]
        s2 = field[self.protocol_data['Step_Byte2_Offset']-data_offset]
        s3 = field[self.protocol_data['Step_Byte3_Offset']-data_offset]
        step = sensomics_utils.function_byte_shift(s1, s2, s3)
        field1 = [step]       
        # Calorie
        c1 = field[self.protocol_data['Calorie_Byte1_Offset']-data_offset]
        c2 = field[self.protocol_data['Calorie_Byte2_Offset']-data_offset]
        c3 = field[self.protocol_data['Calorie_Byte3_Offset']-data_offset]
        calorie = sensomics_utils.function_byte_shift(c1, c2, c3)
        field2 = [calorie]
        field = [field1, field2]
        return field
        
    def _clean(self, frame):
        if not (isinstance(frame, list) and len(frame) == 20):
            return ErFrame().parse(frame)
            
        start_frame_vals = frame[self.protocol_frame['Start_Frame_Offset']] # frame[0]
        start_frame_parsed = self.start_frame_field.parse(start_frame_vals)
        if not start_frame_parsed:
            return ErFrame().parse(frame)
            
        data_length_vals = frame[self.protocol_frame['Data_Length_Offset']] # frame[1-2]
        data_length_parsed = self.data_length_field.parse(data_length_vals)
        if not data_length_parsed:
            return ErFrame().parse(frame)
            
        kind_vals = frame[self.protocol_frame['ID_Offset']] # frame[3-4]
        kind_parsed = self.kind_field.parse(kind_vals)
        if not kind_parsed:
            return ErFrame().parse(frame)
        return frame
        
    def _parse(self, frame):
        # parse kind
        user_vals = frame[self.protocol_frame['User_Defined_Offset']] # frame[3-4]
        user_parsed = self.user_defined_field_field.parse(user_vals)
        user_parsed1 = user_parsed[0]
        user_parsed2 = user_parsed[1]
        # parse data
        data_offset = self.protocol_frame['Data_Field_Offset']
        data_vals = frame[data_offset:]  # frame[5:-1]
        data_parsed = self.data_field.parse(data_vals)
        data_parsed1 = data_parsed[0] 
        data_parsed2 = data_parsed[1]
        frame1 = {'kind': user_parsed1, 'data': data_parsed1}
        frame2 = {'kind': user_parsed2, 'data': data_parsed2}
        frame = [frame1, frame2]
        return frame
        
    def parse(self, frame):
        frame = self._clean(frame)
        if isinstance(frame, ErFrame):
            return frame
        parsed = self._parse(frame)
        return parsed  

        
class ErFrame(object):
    
    def __init__(self):
        pass
    
    def parse(self, frame):
        return {'kind': 'uk', 'data': None}


global HRCURRENT
global ACCURRENT
global HRSTORE
global STSTORE
global TIMEFIELD

HRCURRENT = HrCurrentFrame()
ACCURRENT = AcCurrentFrame()
HRSTORE = HrStoreFrame()
STSTORE = StStoreFrame()
TIMEFIELD = TimeField()



def FrameSelect(steam):
    
    time_frame = steam[0] # str
    data_frame = steam[1] # list
    type_frame = steam[2] # list
    flag1 = type_frame[0]
    flag2 = type_frame[1]
    if flag1 == 132: # HrCurrent
        time_ = TIMEFIELD.parse(time_frame)
        data_ = HRCURRENT.parse(data_frame)
        data_ = data_[0]
        frame = dict()
        frame.update(time_)
        frame.update(data_)
        frame = [frame]
        print('hr1')
    elif flag1 == 161: # AcCurrent
        time_ = TIMEFIELD.parse(time_frame)
        data_ = ACCURRENT.parse(data_frame)
        data_1 = data_[0]
        data_2 = data_[1]
        frame1 = dict()
        frame1.update(time_)
        frame1.update(data_1)
        frame2 = dict()
        frame2.update(time_)
        frame2.update(data_2)
        frame = [frame1, frame2]
        print('ac')
    elif flag1 == 81 and flag2 == 17:
        time_ = TIMEFIELD.parse(time_frame)
        data_ = HRSTORE.parse(data_frame)
        data_ = data_[0]
        frame = dict()
        frame.update(time_)
        frame.update(data_)
        frame = [frame]
        print('hr2')
    elif flag1 == 81 and flag2 == 32:
        time_ = TIMEFIELD.parse(time_frame)
        data_ = STSTORE.parse(data_frame)
        data_1 = data_[0]
        data_2 = data_[1]
        frame1 = dict()
        frame1.update(time_)
        frame1.update(data_1)
        frame2 = dict()
        frame2.update(time_)
        frame2.update(data_2)
        frame = [frame1, frame2]
        print('st')
    else:
        time_ = {'time': None}
        data_ = {'kind': 'uk', 'data': None}
        frame = dict()
        frame.update(time_)
        frame.update(data_)
        frame = [frame]
        print('er')
    return frame