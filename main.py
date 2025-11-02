import sys
import argparse
from utils.io_handler import ConfigReader, ResultWriter
from calculator import OptionCalculator


def main():

    parser = argparse.ArgumentParser(
        description='Option Calculator - Price various types of options',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate with default output (console)
  python main.py --config config/european_call.json

  # Save results to JSON file
  python main.py --config config/american_put.json --output results.json

  # Save results to text file
  python main.py --config config/asian_call.json --output results.txt --format txt

  # Skip Greeks calculation for faster results
  python main.py --config config/barrier_option.json --no-greeks

Supported Option Types:
  - European (call/put)
  - American (call/put)
  - Asian (call/put with arithmetic or geometric averaging)
  - Barrier (up-and-out, up-and-in, down-and-out, down-and-in)
        """
    )

    parser.add_argument(
        '--config', '-c',
        required=True,
        help='Path to config json file'
    )

    parser.add_argument(
        '--output', '-o',
        default=None,
        help='Path to output file (default: prints to console)'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['json', 'txt'],
        default='json',
        help='Output format (default: json)'
    )

    parser.add_argument(
        '--no-greeks',
        action='store_true',
        help='Skip Greeks (default: included)'
    )

    parser.add_argument(
        '--simple',
        action='store_true',
        help='Simple output (default: price only)'
    )

    args = parser.parse_args()

    try:
        # read config
        print(f"Reading configuration from: {args.config}")
        config = ConfigReader.read_config(args.config)

        # validate if it is correct
        is_valid, error_msg = ConfigReader.validate_config(config)
        if not is_valid:
            print(f"Error: {error_msg}", file=sys.stderr)
            sys.exit(1)

        # calc
        print("Calculating price...")
        calculator = OptionCalculator(config)
        results = calculator.calculate(compute_greeks=not args.no_greeks)

        # display results
        ResultWriter.write_results(
            results,
            output_path=args.output,
            format=args.format,
            detailed=not args.simple
        )

        return 0

    # if error
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())