import markdownify, html2text
from bs4 import Comment, BeautifulSoup
import re
import urllib


def parse_series(content, description_format="markdown"):
    """
    Parse series info from mangaupdates.

    Parameters
    ----------
    content : BeautifulSoup
        BeautifulSoup object of series page html.
    description_format : str, optional
        Format to transform the description into. can be 'plain', 'raw' or 'markdown'. defaults to 'markdown'.

    Returns
    -------
    series : dict
        Series information.
        ::

            {
                # main info
                'title': 'Series Name',
                'year':
                'type': 'Type of series (manhwa,manhua,manga,et)',
                'status': 'n Volumes (Ongoing or Complete or etc..)'
                'image': 'cover image link',
                'last_updated': 'December 3rd 2020, 5:32pm PST', # last time page was updated
                # authors & artists
                'artists': [
                    {
                        'id': 'Artist's Manga Updates ID',
                        'name': 'Artist's Name'
                    }
                ],
                'authors': [
                    {
                        'id': 'Author's Manga Updates ID',
                        'name': 'Author's Name'
                    }
                ],
                # relations
                'associated_names': [ # often in different languages, so make sure you can handle unicode.
                     'Name one',
                     'Name two'
                ],
                'related_series': [
                    {
                        'id': 'Related Series ID',
                        'name': 'Related Series Name',
                        'relation': 'Relation to current manga'
                    }
                ],
                'anime_chapters': [ # if it doesn't have an anime, list will be empty
                    'Starts at Vol x, Chap y',
                    'Ends at Vol z, Chap w'
                ],
                # description & genre
                'genres': [
                    'Genre',
                    ...
                ],
                'categories': [
                    {
                        'category': 'Category Name',
                        'score': '16 (16,0)'
                    }
                ],
                'description': 'Lorem ipsum dolor sit amet..',
                # publishing info
                'publisher': {
                    'id': 'publisher ID',
                    'name': 'publisher name'
                },
                'serialized': {
                    'link': 'mangaupdates link to where it was serialized',
                    'name': 'name of where it was serialized'
                },
                'licensed': True or False # whether this series was licensed in english,
                'english_publisher': {
                    'id': 'English Publisher ID',
                    'name': 'English Publisher Name + Volume Info'
                },
                # scanlation info
                'completely_scanlated': True or False,
                'latest_releases': [
                    {
                        'chapter': 'chapter number',
                        'volume': 'volume number if present',
                        'date': 'n days ago',
                        'group': {
                            'id': 'Scanlation Group ID',
                            'name': 'Scanlation Group Name'
                        }
                    }
                ],
                'groups': [ # all scanlation groups that published releases for this series
                    {
                        'id': 'Scanlation Group ID',
                        'name': 'Scanlation Group Name'
                    }
                ],
                # recommendations
                'category_recs': [
                    {
                        'id': 'Recommended Series ID',
                        'name': 'Recommended Series Name'
                    }
                ],
                'recs': [
                    {
                        'id': 'Recommended Series ID',
                        'name': 'Recommended Series Name'
                    }
                ],
                # user-related info
                'positions': {
                    'monthly': '779',
                    'monthly_change': '+155',
                    'six_monthly': '1244',
                    'six_monthly_change': '+76',
                    'tri_monthly': '1120',
                    'tri_monthly_change': '-17',
                    'weekly': '431',
                    'weekly_change': '+121',
                    'yearly': '1277',
                    'yearly_change': '-162'
                },
                'average': { # ratings
                    'average': 'average rating',
                    'bayesian': 'bayesian average rating',
                    'votes': 'n votes'
                },
                'reading_lists': {
                    'custom': 'n',
                    'reading': 'n',
                    'unfinished': 'n',
                    'wish': 'n'
                },
                'forum': {
                    'link': 'https://www.mangaupdates.com/topics.php?fid=120202',
                    'status': 'None'
                }
            }


    """
    manga = {}
    manga["title"] = str(content.find("span", class_="releasestitle").get_text())

    cols = content.find_all("div", class_="col-6", recursive=False)
    col_1 = cols[0]
    col_2 = cols[1]

    _parse_col_1(col_1, manga, description_format)
    _parse_col_2(col_2, manga)
    return manga


