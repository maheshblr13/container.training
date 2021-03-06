#!/usr/bin/env python3
import os
import sys
import yaml
import jinja2


# Read settings from user-provided settings file
context = yaml.safe_load(open(sys.argv[1]))

ips = list(open("ips.txt"))
clustersize = context["clustersize"]

print("---------------------------------------------")
print("   Number of IPs: {}".format(len(ips)))
print(" VMs per cluster: {}".format(clustersize))
print("---------------------------------------------")

assert len(ips)%clustersize == 0

clusters = []

while ips:
    cluster = ips[:clustersize]
    ips = ips[clustersize:]
    clusters.append(cluster)

context["clusters"] = clusters

template_file_name = context["cards_template"]
template_file_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "templates",
    template_file_name
    )
template = jinja2.Template(open(template_file_path).read())
with open("ips.html", "w") as f:
	f.write(template.render(**context))
print("Generated ips.html")


try:
    import pdfkit
    with open("ips.html") as f:
        pdfkit.from_file(f, "ips.pdf", options={
            "page-size": context["paper_size"],
            "margin-top": context["paper_margin"],
            "margin-bottom": context["paper_margin"],
            "margin-left": context["paper_margin"],
            "margin-right": context["paper_margin"],
            })
    print("Generated ips.pdf")
except ImportError:
    print("WARNING: could not import pdfkit; did not generate ips.pdf")
