from ete import Tree
from wgdtree.retention_rates import rrates, place_wgd


def run(list_of_gene_trees, species_tree):

    results_dic = {}

    for l in species_tree.get_leaves():
        resuls_dic[l] = []


    clean_tree = species_tree.copy()
    
    for n in clean_tree.iter_descendants():
        if('WGD' in n.features):
            n.remove_feature('WGD')

    
    paired_trees = []
    
    
    for n in species_tree.traverse():
        if('WGD' in n.features and n.WGD == 'Y'):
            
            for x in n.iter_descendants():
                if('WGD' in n.features and n.WGD == 'Y'):
                                        
                    tmp_tree = clean_tree.copy()
                    
                    n1 = tmp_tree&n.name
                    
                    n2 = tmp_tree&x.name
                    
                    n1.add_feature('WGD', 'Y')
                    
                    n2.add_feature('WGD', 'Y')
                    
                    paired_trees.append(tmp_tree)
                    
                    leaves = []
                    
                    for l in x.get_leaves():
                        leaves.append(l.name.split('_')[0])
                            
                    pSpecies.append(leaves)

                    
    i=0
    for t in paired_trees:  #for each pair of events
        for s in pSpecies[i]: #for each species present for the pair
                l_poss = 0
                r_poss = 0
                l = 0
                r = 0
            for g in list_of_gene_trees: #for each gene tree
                tmp_gene = place_wgd(species_tree,g)
                    
                results = rrates(tmp_gene,s)

                l_poss += results
                r_poss += results
                l += results
                r += results
                
            results_dic[s].append((l/l_poss,r/r_poss))
            
            
            
        i+=1
    
    return resuls_dic
    
