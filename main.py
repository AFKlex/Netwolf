import argparse
from src.Directory import * 
from src.Domain import * 
from src.Files import * 
from src.WebReconGraph import * 

parser = argparse.ArgumentParser(description="Netwolf")


def define_arguments():
    # Define Arguments Here
	#--------------------------------------------
	
	parser.add_argument('-base_domain', type=str, required=True, help='Provide the base domain')
	
	
	#--------------------------------------------
	# Parse the command line arguments
	args = parser.parse_args()
	# Access the values of the arguments
	return args


if __name__ == '__main__':
    args = define_arguments()

    base_domain = Domain(args.base_domain)

    print("Welcome to Netwolf") 
    

    with open ('./wordlists/subdomains.txt') as file: 
        subdomains = file.read().splitlines()


    base_domain.fuzz_subdomains(subdomains)

    print(base_domain.subdomains)
        
    graph = WebReconGraph()

    base_domain.add_domains_to_graph(graph)

    graph.draw_graph()


