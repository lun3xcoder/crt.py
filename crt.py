# For compatibility with both Python 2 and 3
from __future__ import print_function
import os
import requests
import argparse


def print_header():
    header = (
        "\n"
        "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n"
        "|      ..| search crt.sh v1.0 |..     |\n"
        "+   site : crt.sh Certificate Search  +\n"
        "|  https://www.linkedin.com/in/lun3x/ |\n"
        "+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
        "\n"
    )
    print(header)


def get_certificate_data(domain):
    url = "https://crt.sh?q={}&output=json".format(domain)

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Filter out entries starting with '*.'
        filtered_data = [
            entry for entry in data if not entry["common_name"].startswith("*.")]

        # Remove duplicates based on the common_name
        unique_data = {entry["common_name"]                       : entry for entry in filtered_data}.values()

        return list(unique_data)
    except requests.exceptions.RequestException as err:
        print("Error: {}".format(err))
        return None


def extract_common_names(certificate_data, output_folder, domain):
    unique_common_names = set(certificate["common_name"]
                              for certificate in certificate_data)
    save_path = os.path.join(output_folder, f"{domain}.txt")

    with open(save_path, "w") as file:
        for common_name in unique_common_names:
            file.write("{}\n".format(common_name))

    return unique_common_names  # Add this line to return the set of unique common names


def main():
    print_header()

    parser = argparse.ArgumentParser(
        usage="python crt.py -d DOMAIN ",
        description="Extract unique Common Names from a domain's SSL certificates."
    )
    parser.add_argument("-d", required=True,
                        help="Specify the domain for certificate data retrieval.")
    parser.add_argument("-o", default="output",
                        help="Specify the output folder.")

    args = parser.parse_args()

    certificate_data = get_certificate_data(args.d)

    if certificate_data:
        output_folder = args.o
        domain = args.d

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        unique_common_names = extract_common_names(
            certificate_data, output_folder, domain)
        print("Found {} unique Common Names. Extracted and saved to '{}/{}.txt' file.".format(
            len(unique_common_names), output_folder, domain))
    else:
        print("Failed to retrieve certificate data for {}".format(args.domain))


if __name__ == "__main__":
    main()
