from workflows import setup,extract,transform,load,teardown

def main(): 
    setup()
    extract()
    transform()
    load()
    teardown()

if __name__ == '__main__':
    main()