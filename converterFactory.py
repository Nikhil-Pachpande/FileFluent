from converter import Converter


class ConverterFactory:
    @staticmethod
    def get_converter(input_format, output_format, input_path, output_path):
        return Converter(input_path, output_path, output_format)
