import random
import datetime
import argparse

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


def next_wednesday():
    today = datetime.datetime.today()
    days_until_wednesday = (2 - today.weekday()) % 7  # 2 is Wednesday (Monday=0, Sunday=6)
    if days_until_wednesday == 0:
        days_until_wednesday = 7  # If today is Wednesday, get next week's Wednesday
    next_wed = today + datetime.timedelta(days=(days_until_wednesday+7))
    return next_wed.day  # Return the day of the month


def main():

    file_path = 'names.csv'

    names, weights = initialise(file_path)

    num_to_draw = 3
    drawn_names, new_weights = select_names(names=names, weights=weights, num_selections=num_to_draw)
    
    write_names_and_weights(file_path, names, new_weights)

    # Generate new content
    now = datetime.datetime.now()
    with open("index.md", "w") as f:
        f.write(f"---\n")
        f.write(f"layout: default\n")
        f.write(f"---\n")
        f.write(f"\n")
        f.write(f"The cake fairy has chosen:\n")
        f.write(f"  -  {drawn_names[0]}\n")
        f.write(f"  -  {drawn_names[1]}\n")
        f.write(f"  -  {drawn_names[2]}\n")
        f.write(f"\n")
        f.write(f"to bring the cake next week. See you all on the Wednesday the {next_wednesday()}!\n")
        f.write(f"\n")
        f.write(f"\n")
        f.write(f"Updated {now.strftime('%Y-%m-%d %H:%M:%S')}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument('-y',    '--on_week' ,    dest='draw_name',   action='store_true' ,     help='Call this option to draw new names')
    feature_parser.add_argument('-n',    '--off_week',    dest='draw_name',   action='store_false',     help='Call this option to expilicity skip drawing names (this is also the default behaviour)')
    parser.set_defaults(draw_name=False)
    draw_name = parser.parse_args().draw_name
    if draw_name == True:
        main()
