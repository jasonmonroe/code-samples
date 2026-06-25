# src/class_name_filter.py

import inspect
import logging

class ClassNameFilter(logging.Filter):
    def filter(self, record) -> bool:
        """
        Filters out class name for logging data.
        Default value if the log isn't called from inside a class method.
        """
        record.classname = "Module"
        frame = inspect.currentframe()

        while frame:
            filename = frame.f_code.co_filename
            func_name = frame.f_code.co_name
       
            # Skip standard logging library files
            if "logging" in filename:
                frame = frame.f_back
                continue
                
            # Skip this filter's own internal method frame
            if func_name == "filter" or "ClassNameFilter" in func_name:
                frame = frame.f_back
                continue
                
            # Check for the user's class instance 'self'
            if 'self' in frame.f_locals:
                obj = frame.f_locals['self']
                # Ensure 'self' is not the filter instance itself
                if obj.__class__.__name__ != "ClassNameFilter":
                    record.classname = obj.__class__.__name__
                    break
                
            frame = frame.f_back
            
        return True
