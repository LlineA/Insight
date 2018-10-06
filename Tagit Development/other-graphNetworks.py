# -*- coding: utf-8 -*-
"""
Created on Sat Sep 29 18:00:54 2018

@author: Graccolab
"""

import networkx as nx
import matplotlib.pyplot as plt

G = nx.petersen_graph()
plt.subplot(121)


nx.draw(G, with_labels=True, font_weight='bold')
#%%
plt.subplot(122)

nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')

#%%
options = {
    'node_color': 'black',
    'node_size': 100,
    'width': 3,
}
plt.subplot(221)

nx.draw_random(G, **options)

#%%
plt.subplot(222)

nx.draw_circular(G, **options)
#%%
plt.subplot(223)

nx.draw_spectral(G, **options)
#%%
plt.subplot(224)

nx.draw_shell(G, nlist=[range(5,10), range(5)], **options)

G = nx.dodecahedral_graph()
shells = [[2, 3, 4, 5, 6], [8, 1, 0, 19, 18, 17, 16, 15, 14, 7], [9, 10, 11, 12, 13]]
nx.draw_shell(G, nlist=shells, **options)