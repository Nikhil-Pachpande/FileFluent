from converter import Converter


class ConverterFactory:
    @staticmethod
    def get_converter(input_format, output_format, input_path, output_path):
        """
        Factory method to return the appropriate converter instance based on input and output file formats.

        Parameters:
            input_format (str): The format of the input file.
            output_format (str): The desired output format.
            input_path (str): Path to the input file.
            output_path (str): Path to save the converted file.

        Returns:
            Converter: An instance of the `Converter` class configured with the given parameters.
        """
        return Converter(input_path, output_path, output_format)