def _parse_col_1(col, manga, description_format):
    contents = col.find_all("div", class_="sContent", recursive=False)

    desc_tag = contents[0]

    desc_more = desc_tag.find(id="div_desc_more")
    if desc_more:
        desc_more.a.extract()
        desc_html = desc_more
    else:
        desc_html = desc_tag

    if description_format == "markdown":
        manga["description"] = markdownify.markdownify(str(desc_html))
    elif description_format == "raw":
        manga["description"] = str(desc_html)
    elif description_format == "plain":
        text_converter = html2text.HTML2Text()
        text_converter.ignore_links = True
        text_converter.unicode_snob = True
        text_converter.ignore_emphasis = True
        text_converter.ignore_anchors = True
        text_converter.ignore_images = True
        manga["description"] = text_converter.handle(str(desc_html))

    manga["type"] = contents[1].get_text().replace("\n", "")

    manga["related_series"] = []
    for link in contents[2].findAll("a"):
        manga["related_series"].append(
            {
                "name": link.get_text(),
                "id": link.get("href", "").replace("series.html?id=", ""),
                "relation": str(link.nextSibling)
                .strip()
                .replace("(", "")
                .replace(")", ""),
            }
        )

    manga["associated_names"] = [
        markdownify.markdownify(name)
        for name in contents[3]
        .encode_contents()
        .decode("utf-8")
        .replace("\n", "")
        .replace("</br>", "")
        .split("<br>")
        if len(name) > 0 and name != "N/A"
    ]

    if "N/A" not in contents[4].get_text():
        if contents[4].a is None:
            manga["groups"] = [{"name": contents[4].get_text().strip(), "id": None}]
        else:
            manga["groups"] = []
            for group in contents[4].findAll("a", attrs={"title": "Group Info"}):
                manga["groups"].append(
                    {
                        "name": group.get_text(),
                        "id": group["href"].replace(
                            "https://www.mangaupdates.com/groups.html?id=", ""
                        ),
                    }
                )
    else:
        manga["groups"] = []

    manga["latest_releases"] = []
    numbers = contents[5].find_all("i")[:-1]
    groups = contents[5].find_all("a")[:-1]
    dates = contents[5].find_all("span")

    for i in range(0, len(dates)):
        if len(numbers) != len(groups):
            continue
        release = {
            "group": {
                "name": groups[i].get_text(),
                "id": str(
                    groups[i]
                    .get("href", "")
                    .replace("https://www.mangaupdates.com/groups.html?id=", "")
                ),
            },
            "date": dates[i]["title"],
        }

        # this is to check if there are volume numbers. its a bad solution, folks!
        if len(numbers) >= len(dates) * 2:
            release["volume"] = numbers[i].get_text()
            release["chapter"] = numbers[i + 1].get_text()
        else:
            release["chapter"] = numbers[i].get_text()

        manga["latest_releases"].append(release)

    [m.unwrap() for t in ["b", "i", "u"] for m in contents[6].findAll(t)]
    manga["status"] = (
        BeautifulSoup(repr(contents[6]), "html.parser")
        .get_text(separator="!@#")
        .replace("\n", "")
        .split("!@#")
    )
    if str(contents[7].string).replace("\n", "") == "No":
        manga["completely_scanlated"] = False
    else:
        manga["completely_scanlated"] = True

    manga["anime_chapters"] = (
        None
        if "N/A" in contents[8].get_text()
        else contents[8]
        .encode_contents()
        .decode("utf-8")
        .replace("\n", "")
        .split("<br/>")
    )
    manga["user_reviews"] = contents[9].get_text().replace("\n", "")

    manga["forum"] = {
        "status": contents[10].get_text(),
        "link": "https://www.mangaupdates.com/" + contents[10].a.get("href", ""),
    }

    try:
        average_raw = contents[11].contents
        manga["average"] = {
            "average": str(average_raw[0]).replace("Average:", "").replace(" ", ""),
            "votes": str(average_raw[2]).replace("(", "").replace(")", ""),
            "bayesian": str(average_raw[5]).replace("<b>", "").replace("</b>", ""),
        }
    except:
        manga["average"] = None

    manga["last_updated"] = contents[12].get_text().replace("\n", "")


