import pandas as pd
import net

votes_data = pd.read_excel('ESC2018_GF.xlsx',sheetname='Combined result')

votes_melted = votes_data.melt(
    ['Rank','Running order','Country','Total'],
    var_name = 'Source Country',value_name='points')    
    
G = nx.from_pandas_edgelist(votes_melted, 
                            source='Source Country',
                            target='Country',
                            edge_attr='points',
                            create_using=nx.DiGraph())
                            
nx.draw_networkx(G)