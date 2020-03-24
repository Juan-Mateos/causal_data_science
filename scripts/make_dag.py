import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import networkx as nx

def create_graph(node_df,edges,directed=True):
    '''
    Function to create a graph.
    
    Args:
        node_df (df) is a df with the nodes, their positions and labels
        edges (list) is a list of tuples where every element is a pair of nodes describing an edge. 
            element 0 is the source and element 1 is the target
        directed (bool) whether the network is directed or undirected
    
    '''
    if directed==True:
        G = nx.DiGraph()
        
    else:
        G = nx.Graph()

    for rid,r in node_df.iterrows():
        G.add_node(rid,pos=(r['x'],r['y']))


    G.add_edges_from(edges)
            

    return(G)

class Dag():
    '''
    A small class to plot dags.
    
    
    '''
    
    def __init__(self,node_df,edges,outcome='y',treatment='x'):
        '''
        Initialises the class.
        
        Args:
            node_df (df) is a df with the nodes, their positions and labels
            edges (list) is a list of tuples where every element is a pair of nodes describing an edge. 
                element 0 is the source and element 1 is the target
            outcome (str) is the label for the outcome (we assume it is y)
            treatment (str) is the label for the outcome (we assume it is z)
        
        
        '''
        
        self.node_df = node_df
        self.edges = edges
        self.outcome = outcome
        self.treatment = treatment
        
        labels_to_nodes = {v:k for k,v in node_df['label'].to_dict().items()}
        self.edges_unlabelled = [[labels_to_nodes[x] for x in t] for t in edges]
        
        self.node_label_lookup = labels_to_nodes
        
    def plot_dag(self,node_c='lightgrey'):
        '''
        Plots the dag
        
        '''
        
        G = create_graph(self.node_df,self.edges_unlabelled,directed=True)
        
        pos=nx.get_node_attributes(G,'pos')
        
        nx.draw(G,pos,node_color=node_c,edgecolors='black')
        
        nx.draw_networkx_labels(G,pos,self.node_df['label'],font_color='black')
        
        
    def plot_parents(self,child_node,node_c='lightgrey'):
        '''
        Plots the DAG using different colours for a child node and its parent
        
        Args:
            child_node (str) is the label for the child node
        
        '''
        
        node_label_lu = self.node_label_lookup
        
        G = create_graph(self.node_df,self.edges_unlabelled,directed=True)
        
        pos=nx.get_node_attributes(G,'pos')
        
        preds = list(G.predecessors(node_label_lu[child_node]))
        
        nx.draw(G,pos,node_color=['aquamarine' if x==node_label_lu[child_node] else 'coral' if x in preds else node_c for 
                                 x in G.nodes],edgecolors='black')
        
        nx.draw_networkx_labels(G,pos,self.node_df['label'],font_color='black')
        
    def plot_paths(self,node_c='lightgrey'):
        '''
        Plots all paths between outcome and treatment. This gets slightly involved...
        
        '''
        
        #Get the node and label lookup
        node_label_lu = self.node_label_lookup
        
        #Extract output and treatment (with their keys)
        o = node_label_lu[self.outcome]
        t = node_label_lu[self.treatment]
        
        #Create an undirected and directed version of the network (we can only get all paths in the undirected one)
        G = create_graph(node_df,test.edges_unlabelled,directed=False)
        Gd = create_graph(node_df,test.edges_unlabelled,directed=True)

        #This gets the positions (the coordinates we set in node df)
        pos=nx.get_node_attributes(Gd,'pos')
        
        #Extract simple paths between treatment and output
        simple_paths = list(nx.all_simple_paths(G,t,o))
                
        #Plot.
        #This is involved because we want to create a way to do subplots which is robust to the number of subplots.
        
        n_rows = int(np.ceil(len(simple_paths)/2))

        fig,ax = plt.subplots(nrows=n_rows,ncols=2,figsize=(6,n_rows*3))
        
        col = 0
        row = 0
        for n,x in enumerate(simple_paths):
    
    
            if col>1:
                col=0
                row+=1
            nx.draw(
                Gd,pos,node_color=['aquamarine' if n in x else 'lightgrey' for n in G.nodes],edgecolors='black',ax=ax[row][col])
            nx.draw_networkx_labels(Gd,pos,node_df['label'],font_color='black',ax=ax[row][col])
            col+=1

        if len(simple_paths)%2 !=0:
            ax[row][col].set_axis_off()
            
        fig.suptitle(f'All paths between treatment {self.treatment} and outcome {self.outcome}',y=1.01,size=14)

        plt.tight_layout()        