---
description: Learn about fundamental concepts of qyver.
icon: magnifying-glass
---

# Semantic Search - News

This use case implements semantic search in [news](https://www.kaggle.com/datasets/rmisra/news-category-dataset) articles. 
The dataset is filtered for news in the 'BUSINESS' category.

We are embedding
- headlines
- news body (short description)
- and date
  
to be able to search for
- notable events, or
- related articles to a specific story.

There is a possibility to skew the results towards older or fresher news,
and also to influence the results using a specific search term.

### Follow along in this Colab

{% embed url="https://colab.research.google.com/github/qyver/qyver/blob/main/notebook/semantic_search_news.ipynb" %}
{% endembed %}
