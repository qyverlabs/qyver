# Table of contents
* [Welcome](README.md)
## Getting Started
* [Why qyver?](getting-started/why-qyver.md)
* [Setup qyver](getting-started/installation.md)
* [Basic Building Blocks](getting-started/basic-building-blocks.md)
## Run in Production
* [Overview](run-in-production/overview.md)
* [Setup qyver Server](run-in-production/setup/index.md)
  * [Configuring your app](run-in-production/setup/configuring-your-app.md)
  * [Interacting with app via API](run-in-production/setup/interacting-with-app-via-api.md)
* [Supported Vector Databases](run-in-production/vdbs/index.md)
  * [Redis](run-in-production/vdbs/redis.md)
  * [Mongo DB](run-in-production/vdbs/mongodb.md)
  * [Qdrant](run-in-production/vdbs/qdrant.md)


## Concepts
* [Overview](concepts/overview.md)
<!-- * [Features](concepts/features.md) -->
* [Combining Multiple Embeddings for Better Retrieval Outcomes](concepts/multiple-embeddings.md)
* [Dynamic Parameters/Query Time weights](concepts/dynamic-parameters.md)


## Reference
* [Overview](reference/overview.md)
* [Changelog](reference/changelog.md)
* [Components](reference/components.md)
  * [Schema](reference/common/schema)
    * [Id Schema Object](reference/common/schema/id_schema_object.md)
    * [Event Schema Object](reference/common/schema/event_schema_object.md)
    * [Schema Object](reference/common/schema/schema_object.md)
    * [Event Schema](reference/common/schema/event_schema.md)
    * [Schema](reference/common/schema/schema.md)
  * [Dag](reference/common/dag)
    * [Period Time](reference/common/dag/period_time.md)
  * [Parser](reference/common/parser)
    * [Data Parser](reference/common/parser/data_parser.md)
    * [Dataframe Parser](reference/common/parser/dataframe_parser.md)
    * [Json Parser](reference/common/parser/json_parser.md)
  * [App](reference/dsl/app/index.md)
    * [App](reference/dsl/app/app.md)
    * [Rest](reference/dsl/app/rest/index.md)
      * [Rest App](reference/dsl/app/rest/rest_app.md)
    * [Interactive](reference/dsl/app/interactive/index.md)
      * [Interactive App](reference/dsl/app/interactive/interactive_app.md)
    * [In Memory](reference/dsl/app/in_memory/index.md)
      * [In Memory App](reference/dsl/app/in_memory/in_memory_app.md)
    * [Online](reference/dsl/app/online/index.md)
      * [Online App](reference/dsl/app/online/online_app.md)
  * [Registry](reference/dsl/registry/index.md)
    * [qyver Registry](reference/dsl/registry/qyver_registry.md)
    * [Exception](reference/dsl/registry/exception.md)
  * [Source](reference/dsl/source/index.md)
    * [Types](reference/dsl/source/types.md)
    * [Interactive Source](reference/dsl/source/interactive_source.md)
    * [Data Loader Source](reference/dsl/source/data_loader_source.md)
    * [Source](reference/dsl/source/source.md)
    * [Rest Source](reference/dsl/source/rest_source.md)
    * [In Memory Source](reference/dsl/source/in_memory_source.md)
  * [Executor](reference/dsl/executor/index.md)
    * [Exception](reference/dsl/executor/exception.md)
    * [Executor](reference/dsl/executor/executor.md)
    * [Rest](reference/dsl/executor/rest/index.md)
      * [Rest Descriptor](reference/dsl/executor/rest/rest_descriptor.md)
      * [Rest Configuration](reference/dsl/executor/rest/rest_configuration.md)
      * [Rest Executor](reference/dsl/executor/rest/rest_executor.md)
      * [Rest Handler](reference/dsl/executor/rest/rest_handler.md)
    * [Interactive](reference/dsl/executor/interactive/index.md)
      * [Interactive Executor](reference/dsl/executor/interactive/interactive_executor.md)
    * [Query](reference/dsl/executor/query/index.md)
      * [Query Executor](reference/dsl/executor/query/query_executor.md)
    * [In Memory](reference/dsl/executor/in_memory/index.md)
      * [In Memory Executor](reference/dsl/executor/in_memory/in_memory_executor.md)
  * [Query](reference/dsl/query/index.md)
    * [Param](reference/dsl/query/param.md)
    * [Nlq Pydantic Model Builder](reference/dsl/query/nlq_pydantic_model_builder.md)
    * [Query](reference/dsl/query/query.md)
    * [Query Filter Validator](reference/dsl/query/query_filter_validator.md)
    * [Query Param Value Setter](reference/dsl/query/query_param_value_setter.md)
    * [Nlq Param Evaluator](reference/dsl/query/nlq_param_evaluator.md)
    * [Natural Language Query Param Handler](reference/dsl/query/natural_language_query_param_handler.md)
    * [Param Evaluator](reference/dsl/query/param_evaluator.md)
    * [Query Weighting](reference/dsl/query/query_weighting.md)
    * [Query Filter Information](reference/dsl/query/query_filter_information.md)
    * [Query Mixin](reference/dsl/query/query_mixin.md)
    * [Query Param Information](reference/dsl/query/query_param_information.md)
    * [Query Clause](reference/dsl/query/query_clause.md)
    * [Query Vector Factory](reference/dsl/query/query_vector_factory.md)
    * [Query Descriptor](reference/dsl/query/query_descriptor.md)
    * [Result](reference/dsl/query/result.md)
    * [Query Filters](reference/dsl/query/query_filters.md)
    * [Nlq](reference/dsl/query/nlq/index.md)
      * [Nlq Handler](reference/dsl/query/nlq/nlq_handler.md)
      * [Nlq Clause Collector](reference/dsl/query/nlq/nlq_clause_collector.md)
      * [Param Filler](reference/dsl/query/nlq/param_filler/index.md)
        * [Query Param Model Validator](reference/dsl/query/nlq/param_filler/query_param_model_validator.md)
        * [Query Param Model Builder](reference/dsl/query/nlq/param_filler/query_param_model_builder.md)
        * [Query Param Prompt Builder](reference/dsl/query/nlq/param_filler/query_param_prompt_builder.md)
        * [Query Param Model Validator Info](reference/dsl/query/nlq/param_filler/query_param_model_validator_info.md)
        * [Templates](reference/dsl/query/nlq/param_filler/templates/index.md)
      * [Suggestion](reference/dsl/query/nlq/suggestion/index.md)
        * [Query Suggestion Model](reference/dsl/query/nlq/suggestion/query_suggestion_model.md)
        * [Query Suggestions Prompt Builder](reference/dsl/query/nlq/suggestion/query_suggestions_prompt_builder.md)
    * [Predicate](reference/dsl/query/predicate/index.md)
      * [Binary Op](reference/dsl/query/predicate/binary_op.md)
      * [Binary Predicate](reference/dsl/query/predicate/binary_predicate.md)
      * [Query Predicate](reference/dsl/query/predicate/query_predicate.md)
    * [Query Result Converter](reference/dsl/query/query_result_converter/index.md)
      * [Serializable Query Result Converter](reference/dsl/query/query_result_converter/serializable_query_result_converter.md)
      * [Default Query Result Converter](reference/dsl/query/query_result_converter/default_query_result_converter.md)
      * [Query Result Converter](reference/dsl/query/query_result_converter/query_result_converter.md)
  * [Space](reference/dsl/space/index.md)
    * [Recency Space](reference/dsl/space/recency_space.md)
    * [Number Space](reference/dsl/space/number_space.md)
    * [Space Field Set](reference/dsl/space/space_field_set.md)
    * [Categorical Similarity Space](reference/dsl/space/categorical_similarity_space.md)
    * [Image Space Field Set](reference/dsl/space/image_space_field_set.md)
    * [Custom Space](reference/dsl/space/custom_space.md)
    * [Has Space Field Set](reference/dsl/space/has_space_field_set.md)
    * [Image Space](reference/dsl/space/image_space.md)
    * [Text Similarity Space](reference/dsl/space/text_similarity_space.md)
    * [Exception](reference/dsl/space/exception.md)
    * [Space](reference/dsl/space/space.md)
    * [Input Aggregation Mode](reference/dsl/space/input_aggregation_mode.md)
  * [Storage](reference/dsl/storage/index.md)
    * [Vector Database](reference/dsl/storage/vector_database.md)
    * [Mongo Db Vector Database](reference/dsl/storage/mongo_db_vector_database.md)
    * [Qdrant Vector Database](reference/dsl/storage/qdrant_vector_database.md)
    * [Redis Vector Database](reference/dsl/storage/redis_vector_database.md)
    * [In Memory Vector Database](reference/dsl/storage/in_memory_vector_database.md)
  * [Index](reference/dsl/index/index.md)
    * [Index](reference/dsl/index/index.m.md)
    * [Effect](reference/dsl/index/effect.md)
    * [Util](reference/dsl/index/util/index.md)
      * [Event Aggregation Effect Group](reference/dsl/index/util/event_aggregation_effect_group.md)
      * [Aggregation Effect Group](reference/dsl/index/util/aggregation_effect_group.md)
      * [Event Aggregation Node Util](reference/dsl/index/util/event_aggregation_node_util.md)
      * [Effect With Referenced Schema Object](reference/dsl/index/util/effect_with_referenced_schema_object.md)
      * [Aggregation Node Util](reference/dsl/index/util/aggregation_node_util.md)

## Recipes
* [Overview](recipes/overview.md)
* [Multi-Modal Semantic Search](recipes/multi-modal-semantic-search.md)
  * [Hotel Search](recipes/hotel-search.md)

## Tutorials
* [Overview](use-cases/overview.md)
* [Semantic Search - News](use-cases/semantic-search-news.md)
* [Semantic Search - Movies](use-cases/semantic-search-movies.md)
* [Semantic Search - Product Images & Descriptions](use-cases/semantic-search-product-images-descriptions.md)
* [RecSys - Ecommerce](use-cases/recsys-ecomm.md)
* [RAG - HR](use-cases/rag-hr.md)
* [Analytics - User Acquisition](use-cases/analytics-user-acquisition.md)
* [Analytics - Keyword Expansion](use-cases/analytics-keyword-expansion.md)

## Help & FAQ
* [Logging](help-and-faq/logging.md)
* [Support](help-and-faq/support.md)
* [Discussion](https://github.com/qyver/qyver/discussions)

## Policies
* [Terms of Use](https://qyver.com/policies/terms-and-conditions)
* [Privacy Policy](https://qyver.com/policies/privacy-policy)
