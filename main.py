import main_bottleneck

def get_file():
    
    while True:
        filename = ""
        try:
            filename = input("enter a filename: ")
            filename = "Scans/" + filename
            open(filename)
            break
        except FileNotFoundError:
            print("File not found")
        
    return filename
    
    

def main():
    
    filename = get_file()
    
    main_bottleneck.bottleneck(filename)
    
main()

