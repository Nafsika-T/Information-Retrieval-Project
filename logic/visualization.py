import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

# This method creates a bar chart to visualize the TF-IDF values for keywords of a specific year and saves it as an image
def visualize_keywords(term_value_tuples, year, name, is_member):
    terms = [term[0] for term in term_value_tuples]
    scores = [score[1] for score in term_value_tuples]

    indexes = range(len(terms))

    plt.figure(figsize=(12, 12))

    plt.bar(indexes, scores)

    plt.xticks(indexes, terms)

    plt.xticks(rotation=45, ha='right')

    plt.xlabel('Keywords')

    plt.ylabel('tf-idf value')

    plt.title(f"Year: {year}")

    if is_member:
        plt.savefig(f"Data/parliament_data/parliament_member/{name}/{year}/{year}.png")
    else:
        plt.savefig(f"Data/parliament_data/parliament_party/{name}/{year}/{year}.png")

    plt.close()

# This method creates a star graph to visualize the entities of a member and saves the graph as an image
def visualize_entities(member_name, df):
    if df.empty:
        print(f"Δεν βρέθηκαν οντότητες για {member_name}.")
        return

    required_columns = {'Entity', 'Label'}
    if not required_columns.issubset(df.columns):
        print(f"Το DataFrame δεν περιέχει τις στήλες για {member_name}.")
        return

    df.dropna(subset=['Entity', 'Label'], inplace=True)

    plt.figure(figsize=(12, 12))

    G = nx.star_graph([''])

    nodes = df['Entity']

    edges = []
    edge_labels = list(df['Label'])

    for node in nodes:
        edges.append(('', node))

    edge_label_dict = {}

    G.add_nodes_from(nodes) 

    for index, edge in enumerate(edges):
        edge_label_dict[edge] = edge_labels[index]

    for edge in edges:
        G.add_edge(edge[0], edge[1], label=edge_label_dict[edge])

    pos = nx.spring_layout(G)

    nx.draw(G, pos, linewidths=1, labels={node: node for node in G.nodes})

    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'label'), font_color='red')

    plt.axis('off')

    plt.title(f"NER for: {member_name}")

    plt.savefig(f"Data/parliament_data/parliament_member/{member_name}/ner.png", dpi=300)

    plt.close()
