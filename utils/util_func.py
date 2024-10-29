class UtilFunc:

    @staticmethod
    def list_tuple_to_dict(list_tuple):
        dict_data = {k: [v for _, v in list_tuple if _ == k] for k, _ in list_tuple}
        return dict_data
