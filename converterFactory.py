from converter import Converter


class ConverterFactory:
    @staticmethod
    def get_converter(input_format, output_format, input_path, output_path):
        """
        This method will call the correct converter on the basis of the input and output file format
        """
        # to return a converter based on the type of input format
        converter = Converter(input_path, output_path, output_format)
        return converter
