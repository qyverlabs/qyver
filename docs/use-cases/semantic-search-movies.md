---
description: Learn about fundamental concepts of qyver.
icon: magnifying-glass
---

# Semantic Search - Movies

Finding out what to watch is tough choice mainly because of the abundance of options and the scarcity of time.
Let's follow a data-driven approach to arrive at a decision!

In our [dataset](https://www.kaggle.com/datasets/dgoenrique/netflix-movies-and-tv-shows) of movies, we know the
- description,
- genre
- title
- and the release_year
of the movie.

Putting together a vector index on top of these embedded inputs will create a space where we can search semantically to find our movie choice for tonight.

We are going to browse the movies

- searching with an idea (heartfelt romantic comedy)
- tweak around the results giving more imporance to matches in certain input fields
- search in description, genre and title with different search terms for each
- and after finding a close enough movie (that is not quite it), search around utilizing that one, too

### Follow along in this Colab

{% embed url="https://colab.research.google.com/github/qyver/qyver/blob/main/notebook/semantic_search_netflix_titles.ipynb" %}
{% endembed %}
