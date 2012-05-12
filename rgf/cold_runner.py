import os, sys

if __name__ == '__main__':
    rgf_path = os.path.dirname(os.path.dirname(__file__))
    if rgf_path not in sys.path:
        sys.path.insert(0, rgf_path)
    from rgf.core.runner import main
    exit = main()
    if exit:
        sys.exit(exit)

