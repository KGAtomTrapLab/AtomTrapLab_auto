import main_bottleneck

def main():
    
    filename = input("enter a filename: ")
    
    filename = "scans/" + filename
    
    main_bottleneck.bottleneck(filename)
    

main()

