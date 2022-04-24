import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

import feature_handler
import helper
def main():
    helper.check_update()
    while True:
        feature_handler.menu()
        print()

try:
    main()
except KeyboardInterrupt:
    exit()
    