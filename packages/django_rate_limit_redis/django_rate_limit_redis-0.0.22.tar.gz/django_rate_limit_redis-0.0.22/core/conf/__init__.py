from django.core.cache import cache

from core.models import SettingsModel


class Settings(object):

    def __getattr__(self, attr):
        '''
        Produces features from DB/Cache and converts to specified type
        the boolean part is taken from:
        https://github.com/capless/envs/blob/68bee09ef3224c2d7d94467f65173fbc1ae782bc/envs/__init__.py#L21

        :param attr: Settings attribute
        :return value: str, int, float, bool
        '''

        value_dict = cache.get(attr)
        if not value_dict:
            value_dict = self.set_cache_value(attr)
        value = value_dict.get('value')
        type_value = value_dict.get('type')
        if type_value == 'str':
            value = str(value)
        elif type_value == 'int':
            value = int(value)
        elif type_value == 'float':
            value = float(value)
        elif type_value == 'bool':
            true_vals = ('True', 'true', 1, '1')
            false_vals = ('False', 'false', 0, '0')
            if value in true_vals:
                value = True
            elif value in false_vals:
                value = False
            else:
                raise ValueError('This value is not a boolean value.')

        return value

    def set_cache_value(self, attr):
        try:
            obj = SettingsModel.objects.get(attribute_name=attr)
        except SettingsModel.DoesNotExist as ex:
            raise AttributeError(f"'Settings' object has no attribute '{attr}'\n"
                                 f"Exception: {ex}")
        value_dict = {
            'value': obj.attribute_value,
            'type': obj.attribute_type
        }
        cache.set(
            obj.attribute_name,
            value_dict
        )
        return value_dict
