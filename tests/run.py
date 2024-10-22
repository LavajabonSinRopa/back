import pytest
import sys


if __name__ == "__main__":
    # Get command line arguments
    args = sys.argv[1:]
    
    # Default pytest arguments
    pytest_args = [
        "tests",
        "-v",
        "--tb=short"
    ]
    
    # Add any additional arguments passed to this script
    pytest_args.extend(args)
    
    # Run pytest with the constructed arguments
    sys.exit(pytest.main(pytest_args))