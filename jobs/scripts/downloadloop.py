debug = False

exec(open("../../parameters/parameters.py").read())
exec(open("../../scripts/path.py").read())
exec(open("../../scripts/setup.py").read())
exec(open("../../scripts/functions.py").read())

if __name__ == '__main__':

    print("Running 01.py")
    exec(open("../../scripts/01.py").read())

    print("Running 02.py")
    exec(open("../../scripts/02.py").read())