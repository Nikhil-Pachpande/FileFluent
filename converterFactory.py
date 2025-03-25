from converter import Converter


class ConverterFactory:
    @staticmethod
    def get_converter(input_format: str, output_format: str, input_path: str, output_path: str) -> Converter:
        return Converter(input_path, output_path, output_format)