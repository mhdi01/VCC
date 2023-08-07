import uuid
from sqlalchemy.orm import Session
from cpmpy import *



class TableRepository:

    entity:object = NotImplementedError
    db:Session = NotImplementedError

    def __init__(self, db:Session, entity:object):
        self.db = db
        self.entity = entity

    def find_by_id(self, id:int):
        return self.db.query(self.entity).filter(self.entity.id==id).first()

    def set_attrs(self, entity, updated_attrs, 
    throw_error_if_data_type_not_same:bool = True, 
    throw_error_if_attr_not_in_entity:bool = True):

        # simple one
        # for attr in updated_attrs:
        #     has_attr = hasattr(entity, attr)
        #     if has_attr:
        #         setattr(entity, attr, updated_attrs[attr])

        # complex one
        attrs = []
        for attr in updated_attrs:
            has_attr = hasattr(entity, attr)
            if has_attr:
                expected_type = type(getattr(entity, attr))
                inputed_type = type(updated_attrs[attr])
                is_same_type =  inputed_type == expected_type
                if is_same_type:
                    attrs.append(attr)
                else:
                    print(str(inputed_type))
                    if str(expected_type)[1:5] == 'enum' or str(inputed_type) == "<class 'set'>":
                        attrs.append(attr)
                    else:
                        raise TypeError(f"The expected value type of attr '{attr}' is '{expected_type}' of entity, where inputted value type is '{inputed_type}'.")
            else:
                if throw_error_if_attr_not_in_entity:
                    raise TypeError(f"attr '{attr}' is not found in entity.")
                  
        for attr in attrs:
            setattr(entity, attr, updated_attrs[attr])   
        return attrs
  
  
def id_generator():
    return "{0}-{1}-{2}-{3}-{4}".format(uuid.uuid4().hex[:8],uuid.uuid4().hex[:4],uuid.uuid4().hex[:4],uuid.uuid4().hex[:4],uuid.uuid4().hex[:12])


def solve_maintenance_conflict(start_time, end_time, maintenance_start_time, maintenance_end_time):
    # Check for overlaps using cpmpy
    overlap_model = Model()

    # Variables to represent the start and end times of the new schedule
    schedule_start_var = IntVar(0, int(start_time))
    schedule_end_var = IntVar(0, int(end_time))

    # Constraint: schedule_end_var should be greater than or equal to schedule_start_var
    overlap_model += schedule_end_var >= schedule_start_var

    # Constraint: new schedule should not overlap with cluster maintenance time
    overlap_model += (schedule_start_var.ub >= int(maintenance_end_time)) | (schedule_end_var.ub <= int(maintenance_start_time))

    print(overlap_model.solve())
    # Check if the model is satisfiable (i.e., no overlap exists)
    if overlap_model.solve():
        return True
    else:
        return False
