import sys
import argparse
from utils.io_handler import ConfigReader, ResultWriter
from calculator import OptionCalculator


def main():
    # Setup command line arguments
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

    # Config file path - required
    parser.add_argument(
        '--config', '-c',
        required=True,
        help='Path to config json file'
    )

    # Where to save output (optional - defaults to console)
    parser.add_argument(
        '--output', '-o',
        default=None,
        help='Path to output file (default: prints to console)'
    )

    # Output format if saving to file
    parser.add_argument(
        '--format', '-f',
        choices=['json', 'txt'],
        default='json',
        help='Output format (default: json)'
    )

    # Option to skip Greeks if you just want the price
    parser.add_argument(
        '--no-greeks',
        action='store_true',
        help='Skip Greeks calculation (faster if you only need price)'
    )

    # Simple mode - just show the essentials
    parser.add_argument(
        '--simple',
        action='store_true',
        help='Simple output - price only, no Greeks'
    )

    args = parser.parse_args()

    try:
        # Load the config file
        print(f"Reading configuration from: {args.config}")
        config = ConfigReader.read_config(args.config)

        # Make sure the config has everything we need
        is_valid, error_msg = ConfigReader.validate_config(config)
        if not is_valid:
            print(f"Error: {error_msg}", file=sys.stderr)
            sys.exit(1)

        # Do the actual calculation
        print("Calculating price...")
        calculator = OptionCalculator(config)
        results = calculator.calculate(compute_greeks=not args.no_greeks)

        # Show or save the results
        ResultWriter.write_results(
            results,
            output_path=args.output,
            format=args.format,
            detailed=not args.simple
        )

        return 0

    # Handle various error cases
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    except Exception as e:
        # Catch-all for unexpected errors - print full traceback for debugging
        print(f"Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())