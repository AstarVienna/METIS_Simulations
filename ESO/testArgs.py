if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()


    parser.add_argument('--inputYAML', type=str,
                    help='input YAML File')
    parser.add_argument('--outputDir', type=str, 
                    help='output directory')

    args = parser.parse_args()
    print(args)
    
    if(args.inputYAML):
        inputYAML = args.inputYAML
    else:
        inputYAML = "recipes.yaml"
    if(args.outputDir):
        outputDir = args.outputDir
    else:
        outputDir = "./output/"

    print(outputDir,inputYAML)
    
