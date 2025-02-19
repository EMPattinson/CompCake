import random
import datetime

import csv

def initialise(file_path):
    names = []
    weights = []
    with open(file_path, 'r') as f:
        for line in f:
            row = line.strip().split(',')
            if row and len(row) >= 2:  # Ensure row has at least two elements
                name = row[0].strip()
                weight = float(row[1].strip())
                names.append(name)
                weights.append(weight)
    return names, weights


def select_names(names, weights, num_selections, decay_factor=0.1):

    selected_names = []

    temp_weights = weights.copy()  # Temporary weights for the current draw

    for _ in range(num_selections):
        # Select a name based on current weights
        selected = random.choices(names, weights=temp_weights, k=1)[0]
        selected_names.append(selected)

        # Find the index of the selected name
        idx = names.index(selected)

        # Set the weight of the selected name to 0 to avoid selecting it again in this draw
        temp_weights[idx] = 0

        # After the draw, reduce the actual weight of the selected name
        weights[idx] *= decay_factor  # Reduce the weight by the decay factor


    total_weight = sum(weights)
    new_weights = [100 * x / total_weight for x in weights]

    return selected_names, new_weights


def write_names_and_weights(file_path, names, weights):
    # Write the updated names and weights back to the CSV file
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for name, weight in zip(names, weights):
            writer.writerow([name, weight])


def add_name(new_name, names, weights):
    names.append(new_name)
    weights.append(max(weights))  # Assign default weight to the new name
    print(f"Added '{new_name}' to the list of names.")

    return names, weights

def main():

    file_path = 'names.csv'

    names, weights = initialise(file_path)

    num_to_draw = 3
    drawn_names, new_weights = select_names(names=names, weights=weights, num_selections=num_to_draw)
    write_names_and_weights(file_path, names, new_weights)
    print(f"Drawn names: {', '.join(drawn_names)}")


# Generate new content
    now = datetime.datetime.now()
    with open("index.md", "w") as f:
        f.write(f"---\n")
        f.write(f"layout: default\n")
        f.write(f"---\n")
        f.write(f"\n")
        f.write(f"#  CompCake\n")
        f.write(f"\n")
        f.write(f"The cake fairy has chosen:\n")
        f.write(f"  -  {drawn_names[0]}\n")
        f.write(f"  -  {drawn_names[1]}\n")
        f.write(f"  -  {drawn_names[2]}\n")
        f.write(f"\n")
        f.write(f"To bring the cake next week, see you all on the 26th!\n")
        f.write(f"\n")
        f.write(f"\n")
        f.write(f"# Updated on {now.strftime('%Y-%m-%d %H:%M:%S')}\n")
if __name__ == "__main__":
    main()