def _parse_col_2(col, manga):
    contents = col.find_all("div", class_="sContent", recursive=False)

    try:
        manga["image"] = contents[0].center.img["src"]
    except:
        manga["image"] = None

    manga["genres"] = []
    for genre in contents[1].find_all("a")[:-1]:
        manga["genres"].append(genre.u.get_text())

    manga["categories"] = []
    if contents[2].div:
        for cat_raw in contents[2].div.ul.find_all("li"):
            cat = cat_raw.find("a", rel="nofollow")
            manga["categories"].append(
                {
                    "category": cat.get_text(),
                    "score": str(cat["title"]).replace("Score:", ""),
                }
            )

    manga["category_recs"] = []
    for rec in contents[3].find_all("a", recursive=True):
        if "javascript" not in rec.get("href", ""):
            manga["category_recs"].append(
                {
                    "name": rec.get_text(),
                    "id": rec.get("href", "").replace("series.html?id=", ""),
                }
            )

    manga["recs"] = []
    for rec in contents[4].find_all("a", recursive=True):
        if "javascript" not in rec.get("href", ""):
            manga["recs"].append(
                {
                    "name": rec.get_text(),
                    "id": rec.get("href", "").replace("series.html?id=", ""),
                }
            )

    manga["authors"] = []
    for author in contents[5].find_all("a"):
        query = urllib.parse.parse_qs(
            urllib.parse.urlparse(author.get("href", "")).query
        )
        if "id" in query.keys():
            manga["authors"].append(
                {
                    "name": author.get_text(),
                    "id": query["id"][0] if contents[5].a else "N/A",
                }
            )
        elif "author" in query.keys():
            manga["authors"].append(
                {
                    "name": query["author"][0],
                    "id": "N/A",
                }
            )
        else:
            manga["authors"].append(
                {
                    "name": author.get_text(),
                    "id": "N/A",
                }
            )

    manga["artists"] = []
    for artist in contents[6].find_all("a"):
        query = urllib.parse.parse_qs(
            urllib.parse.urlparse(artist.get("href", "")).query
        )
        if "id" in query.keys():
            manga["artists"].append(
                {
                    "name": artist.get_text(),
                    "id": query["id"][0] if contents[6].a else "N/A",
                }
            )
        elif "author" in query.keys():
            manga["artists"].append(
                {
                    "name": query["author"][0],
                    "id": "N/A",
                }
            )
        else:
            manga["artists"].append(
                {
                    "name": artist.get_text(),
                    "id": "N/A",
                }
            )

    manga["year"] = contents[7].get_text().replace("\n", "")

    manga["publisher"] = {
        "name": contents[8].get_text().strip(),
        "id": contents[8]
        .a.get("href", "")
        .replace("https://www.mangaupdates.com/publishers.html?id=", "")
        if contents[8].a
        else "N/A",
    }

    # TODO: add publisher info
    manga["serialized"] = {
        "name": contents[9].get_text().strip(),
        "link": "https://www.mangaupdates.com/" + contents[9].a.get("href", "")
        if contents[9].a
        else "",
    }

    manga["licensed"] = True if "Yes" in contents[10].get_text() else False

    # TODO: add volume/ongoing info
    manga["english_publisher"] = {
        "name": str(contents[11].get_text().strip()),
        "id": str(
            contents[11]
            .a.get("href", "")
            .replace("https://www.mangaupdates.com/publishers.html?id=", "")
            if contents[11].a
            else "N/A"
        ),
    }

    positions = dict()
    pos_r = str(contents[12]).split("<br/>")
    for title, p in zip(
        ["weekly", "monthly", "tri_monthly", "six_monthly", "yearly"], pos_r
    ):
        position = re.search("<b>(\d+)</b>", p)
        change = re.search("\(([^()]+)\)", p)
        
        if position is not None:
            positions[title] = position.group(1)
        
        if change is not None:
            positions[title + "_change"] = change.group(1)
        else:
            positions[title + "_change"] = ""

    manga["positions"] = positions

    manga["reading_lists"] = dict()
    cnt = ""
    for obj in contents[13]:
        if "<b>" in str(obj):
            cnt = obj.get_text().strip()

        if "lists" in str(obj):
            if "reading" in str(obj):
                manga["reading_lists"]["reading"] = cnt
            if "wish" in str(obj):
                manga["reading_lists"]["wish"] = cnt
            if "completed" in str(obj):
                manga["reading_lists"]["completed"] = cnt
            if "unfinished" in str(obj):
                manga["reading_lists"]["unfinished"] = cnt
            if "custom" in str(obj):
                manga["reading_lists"]["custom"] = cnt

