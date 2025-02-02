---
description: Learn about fundamental concepts of qyver.
icon: chart-line
---

# Analytics - User Acquisition

In this use case we are going to embed our user data in order to draw relevant conclusions our user acquisition.

Recently we have run 2 campaings - an older one at the end of August, and a more recent one right before Christmas, 2023. The first campaign operated with more generic messages, while the latter one was aided by XYZCr$$d, a made up influencer.

In terms of user data, we have 
1. the ad creative the users clicked on
2. the signup date as a unix timestamp
3. and the average daily activity (measured in API calls / day)

Embedding those inputs in a vectorspace allows us to cluster them and find meaningful user groups.

To understand the embeddings we will
- create a UMAP visualisation
- and examine the cluster labels' association with initial features

### Follow along in this Colab

{% embed url="https://colab.research.google.com/github/qyver/qyver/blob/main/notebook/analytics_user_acquisition.ipynb" %}
{% endembed %}
