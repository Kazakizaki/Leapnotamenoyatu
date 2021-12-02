#QPU上のactive/inactiveな量子ビットとカプラーを可視化する
def visualize_qpu(sampler, fname, dir=".", figsize=(7, 7), ok_color="cyan", ng_color="red", node_size=1, width=1, **plot_args):
    topology = sampler.properties["topology"]["type"]

    if   topology == "pegasus":
        G_ideal = dnx.pegasus_graph(16)
    elif topology == "chimera":
        G_ideal = dnx.chimera_graph(16, 16, 4)
    else:
        raise ValueError(f"{topology}")

    #set node color
    ideal_nodes   = G_ideal.nodes()
    sampler_nodes = sampler.nodelist
    node_color      = {v:ok_color for v in ideal_nodes}
    node_color.update({v:ng_color for v in (set(ideal_nodes) - set(sampler_nodes))})
    node_color = node_color.values()

    #set edge color
    ideal_edges   = G_ideal.edges()
    sampler_edges = sampler.edgelist
    diff_edges = []
    for u, v in ideal_edges:
        if (u, v) not in sampler_edges:
            if (v, u) not in sampler_edges:
                diff_edges.append((u, v))
    edge_color      = {e: ok_color for e in ideal_edges}
    edge_color.update({e: ng_color for e in diff_edges})
    edge_color = edge_color.values()
    
    #plot
    plt.figure(figsize=figsize)
    draw_func = dnx.draw_pegasus if topology == "pegasus" else dnx.draw_chimera
    draw_func(G_ideal, crosses=True, with_labels=True, node_color=node_color, edge_color=edge_color, **plot_args)
    plt.savefig('{0}/{1}.pdf'.format(dir,fname))
    plt.show()
