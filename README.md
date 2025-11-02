## Feedzgerald

Feedzgerald is an application used to curate RSS feeds and by filtering existing ones. For example, it can be used to expose an RSS feeds to a YouTube channel for specific topics, or by excluding topics.

At the time of this writing, this is my personal feedzgerald configuration file:

```toml
[core]
output_folder = "/feeds"

[feeds.kexp_full_concerts]
name = "KEXP - Full Performances"
url = "https://www.youtube.com/feeds/videos.xml?channel_id=UC3I2GFN_F8WudD_2jUZbojA"
website = "https://www.youtube.com/@kexp"
title_filter = "Full Performance"

[feeds.knights_of_last_call]
name = "Knights of Last Call"
url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCIVOFu4geQx5KrTTQwtIyMg"
website = "https://www.youtube.com/@KnightsofLastCall"
negative_title_filter = "Torchbearer"

[feeds.roll_for_combat]
name = "Roll for Combat"
url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCU4p5Dgq5G8cA2OMU1SLpXw"
website = "https://www.youtube.com/@RollForCombat"
negative_title_filter = "Jewel of the Indigo Isles"

[feeds.backseat]
name = "Backseat"
url = "https://www.youtube.com/feeds/videos.xml?channel_id=UC2ijB3_Fg2pIW1g6FeIiYKA"
website = "https://www.youtube.com/@backseat_fr"
title_filter = "BACKSEAT - S0"

[feeds.dm_lair]
name = "The DM Lair"
url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCk9dtbM-wjpLk134r55OUbg"
website = "https://www.youtube.com/@theDMLair"
negative_url_filter = "youtube.com/shorts/"
negative_title_filter = "Q&A"

[feeds.tiny_desk_concerts]
name = "Tiny Desk Concerts"
url = "https://www.youtube.com/feeds/videos.xml?channel_id=UC4eYXhJI4-7wSWc8UNRwD4A"
website = "https://www.youtube.com/@nprmusic"
title_filter = "Tiny Desk Concert"
```


### Installation

You can run
```console
$ pip install feedzgerald
$ feedzgerald -c ./path/to/config.toml
```

Alternatively, you can use the provided docker image to run `feedzgerald` without installing any python dependencies:
```console
$ docker run -it --rm \
  --name=feedzgerald
  -v path/to/feedzgerald/config.toml:/app/config.toml
  -v path/to/output_folder/feedzgerald:/feeds
  brouberol/feedzgerald
  --config /app/config.toml
```
