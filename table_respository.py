from sqlalchemy.orm import Session

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
  