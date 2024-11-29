from converter import Converter


class ConverterFactory:
    @staticmethod
    def get_converter(input_format, output_format, input_path, output_path):
        """
        This method will call the correct converter on the basis of the input and output file format
        """
        # to return a converter based on the type of input format
        converter = Converter(input_path, output_path, output_format)

        if input_format in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
            return converter.convert_image()
        elif input_format == 'pdf':
            return converter.convert_pdf()
        elif input_format == 'docx':
            return converter.convert_docx()
        elif input_format == 'csv':
            return converter.convert_csv()
        else:
            raise ValueError(f"Unsupported input format for conversion: {input_format}")
