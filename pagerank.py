from Retriever import Retriever
R = Retriever()

# pagerank updates for random names
res = R.fetch_objects(size=1000)
print(res.keys())

n_iterations = 10000
d = 0.7
n = float(len(res.keys()))

for i in range(n_iterations):
    # for each name...
    for k, v in res.items():
        
        # calculate pagerank...
        updated_prob = (1-d) * 1/n
        
        # ...by inspecting its parents
        for parent_node in v.parents:
            # parents with high pageranks but few outbound are best
            updated_prob += d * (parent_node.pagerank)/parent_node.n_children
        
        # update node's pagerank
        v.update_pagerank(updated_prob)
    
    if i % (n_iterations / 5) == 0:
        print("iteration", i)

R.put_objects(res)