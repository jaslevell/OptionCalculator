import json
from pathlib import Path


class ConfigReader:

    @staticmethod
    def read_config(config_path):

        config_file = Path(config_path)

        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_file, 'r') as f:
            config = json.load(f)

        return config

    @staticmethod
    def validate_config(config):

        required_fields = ['option_style', 'option_type', 'underlying_price', 'strike_price', 'time_to_maturity', 'volatility', 'risk_free_rate']

        missing_fields = [field for field in required_fields if field not in config]

        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"

        # Validate option_style
        valid_styles = ['european', 'american', 'asian', 'barrier']
        if config['option_style'].lower() not in valid_styles:
            return False, f"Invalid option_style. Must be one of: {', '.join(valid_styles)}"

        # Validate option_type
        valid_types = ['call', 'put']
        if config['option_type'].lower() not in valid_types:
            return False, f"Invalid option_type. Must be one of: {', '.join(valid_types)}"

        # Validate barrier
        if config['option_style'].lower() == 'barrier':
            if 'barrier_type' not in config or 'barrier_level' not in config:
                return False, "Barrier options require 'barrier_type' and 'barrier_level' fields"

        # Validate asian
        if config['option_style'].lower() == 'asian':
            if 'average_type' not in config:
                config['average_type'] = 'arithmetic'

        return True, None


class ResultWriter:

    @staticmethod
    def write_results(results, output_path=None, format='json', detailed=True):

        if output_path is None:
            ResultWriter.write_to_console(results, detailed)
        else:
            ResultWriter.write_to_file(results, output_path, format)

    @staticmethod
    def write_to_console(results, detailed=True):

        print("\n" + "="*60)
        print("RESULTS")
        print("="*60)

        print("\nInput Parameters:")
        print("-" * 60)
        params = results.get('parameters', {})
        for key, value in params.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")

        print("\n" + "-"*60)
        print(f"Option Price: ${results['price']:.4f}")
        print("-"*60)

        if detailed and 'greeks' in results and results['greeks'] is not None:
            print("\nGreeks:")
            print("-" * 60)
            greeks = results['greeks']
            print(f"  Delta:   {greeks.get('delta', 'N/A'):.6f}")
            print(f"  Gamma:   {greeks.get('gamma', 'N/A'):.6f}")
            print(f"  Vega:    {greeks.get('vega', 'N/A'):.6f}")
            print(f"  Theta:   {greeks.get('theta', 'N/A'):.6f}")
            print(f"  Rho:     {greeks.get('rho', 'N/A'):.6f}")

        print("="*60 + "\n")

    # Option if specified
    @staticmethod
    def write_to_file(results, output_path, format='json'):

        output_file = Path(output_path)

        if format.lower() == 'json':
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\nResults written to: {output_path}")

        elif format.lower() == 'txt':
            with open(output_file, 'w') as f:
                f.write("="*60 + "\n")
                f.write("OPTION CALCULATOR RESULTS\n")
                f.write("="*60 + "\n\n")

                f.write("Input Parameters:\n")
                f.write("-" * 60 + "\n")
                params = results.get('parameters', {})
                for key, value in params.items():
                    f.write(f"  {key.replace('_', ' ').title()}: {value}\n")

                f.write("\n" + "-"*60 + "\n")
                f.write(f"Option Price: ${results['price']:.4f}\n")
                f.write("-"*60 + "\n")

                if 'greeks' in results and results['greeks'] is not None:
                    f.write("\nGreeks:\n")
                    f.write("-" * 60 + "\n")
                    greeks = results['greeks']
                    f.write(f"  Delta:   {greeks.get('delta', 'N/A'):.6f}\n")
                    f.write(f"  Gamma:   {greeks.get('gamma', 'N/A'):.6f}\n")
                    f.write(f"  Vega:    {greeks.get('vega', 'N/A'):.6f}\n")
                    f.write(f"  Theta:   {greeks.get('theta', 'N/A'):.6f}\n")
                    f.write(f"  Rho:     {greeks.get('rho', 'N/A'):.6f}\n")

                f.write("="*60 + "\n")

            print(f"\nResults written to: {output_path}")

        else:
            raise ValueError(f"Unsupported output format: {format}")