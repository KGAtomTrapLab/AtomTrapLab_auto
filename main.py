import main_bottleneck
import logging

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
    
    logging.basicConfig(filename="example.log", level=logging.DEBUG)

    filename = get_file()
    
    main_bottleneck.bottleneck(filename)



if __name__ == "__main__":
    main()
