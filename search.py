from requests import exceptions
import argparse
import requests
import cv2
import os
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", required=True,
	help="search query to search Bing Image API for")
ap.add_argument("-o", "--output", required=True,
	help="path to output directory of images")
args = vars(ap.parse_args())
API_KEY = "8ea9021ed2594d95b0e3f692583285e6"
MAX_RESULTS = 2000
GROUP_SIZE = 50
URL = "https://api.bing.microsoft.com/v7.0/images/search"
EXCEPTIONS = set([IOError, FileNotFoundError,
	exceptions.RequestException, exceptions.HTTPError,
	exceptions.ConnectionError, exceptions.Timeout])
term = args["query"]
headers = {"Ocp-Apim-Subscription-Key" : API_KEY}
params = {"q": term, "offset": 0, "count": GROUP_SIZE}
print("[INFO] searching Bing API for '{}'".format(term))
search = requests.get(URL, headers=headers, params=params)
search.raise_for_status()
results = search.json()
estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
print("[INFO] {} total results for '{}'".format(estNumResults,
	term))
total = 0
for offset in range(0, estNumResults, GROUP_SIZE):
	print("[INFO] making request for group {}-{} of {}...".format(
		offset, offset + GROUP_SIZE, estNumResults))
	params["offset"] = offset
	search = requests.get(URL, headers=headers, params=params)
	search.raise_for_status()
	results = search.json()
	print("[INFO] saving images for group {}-{} of {}...".format(
		offset, offset + GROUP_SIZE, estNumResults))
	for v in results["value"]:
		try:
			print("[INFO] fetching: {}".format(v["contentUrl"]))
			r = requests.get(v["contentUrl"], timeout=30)
			ext = v["contentUrl"][v["contentUrl"].rfind("."):]
			p = os.path.join(args["output"], "{}{}".format(
				str(total).zfill(8), ext))
			f = open(p, "wb")
			f.write(r.content)
			f.close()
		except Exception as e:
			if type(e) in EXCEPTIONS:
				print("[INFO] skipping: {} due to exception: {}".format(v["contentUrl"], str(e)))
				continue
		image = cv2.imread(p)
		if image is None:
			print("[INFO] deleting: {} (invalid or unsupported image format)".format(p))
			os.remove(p)
			continue
		total += 1
