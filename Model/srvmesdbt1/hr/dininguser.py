class DiningUser:
    class user_add_edit:
        def __init__(self, usr):
            # print(f'usr: {type(usr)}')
            for key, value in usr.items():
                setattr(self, key, value)

    # class implicit_user_add_edit(user_add_edit):
    #     def __init__(self, usr):
    #         super().__init__(usr)
    #         self.ModifyBy=usr['musr']