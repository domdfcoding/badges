# stdlib
import datetime
import json
import re

# 3rd party
import pybadges
import pypistats
from domdf_python_tools.paths import PathPlus

badges_directory = PathPlus("downloads")
badges_directory.maybe_make()

yellow = 10
yellowgreen = 100
green = 1000


def get_badge_colour(count: int) -> str:
	if (count <= 0):
		return "red"
	elif (count < yellow):
		return "yellow"
	elif (count < yellowgreen):
		return "yellowgreen"
	elif (count < green):
		return "green"
	else:
		return "brightgreen"


# def format_download_count(num):
# 	for unit in ("", "K", "M"):
# 		if abs(num) < 1000:
# 			return f"{int(num)}{unit}"
# 		num /= 1000
# 	return f"{int(num*1000)}M"


def format_download_count(num):
	if num >= 1000000:
		return f"{int(num/1000000)}M"
	elif num >= 1000:
		return f"{int(num/1000)}K"
	else:
		return f"{int(num)}"


current_timestamp = datetime.datetime.now()

for project in [
		# python-formate
		"astatine",
		"flake8-dunder-all",
		"flake8-encodings",
		"flake8-github-actions",
		"flake8-prettycount",
		"flake8-slots",
		"flake8-sphinx-links",
		"flake8-strftime",
		"formate",
		"formate-black",
		"snippet-fmt",

  # python-coincidence
		"coincidence",
		"coverage-pyver-pragma",
		"dep-checker",
		"importcheck",
		"pytest-mypy-plugins-shim",
		"tox-envlist",
		"tox-recreate-hook",

  # sphinx-toolbox
		"default-values",
		"dict2css",
		"extras-require",
		"html-section",
		"seed-intersphinx-mapping",
		"sphinx-autofixture",
		"sphinx-debuginfo",
		"sphinx-highlights",
		"sphinx-jinja2-compat",
		"sphinx-licenseinfo",
		"sphinx-packaging",
		"sphinx-pyproject",
		"sphinx-toolbox",
		"toctree-plus",

  # GunShotMatch
		"libgunshotmatch",
		"apeye",
		"apeye-core",
		]:

	badge_file = badges_directory / f"{project}.svg"

	if badge_file.exists():
		existing_badge = badge_file.read_text()
		raw_timestamp = existing_badge.splitlines()[0]
		match = re.match("<!--last-modified: (.*)-->", raw_timestamp)
		if match is not None:
			timestamp = datetime.datetime.fromisoformat(match.group(1))

			if (current_timestamp - timestamp) < datetime.timedelta(hours=23):
				# No need to generate a new badge yet
				print(f"{project}: Badge last modified at {timestamp}")
				continue

	download_count = json.loads(pypistats.recent(project, "month", format="json"))["data"]["last_month"]

	s = pybadges.badge(
			left_text="downloads",
			right_text=f"{format_download_count(download_count)}/month",
			right_color=get_badge_colour(download_count),
			)
	badge_file.write_lines([
			f"<!--last-modified: {current_timestamp.isoformat()}-->",
			s,
			])
	print(f"{project}: Wrote new badge")
