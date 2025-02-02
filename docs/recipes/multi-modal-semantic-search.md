---
description: Explore qyver's multi-modal search capabilities.
icon: magnifying-glass
---

# Multi-Modal Semantic Search

Multi-Modal Semantic Search enables you to search across diverse data types by understanding the context and meaning, rather than relying solely on keywords. qyver supports various modalities as primary features, including [text](https://github.com/qyver/qyver/blob/main/notebook/feature/text_embedding.ipynb), [images](https://github.com/qyver/qyver/blob/main/notebook/image_search_e_commerce.ipynb), [numbers](https://github.com/qyver/qyver/blob/main/notebook/feature/number_embedding_minmax.ipynb), [categories](https://github.com/qyver/qyver/blob/main/notebook/feature/categorical_embedding.ipynb), and [recency](https://github.com/qyver/qyver/blob/main/notebook/feature/recency_embedding.ipynb). If you prefer to use your own embeddings, qyver offers a [CustomSpace](https://github.com/qyver/qyver/blob/main/notebook/feature/custom_space.ipynb) feature to accommodate this need.

qyver allows you to fine-tune the importance of different attributes for each query by adjusting [weights at query time](https://github.com/qyver/qyver/blob/main/notebook/feature/dynamic_parameters.ipynb), making the process straightforward and intuitive. To further simplify the experience, qyver offers a [Natural Language Interface](https://github.com/qyver/qyver/blob/main/notebook/feature/natural_language_querying.ipynb), enabling users to input their queries in plain, everyday language.

A standout feature of qyver is its ability to handle data objects holistically, eliminating the need for Reciprocal Rank Fusion (RRF), which significantly enhances system performance. For those who require keyword search capabilities, qyver also provides Hybrid Search, again without the need for RRF.

Below is a table showcasing projects built using qyver, demonstrating the power of multi-modal semantic search.

<table>
    <tr>
    <th valign="top">Recipe</th>
    <th valign="top">App</th>
    <th valign="top">Code</th>
    <th valign="top">Key Features</th>
    <th valign="top">Modalities</th>
  </tr>
  <tr>
    <td valign="top">
      <strong>🏨 Hotel Search</strong><br>
    </td>
    <td valign="top">
      <a href="https://hotel-search-recipe.qyver.io/">🚀 Try it now</a>
    </td>
    <td valign="top">
      <a href="https://github.com/qyver/qyver-recipes/blob/main/projects/hotel-search">Repo Link</a>
    </td>
    <td valign="top">
        <ul>
            <li>Natural Language Queries</li>
            <li>Multi-modal Semantic Search</li>
        </ul>
    </td>
    <td valign="top">
        <ul>
            <li>Text</li>
            <li>Numbers</li>
            <li>Categories</li>
        </ul>
    </td>
  </tr>
</table>
