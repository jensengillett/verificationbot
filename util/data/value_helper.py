class ValueHelper:

    @staticmethod
    def list_tuple_value(tuple_list: list, val_pos: int):
        if not len(tuple_list) > 0:
            return None
        return tuple_list[0][val_pos]
