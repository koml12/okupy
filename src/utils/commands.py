"""Functions to run when command line flags are specified."""

from settings import ARGS, KWARGS

def get_app_info(app_list, info_list):
    app_names = [app.__name__ for app in app_list]
    for app in info_list:
        if app in app_names:
            class_obj = next(i for i in app_list if i.__name__ == app)
            print(app)
            print('    {}'.format(class_obj.__doc__))
            print('    setup args: {}'.format(ARGS.get(app)))
            print('    setup kwargs: {}'.format(KWARGS.get(app)))
            print('')
            
            
        else:
            print('App {} does not exist'.format(app.__name__))

    