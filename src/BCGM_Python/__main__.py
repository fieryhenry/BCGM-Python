from BCGM_Python import feature_handler, helper


def main():
    helper.check_update()
    while True:
        feature_handler.menu()
        print()


try:
    main()
except KeyboardInterrupt:
    exit()
